"""Utility meter helper naming tests."""

from __future__ import annotations

from types import SimpleNamespace

from custom_components.cupra_eu_data_act.const import CONF_NICKNAME, CONF_VIN
from custom_components.cupra_eu_data_act.utility_meter import (
    utility_meter_helper_name,
    utility_meter_helper_object_id,
)


def _entry(vin: str, nickname: str | None = None):
    data = {CONF_VIN: vin}
    if nickname is not None:
        data[CONF_NICKNAME] = nickname
    return SimpleNamespace(data=data)


def test_helper_name_prefers_nickname() -> None:
    entry = _entry("WVWZZZTESTVIN0001", "Born")
    assert (
        utility_meter_helper_name(entry, "Monthly charged energy")
        == "Born Monthly charged energy"
    )


def test_helper_object_id_uses_vin_when_no_nickname() -> None:
    entry = _entry("WVWZZZTESTVIN0001")
    assert (
        utility_meter_helper_object_id(entry, "Monthly mileage")
        == "sensor.wvwzzztestvin0001_monthly_mileage"
    )
