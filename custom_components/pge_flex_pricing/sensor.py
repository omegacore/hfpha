"""
Home Assistant sensor platform for PGE hourly flex pricing (no authentication required)
Creates a separate sensor for each hour, grouped under one device. Updates once per day.
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

DEFAULT_NAME = "PGE Flex Price"
DOMAIN = "pge_flex_pricing"

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
    try:
        prices = []
        for day in raw_data.get("data", []):
            for entry in day.get("priceDetails", []):
                price = float(entry.get("intervalPrice"))
                prices.append(price)
        times = [f"{idx:02}" for idx in range(len(prices))]
        entity = PGEFlexPricesSensor(times, prices, circuit_id)
        async_add_entities([entity])
    except Exception as e:
        _LOGGER.error(f"Error parsing API response: {e}")

class PGEFlexPricesSensor(SensorEntity):
    def __init__(self, times, prices, circuit_id):
        self._times = times
        self._prices = prices
        self._circuit_id = circuit_id
        self._attr_name = "PGE Flex Prices"
        self._attr_unique_id = "pge_flex_prices"
        self._attr_state = self._get_state()
        self._attr_extra_state_attributes = {
            "circuit_id": circuit_id,
            "last_update": times[0] if times else None
        }

    def _get_state(self):
        import json
        return json.dumps({"times": self._times, "prices": self._prices})

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def state(self):
        return self._attr_state

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes
