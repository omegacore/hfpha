"""
Config flow for PGE Flex Pricing integration
"""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "pge_flex_pricing"

class PGEFlexPricingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            circuit_id = user_input.get("circuit_id")
            if not circuit_id:
                errors["circuit_id"] = "required"
            if not errors:
                return self.async_create_entry(title="PGE Flex Pricing", data={"circuit_id": circuit_id})
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("circuit_id"): str}),
            errors=errors,
        )
