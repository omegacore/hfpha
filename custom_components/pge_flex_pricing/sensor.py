"""
Home Assistant sensor platform for PGE hourly flex pricing (no authentication required)
Supports config flow for circuit_id entry via HA GUI.
HACS compatibility: Only define the PGEFlexPriceSensor class here.
"""
import logging
try:
    from homeassistant.components.sensor import SensorEntity
except ImportError:
    SensorEntity = object  # For linting outside HA

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "PGE Flex Price"

class PGEFlexPriceSensor(SensorEntity):
    def __init__(self, hour, price, circuit_id):
        self._hour = hour
        self._price = price
        self._state = price
        self._attr_name = f"{DEFAULT_NAME} {hour}"
        self._attr_unique_id = f"pge_flex_price_{circuit_id}_{hour}"
        self._attr_extra_state_attributes = {"hour": self._hour, "price": self._price, "circuit_id": circuit_id}

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes
