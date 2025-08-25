"""
Home Assistant sensor platform for PGE hourly flex pricing (no authentication required)
Single sensor with all hourly prices as attributes. Uses config entry data for circuit_id.
Async API call for Home Assistant compatibility.
"""
import logging
from datetime import datetime, timedelta
try:
    from homeassistant.components.sensor import SensorEntity
    from homeassistant.helpers.aiohttp_client import async_get_clientsession
except ImportError:
    SensorEntity = object  # For linting outside HA
from .pge_api import PGEFlexPricingClient

_LOGGER = logging.getLogger(__name__)

SENSOR_NAME = "PGE Flex Pricing"

async def async_setup_entry(hass, config_entry, async_add_entities):
    circuit_id = config_entry.data.get("circuit_id")
    if not circuit_id:
        _LOGGER.error("circuit_id must be set via integration setup")
        return
    client = PGEFlexPricingClient()
    now = datetime.utcnow()
    end = now + timedelta(hours=24)
    session = async_get_clientsession(hass)
    prices = await client.get_hourly_prices(session, circuit_id, now, end)
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
