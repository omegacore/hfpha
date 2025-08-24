"""
PGE API client for hourly flex pricing (no authentication required)
Updated to use the working endpoint and parameters.
"""
import requests
from datetime import datetime, timedelta

class PGEFlexPricingClient:
    BASE_URL = "https://pge-pe-api.gridx.com/v1/getPricing"

    def get_hourly_prices(self, circuit_id: str, start: datetime, end: datetime, ratename="EV2A", utility="PGE", market="DAM", program="CalFUSE"):
        params = {
            "utility": utility,
            "market": market,
            "startdate": start.strftime("%Y%m%d"),
            "enddate": end.strftime("%Y%m%d"),
            "ratename": ratename,
            "representativeCircuitId": circuit_id,
            "program": program
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
