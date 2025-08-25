"""
PGE API client for hourly flex pricing (no authentication required)
Async implementation for Home Assistant compatibility.
"""
import aiohttp

class PGEFlexPricingClient:
    BASE_URL = "https://pge-pe-api.gridx.com/v1/getPricing"

    async def get_hourly_prices(self, session, circuit_id, start, end, ratename="EV2A", utility="PGE", market="DAM", program="CalFUSE"):
        params = {
            "utility": utility,
            "market": market,
            "startdate": start.strftime("%Y%m%d"),
            "enddate": end.strftime("%Y%m%d"),
            "ratename": ratename,
            "representativeCircuitId": circuit_id,
            "program": program
        }
        async with session.get(self.BASE_URL, params=params) as response:
            response.raise_for_status()
            return await response.json()
