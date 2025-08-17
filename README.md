# PGE Hourly Flex Pricing API Client

## Overview
This project provides a Home Assistant custom integration for retrieving hourly flex pricing data from the PGE API (https://api-calculate-docs.gridx.com/acgd/api-introduction-overview).

## Installation (HACS)
1. Copy the `custom_components/pge_flex_pricing` folder into your Home Assistant `custom_components` directory.
2. In HACS, add this repository as a custom integration (category: Integration).
3. Restart Home Assistant.
4. Go to **Settings > Devices & Services > Add Integration** and search for "PGE Flex Pricing".
5. Enter your circuit ID in the integration setup dialog.

## Features
- Fetches hourly flex prices from PGE API (no authentication required)
- Circuit ID is configured via the Home Assistant UI
- Exposes hourly prices as Home Assistant sensors
- Follows Home Assistant best practices and supports HACS

## Usage
After installation and setup, sensors for each hourly price will be available in Home Assistant. You can use these sensors in automations, dashboards, and more.

## Example (Direct API Usage)
```python
from custom_components.pge_flex_pricing.pge_api import PGEFlexPricingClient
from datetime import datetime, timedelta

circuit_id = "YOUR_CIRCUIT_ID"
client = PGEFlexPricingClient()
now = datetime.utcnow()
end = now + timedelta(hours=24)
prices = client.get_hourly_prices(circuit_id, now, end)
print(prices)
```

## License
MIT
