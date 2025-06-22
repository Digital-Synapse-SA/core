"""Config flow for Locative."""

from smarthub.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_webhook_flow(
    DOMAIN,
    "Locative Webhook",
    {"docs_url": "https://www.smart-hub.io/integrations/locative/"},
)
