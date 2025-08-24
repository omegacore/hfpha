"""
Home Assistant sensor platform for PGE hourly flex pricing (no authentication required)
Single sensor with all hourly prices as attributes.
"""
import logging
from datetime import datetime, timedelta
try:
    from homeassistant.components.sensor import SensorEntity
except ImportError:
    SensorEntity = object  # For linting outside HA
from .pge_api import PGEFlexPricingClient

_LOGGER = logging.getLogger(__name__)

SENSOR_NAME = "PGE Flex Pricing"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    circuit_id = config.get("circuit_id")
    if not circuit_id:
        _LOGGER.error("circuit_id must be set in configuration.yaml")
        return
    client = PGEFlexPricingClient()
    now = datetime.utcnow()
    end = now + timedelta(hours=24)
    prices = client.get_hourly_prices(circuit_id, now, end)
    async_add_entities([PGEFlexPricingSensor(prices, circuit_id)])

class PGEFlexPricingSensor(SensorEntity):
    def __init__(self, prices, circuit_id):
        self._prices = prices
        self._circuit_id = circuit_id
        self._state = prices.get("00") if "00" in prices else next(iter(prices.values()), None)
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = f"pge_flex_pricing_{circuit_id}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        attrs = {"circuit_id": self._circuit_id, "prices": self._prices}
        for hour, price in self._prices.items():
            attrs[f"price_{hour}"] = price
        return attrs
