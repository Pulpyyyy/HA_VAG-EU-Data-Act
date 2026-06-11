"""Entity registry migrations for translation_key / naming fixes."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er

from .const import CONF_VIN
from .data import (
    CURATED_SENSORS_DOTTED,
    CURATED_SENSORS_FLAT,
    curated_translation_key,
)

_FIELD_TO_TRANSLATION_KEY: dict[str, str] = {
    s.field_name: curated_translation_key(s.field_name, s.translation_key)
    for s in (*CURATED_SENSORS_DOTTED, *CURATED_SENSORS_FLAT)
}


def translation_key_for_unique_id(unique_id: str, vin: str) -> str | None:
    """Map a curated sensor unique_id to its HA translation_key."""
    if unique_id == f"{vin}_integration_status":
        return "integration_status"
    prefix = f"{vin}_"
    if not unique_id.startswith(prefix):
        return None
    return _FIELD_TO_TRANSLATION_KEY.get(unique_id[len(prefix) :])


async def async_migrate_entity_translations(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Ensure curated entities use translation_key instead of stale registry names.

    Curated sensors must not set ``_attr_name`` (especially not to ``None`` — that
    tells HA to use the device name only). Existing registry entries created
    before v0.5.3 may lack ``translation_key`` or still carry a custom ``name``
    override.
    """
    vin = entry.data[CONF_VIN]

    @callback
    def _migrate(reg_entry: er.RegistryEntry) -> dict | None:
        if reg_entry.domain != "sensor":
            return None
        key = translation_key_for_unique_id(reg_entry.unique_id, vin)
        if not key:
            return None
        if reg_entry.translation_key == key and reg_entry.name is None:
            return None
        return {"translation_key": key, "name": None}

    await er.async_migrate_entries(hass, entry.entry_id, _migrate)
