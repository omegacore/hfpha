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
    prices = []
    try:
        for day in raw_data.get("data", []):
            for entry in day.get("priceDetails", []):
                price = float(entry.get("intervalPrice"))
                prices.append(price)
    except Exception as e:
        _LOGGER.error(f"Error parsing API response: {e}")
        return
    # Generate ISO timestamps for each hour starting from now
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    times = [(now + timedelta(hours=idx)).isoformat() for idx in range(len(prices))]
    entity = PGEFlexPricesSensor(times, prices, circuit_id)
    async_add_entities([entity])

class PGEFlexPricesSensor(SensorEntity):
    def __init__(self, times, prices, circuit_id):
        self._times = times
        self._prices = prices
        self._circuit_id = circuit_id
        self._attr_name = "PGE Flex Prices"
        self._attr_unique_id = "pge_flex_prices"
        self._attr_state = self._get_current_price()
        self._attr_extra_state_attributes = {
            "times": times,
            "prices": prices,
            "circuit_id": circuit_id,
            "last_update": times[0] if times else None
        }

    def _get_current_price(self):
        from datetime import datetime
        now = datetime.utcnow()
        # Find the index of the closest time not after now
        idx = None
        for i, t in enumerate(self._times):
            try:
                ts = datetime.fromisoformat(t)
                if ts > now:
                    break
                idx = i
            except Exception:
                continue
        if idx is not None and idx < len(self._prices):
            return self._prices[idx]
        return None

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
