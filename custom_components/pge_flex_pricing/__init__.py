"""
Home Assistant integration setup for PGE Flex Pricing with config flow support
"""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import discovery

DOMAIN = "pge_flex_pricing"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.async_create_task(
        discovery.async_load_platform(hass, "sensor", DOMAIN, {}, entry.data)
    )
    return True
