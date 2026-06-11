"""Service handler tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import ServiceCall
from homeassistant.exceptions import ServiceValidationError
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.cupra_eu_data_act.const import CONF_IDENTIFIER, CONF_VIN, DOMAIN
from custom_components.cupra_eu_data_act.services import (
    SERVICE_REFRESH_NOW,
    _async_handle_refresh_now,
    _entries_for_call,
    async_setup_services,
)


def _mock_entry(hass, entry_id: str = "test-entry") -> MockConfigEntry:
    entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id=entry_id,
        data={CONF_VIN: "WVWZZZTESTVIN0001", CONF_IDENTIFIER: "ident-1"},
        unique_id="WVWZZZTESTVIN0001",
    )
    entry.add_to_hass(hass)
    coordinator = MagicMock()
    coordinator.async_refresh = AsyncMock()
    entry.runtime_data = MagicMock(coordinator=coordinator)
    return entry


def test_entries_for_call_all(hass) -> None:
    entry = _mock_entry(hass)
    call = ServiceCall(hass, DOMAIN, SERVICE_REFRESH_NOW, {})
    assert _entries_for_call(hass, call) == [entry]


def test_entries_for_call_specific(hass) -> None:
    _mock_entry(hass, "entry-a")
    entry_b = _mock_entry(hass, "entry-b")
    call = ServiceCall(
        hass, DOMAIN, SERVICE_REFRESH_NOW, {"config_entry": "entry-b"}
    )
    assert _entries_for_call(hass, call) == [entry_b]


def test_entries_for_call_unknown_entry(hass) -> None:
    call = ServiceCall(
        hass, DOMAIN, SERVICE_REFRESH_NOW, {"config_entry": "missing"}
    )
    with pytest.raises(ServiceValidationError):
        _entries_for_call(hass, call)


async def test_refresh_now_calls_coordinator(hass) -> None:
    async_setup_services(hass)
    entry = _mock_entry(hass)
    call = ServiceCall(hass, DOMAIN, SERVICE_REFRESH_NOW, {})

    await _async_handle_refresh_now(hass, call)

    entry.runtime_data.coordinator.async_refresh.assert_awaited_once()
