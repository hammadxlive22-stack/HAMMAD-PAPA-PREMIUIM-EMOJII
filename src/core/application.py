from __future__ import annotations

from telegram.ext import Application, ApplicationBuilder

from src.config import config
from src.handlers import bot_profile, callbacks, commands, errors, messages
from src.logger import get_logger, setup_logging

logger = get_logger(__name__)


async def _post_init(application: Application) -> None:
    await bot_profile.setup_bot_profile(application)


def build_application() -> Application:
    setup_logging()

    application = (
        ApplicationBuilder()
        .token(config.bot_token)
        .concurrent_updates(True)
        .post_init(_post_init)
        .build()
    )

    commands.register(application)
    callbacks.register(application)
    messages.register(application)
    application.add_error_handler(errors.on_error)

    return application