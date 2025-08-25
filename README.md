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

## Example: Lovelace Dashboard Card
To display the hourly flex prices in your Home Assistant dashboard, add a card like this to your Lovelace UI:

```yaml
- type: entities
  title: PGE Hourly Flex Prices
  entities:
    - entity: sensor.pge_flex_price_00  # Replace with your actual entity names
    - entity: sensor.pge_flex_price_01
    - entity: sensor.pge_flex_price_02
    # ...add more hourly sensors as needed
```

Or use a custom card for a more visual display:

```yaml
- type: custom:mini-graph-card
  name: PGE Flex Prices
  entities:
    - sensor.pge_flex_price_00
    - sensor.pge_flex_price_01
    - sensor.pge_flex_price_02
    # ...add more hourly sensors as needed
  show_legend: true
  hours_to_show: 24
  points_per_hour: 1
```

Adjust the entity names to match those created by your integration (e.g., `sensor.pge_flex_price_00`, `sensor.pge_flex_price_01`, etc.).

## Example: Lovelace Dashboard Card (Single Sensor)
To display the hourly flex prices in your Home Assistant dashboard, add a card like this to your Lovelace UI:

```yaml
- type: entities
  title: PGE Hourly Flex Pricing
  entities:
    - entity: sensor.pge_flex_pricing
```

To show individual hourly prices, use the sensor's attributes in a template or custom card. For example:

```yaml
- type: custom:template-entity-row
  entity: sensor.pge_flex_pricing
  name: Price for 14:00
  state: "{{ state_attr('sensor.pge_flex_pricing', 'price_14') }}"
```

Or use a custom card to graph the hourly prices:

```yaml
- type: custom:mini-graph-card
  name: PGE Flex Prices
  entities:
    - sensor.pge_flex_pricing
  attribute: prices
  show_legend: true
  hours_to_show: 24
  points_per_hour: 1
```

Adjust the attribute references to match your needs. The sensor exposes all hourly prices as attributes for easy access.

## Example: Lovelace Bar Chart for Hourly Prices
To display the hourly flex prices as a bar chart in your Home Assistant dashboard, use the [custom:plotly-graph-card](https://github.com/dccsillag/home-assistant-plotly-graph-card) or [custom:apexcharts-card](https://github.com/RomRider/apexcharts-card). Here’s an example using apexcharts-card:

```yaml
- type: custom:apexcharts-card
  header:
    show: true
    title: PGE Hourly Flex Prices
  chart_type: bar
  series:
    - entity: sensor.pge_flex_pricing
      attribute: hourly_prices
      name: Hourly Price
      type: column
      data_generator: |
        return entity.attributes.hourly_prices.map((price, idx) => {
          return [idx, price];
        });
  xaxis:
    categories:
      - "00" - "01" - "02" - "03" - "04" - "05" - "06" - "07" - "08" - "09" - "10" - "11" - "12" - "13" - "14" - "15" - "16" - "17" - "18" - "19" - "20" - "21" - "22" - "23"
```

This will show a bar for each hour using the `hourly_prices` attribute from your sensor. Make sure you have the apexcharts-card installed via HACS.

## License
MIT
