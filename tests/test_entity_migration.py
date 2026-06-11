"""Entity registry translation_key migration tests."""

from __future__ import annotations

from custom_components.cupra_eu_data_act.entity_migration import (
    translation_key_for_unique_id,
)


def test_translation_key_for_curated_sensor() -> None:
    assert (
        translation_key_for_unique_id(
            "WVWZZZTESTVIN0001_battery_state_report.soc", "WVWZZZTESTVIN0001"
        )
        == "battery_state_report_soc"
    )


def test_translation_key_for_enum_sensor() -> None:
    assert (
        translation_key_for_unique_id(
            "WVWZZZTESTVIN0001_charging_state_report.current_charge_state",
            "WVWZZZTESTVIN0001",
        )
        == "charge_state"
    )


def test_translation_key_for_status_sensor() -> None:
    assert (
        translation_key_for_unique_id(
            "WVWZZZTESTVIN0001_integration_status", "WVWZZZTESTVIN0001"
        )
        == "integration_status"
    )


def test_translation_key_unknown_raw_sensor() -> None:
    assert (
        translation_key_for_unique_id(
            "WVWZZZTESTVIN0001_1763a4fe-d8a6-3b8c-b095-70081f3e61c7",
            "WVWZZZTESTVIN0001",
        )
        is None
    )


def test_translation_key_for_curated_binary_sensor() -> None:
    assert (
        translation_key_for_unique_id(
            "WVWZZZTESTVIN0001_locked", "WVWZZZTESTVIN0001"
        )
        == "locked"
    )


def test_translation_key_for_dotted_binary_sensor() -> None:
    assert (
        translation_key_for_unique_id(
            "WVWZZZTESTVIN0001_charge_mode_selection_options.immediate_charging",
            "WVWZZZTESTVIN0001",
        )
        == "charge_mode_selection_options_immediate_charging"
    )


def test_translation_key_for_flat_binary_sensor() -> None:
    assert (
        translation_key_for_unique_id(
            "WVWZZZTESTVIN0001_open_state_front_left_door",
            "WVWZZZTESTVIN0001",
        )
        == "open_state_front_left_door"
    )
