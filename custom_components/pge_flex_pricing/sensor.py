"""
Home Assistant sensor platform for PGE hourly flex pricing (no authentication required)
Single sensor with parsed hourly prices as attributes.
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
    raw_data = await client.get_hourly_prices(session, circuit_id, now, end)
    # Parse hourly prices from API response
    hourly_prices = []
    prices_by_hour = {}
    try:
        for entry in raw_data.get("prices", []):
            hour = entry.get("hour")
            price = entry.get("price")
            if hour is not None and price is not None:
                hourly_prices.append(price)
                prices_by_hour[f"price_{hour:02}"] = price
    except Exception as e:
        _LOGGER.error(f"Error parsing API response: {e}")
    async_add_entities([PGEFlexPricingSensor(hourly_prices, prices_by_hour, circuit_id)])

class PGEFlexPricingSensor(SensorEntity):
    def __init__(self, hourly_prices, prices_by_hour, circuit_id):
        self._hourly_prices = hourly_prices
        self._prices_by_hour = prices_by_hour
        self._circuit_id = circuit_id
        self._state = hourly_prices[0] if hourly_prices else None
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = f"pge_flex_pricing_{circuit_id}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        attrs = {"circuit_id": self._circuit_id, "hourly_prices": self._hourly_prices}
        attrs.update(self._prices_by_hour)
        return attrs
