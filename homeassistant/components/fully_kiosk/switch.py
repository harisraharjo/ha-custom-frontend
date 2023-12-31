"""Fully Kiosk Browser switch."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from fullykiosk import FullyKiosk

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import FullyKioskDataUpdateCoordinator
from .entity import FullyKioskEntity


@dataclass
class FullySwitchEntityDescriptionMixin:
    """Fully Kiosk Browser switch entity description mixin."""

    on_action: Callable[[FullyKiosk], Any]
    off_action: Callable[[FullyKiosk], Any]
    is_on_fn: Callable[[dict[str, Any]], Any]


@dataclass
class FullySwitchEntityDescription(
    SwitchEntityDescription, FullySwitchEntityDescriptionMixin
):
    """Fully Kiosk Browser switch entity description."""


SWITCHES: tuple[FullySwitchEntityDescription, ...] = (
    FullySwitchEntityDescription(
        key="screensaver",
        translation_key="screensaver",
        on_action=lambda fully: fully.startScreensaver(),
        off_action=lambda fully: fully.stopScreensaver(),
        is_on_fn=lambda data: data.get("isInScreensaver"),
    ),
    FullySwitchEntityDescription(
        key="maintenance",
        translation_key="maintenance",
        entity_category=EntityCategory.CONFIG,
        on_action=lambda fully: fully.enableLockedMode(),
        off_action=lambda fully: fully.disableLockedMode(),
        is_on_fn=lambda data: data.get("maintenanceMode"),
    ),
    FullySwitchEntityDescription(
        key="kiosk",
        translation_key="kiosk",
        entity_category=EntityCategory.CONFIG,
        on_action=lambda fully: fully.lockKiosk(),
        off_action=lambda fully: fully.unlockKiosk(),
        is_on_fn=lambda data: data.get("kioskLocked"),
    ),
    FullySwitchEntityDescription(
        key="motion-detection",
        translation_key="motion_detection",
        entity_category=EntityCategory.CONFIG,
        on_action=lambda fully: fully.enableMotionDetection(),
        off_action=lambda fully: fully.disableMotionDetection(),
        is_on_fn=lambda data: data["settings"].get("motionDetection"),
    ),
    FullySwitchEntityDescription(
        key="screenOn",
        translation_key="screen_on",
        on_action=lambda fully: fully.screenOn(),
        off_action=lambda fully: fully.screenOff(),
        is_on_fn=lambda data: data.get("screenOn"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Fully Kiosk Browser switch."""
    coordinator: FullyKioskDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    async_add_entities(
        FullySwitchEntity(coordinator, description) for description in SWITCHES
    )


class FullySwitchEntity(FullyKioskEntity, SwitchEntity):
    """Fully Kiosk Browser switch entity."""

    entity_description: FullySwitchEntityDescription

    def __init__(
        self,
        coordinator: FullyKioskDataUpdateCoordinator,
        description: FullySwitchEntityDescription,
    ) -> None:
        """Initialize the Fully Kiosk Browser switch entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data['deviceID']}-{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the entity is on."""
        if (is_on := self.entity_description.is_on_fn(self.coordinator.data)) is None:
            return None
        return bool(is_on)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.entity_description.on_action(self.coordinator.fully)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.entity_description.off_action(self.coordinator.fully)
        await self.coordinator.async_refresh()
