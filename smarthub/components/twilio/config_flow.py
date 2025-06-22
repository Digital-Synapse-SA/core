"""Config flow for Twilio."""

from smarthub.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_webhook_flow(
    DOMAIN,
    "Twilio Webhook",
    {
        "twilio_url": "https://www.twilio.com/docs/glossary/what-is-a-webhook",
        "docs_url": "https://www.smart-hub.io/integrations/twilio/",
    },
)
