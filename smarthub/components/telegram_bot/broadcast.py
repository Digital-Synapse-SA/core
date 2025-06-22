"""Support for Telegram bot to send messages only."""

from telegram import Bot

from smarthub.core import SmartHub

from .bot import BaseTelegramBot, TelegramBotConfigEntry


async def async_setup_platform(
    hass: SmartHub, bot: Bot, config: TelegramBotConfigEntry
) -> type[BaseTelegramBot] | None:
    """Set up the Telegram broadcast platform."""
    return None
