"""
Home Assistant sensor platform for PGE hourly flex pricing (no authentication required)
Creates a separate sensor for each hour, grouped under one device. Updates once per day.
"""
import logging
from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
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
    session = async_get_clientsession(hass)

    async def _async_update_data():
        try:
            now = datetime.utcnow()
            end = now + timedelta(hours=24)
            raw_data = await client.get_hourly_prices(session, circuit_id, now, end)
            prices = []
            for day in raw_data.get("data", []):
                for entry in day.get("priceDetails", []):
                    price = float(entry.get("intervalPrice"))
                    prices.append(price)
            # Generate ISO timestamps for each hour starting from now
            base = now.replace(minute=0, second=0, microsecond=0)
            times = [(base + timedelta(hours=idx)).isoformat() for idx in range(len(prices))]
            return {"times": times, "prices": prices, "circuit_id": circuit_id}
        except Exception as e:
            raise UpdateFailed(f"Error fetching PGE Flex Pricing data: {e}")

    # Coordinator updates every hour
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="PGE Flex Pricing Data",
        update_method=_async_update_data,
        update_interval=timedelta(hours=1),
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([PGEFlexPricesSensor(coordinator)])

class PGEFlexPricesSensor(SensorEntity):
    def __init__(self, coordinator):
        super().__init__()
        self.coordinator = coordinator
        self._attr_name = "PGE Flex Prices"
        self._attr_unique_id = "pge_flex_prices"

    @property
    def times(self):
        return self.coordinator.data.get("times", []) if self.coordinator.data else []

    @property
    def prices(self):
        return self.coordinator.data.get("prices", []) if self.coordinator.data else []

    @property
    def circuit_id(self):
        return self.coordinator.data.get("circuit_id") if self.coordinator.data else None

    @property
    def state(self):
        # Return the current price based on the current time
        now = dt_util.utcnow()
        idx = None
        for i, t in enumerate(self.times):
            try:
                ts = dt_util.parse_datetime(t)
                if ts > now:
                    break
                idx = i
            except Exception:
                continue
        if idx is not None and idx < len(self.prices):
            return self.prices[idx]
        return None

    @property
    def extra_state_attributes(self):
        return {
            "times": self.times,
            "prices": self.prices,
            "circuit_id": self.circuit_id,
            "last_update": self.times[0] if self.times else None
        }

    async def async_update(self):
        await self.coordinator.async_request_refresh()

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
