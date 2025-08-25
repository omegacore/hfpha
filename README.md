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

## How it works
- The integration creates one device with 24 sensor entities, each representing the price for a specific hour.
- Sensors are named `sensor.pge_flex_price_00`, `sensor.pge_flex_price_01`, ..., `sensor.pge_flex_price_23`.
- Each sensor has attributes for the hour, price, and circuit ID.
- Prices are updated once per day from the PGE API.

## Example: Lovelace Entities Card
To display all hourly prices in your dashboard:

```yaml
- type: entities
  title: PGE Hourly Flex Prices
  entities:
    - entity: sensor.pge_flex_price_00
    - entity: sensor.pge_flex_price_01
    - entity: sensor.pge_flex_price_02
    # ... add all sensors up to sensor.pge_flex_price_23
```

## Example: Lovelace Bar Chart for Hourly Prices
To display the hourly flex prices as a timeseries bar chart, use the [apexcharts-card](https://github.com/RomRider/apexcharts-card) with a column type and a data generator. Here’s the updated YAML example for a single sensor with separate times and prices keys:

```yaml
- type: custom:apexcharts-card
  apex_config:
    chart:
      type: column
  header:
    show: true
    title: PGE Hourly Flex Prices
  series:
    - entity: sensor.pge_flex_prices
      name: "Hourly Prices"
      data_generator: |
        const times = attributes['sensor.pge_flex_prices'].times;
        const prices = attributes['sensor.pge_flex_prices'].prices;
        return times.map((t, i) => ({ x: t, y: prices[i] }));
```

This approach uses a single sensor whose attributes include two arrays: `times` (ISO timestamps) and `prices` (hourly price values). The data generator reads these attributes and returns timeseries data for the chart.

## Automation
You can use the hourly sensors in automations to trigger actions based on price changes.

## License
MIT
