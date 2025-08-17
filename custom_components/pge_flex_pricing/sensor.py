"""
Home Assistant sensor platform for PGE hourly flex pricing (no authentication required)
Supports config flow for circuit_id entry via HA GUI.
"""
import logging
from datetime import datetime, timedelta
try:
    from homeassistant.components.sensor import SensorEntity
except ImportError:
    SensorEntity = object  # For linting outside HA
from .pge_api import PGEFlexPricingClient

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "PGE Flex Price"

async def async_setup_entry(hass, config_entry, async_add_entities):
    circuit_id = config_entry.data.get("circuit_id")
    if not circuit_id:
        _LOGGER.error("circuit_id must be set via integration setup")
        return
    client = PGEFlexPricingClient()
    now = datetime.utcnow()
    end = now + timedelta(hours=24)
    prices = client.get_hourly_prices(circuit_id, now, end)
    sensors = [PGEFlexPriceSensor(hour, price, circuit_id) for hour, price in prices.items()]
    async_add_entities(sensors)

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
