"""
Home Assistant integration setup for PGE Flex Pricing with config flow support and HACS compatibility
"""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "pge_flex_pricing"
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    return True
