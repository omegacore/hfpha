"""
PGE API client for hourly flex pricing (no authentication required)
"""
import requests
from datetime import datetime, timedelta

class PGEFlexPricingClient:
    BASE_URL = "https://api-calculate.gridx.com/acgd/v1/flex-pricing"

    def get_hourly_prices(self, circuit_id: str, start: datetime, end: datetime):
        params = {
            "circuitId": circuit_id,
            "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
