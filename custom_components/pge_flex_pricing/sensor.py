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
    sensors = []
    try:
        # Parse the correct structure from the sample response
        for day in raw_data.get("data", []):
            for idx, entry in enumerate(day.get("priceDetails", [])):
                hour = idx
                price = float(entry.get("intervalPrice"))
                sensors.append(PGEFlexPriceSensor(hour, price, circuit_id, config_entry.entry_id))
    except Exception as e:
        _LOGGER.error(f"Error parsing API response: {e}")
    async_add_entities(sensors)

class PGEFlexPriceSensor(SensorEntity):
    def __init__(self, hour, price, circuit_id, entry_id):
        self._hour = hour
        self._price = price
        self._state = price
        self._attr_name = f"{DEFAULT_NAME} {hour:02}"
        self._attr_unique_id = f"pge_flex_price_{circuit_id}_{hour:02}"
        self._attr_extra_state_attributes = {"hour": self._hour, "price": self._price, "circuit_id": circuit_id}
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "PGE Flex Pricing",
            "manufacturer": "PG&E",
            "model": "Hourly Flex Pricing"
        }

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes
