"""Repairs-center issues for portal delivery states."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import issue_registry as ir

from .const import BASE_URL, CONF_NICKNAME, DOMAIN, RETRY_INTERVAL
from .coordinator import EudaCoordinator

# Status labels that should surface a repairs issue (see coordinator.status_label).
_ISSUE_STATUSES: frozenset[str] = frozenset(
    {
        "delivery_not_ready",
        "waiting_for_portal_data",
        "empty_snapshots",
    }
)

_RETRY_MINUTES = str(int(RETRY_INTERVAL.total_seconds() // 60))


def _issue_id(entry_id: str, status: str) -> str:
    return f"{entry_id}_{status}"


@callback
def async_update_issues(
    hass: HomeAssistant, entry: ConfigEntry, coordinator: EudaCoordinator
) -> None:
    """Create or clear repairs issues based on the integration status sensor."""
    status = coordinator.status_label
    vehicle = entry.data.get(CONF_NICKNAME) or coordinator.vin

    for issue_status in _ISSUE_STATUSES:
        issue_id = _issue_id(entry.entry_id, issue_status)
        if status != issue_status:
            ir.async_delete_issue(hass, DOMAIN, issue_id)
            continue

        placeholders: dict[str, str] = {
            "portal_url": BASE_URL,
            "retry_minutes": _RETRY_MINUTES,
            "vehicle": vehicle,
        }
        if issue_status == "empty_snapshots":
            placeholders["empty_count"] = str(coordinator.empty_snapshot_count)

        severity = (
            ir.IssueSeverity.ERROR
            if issue_status == "delivery_not_ready"
            else ir.IssueSeverity.WARNING
        )

        ir.async_create_issue(
            hass,
            DOMAIN,
            issue_id,
            data={"entry_id": entry.entry_id},
            is_fixable=False,
            issue_domain=DOMAIN,
            learn_more_url=BASE_URL,
            severity=severity,
            translation_key=issue_status,
            translation_placeholders=placeholders,
        )


@callback
def async_clear_issues(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove all portal-state issues when the config entry is unloaded."""
    for status in _ISSUE_STATUSES:
        ir.async_delete_issue(hass, DOMAIN, _issue_id(entry.entry_id, status))
