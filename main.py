# ==== main.py ====
# Ботын ажиллуулалт
from aiogram import executor
from mybot import dp
import mybot.handlers.user
import mybot.handlers.menu
from mybot.handlers.admin import register_admin_handlers
from utils.logging_config import setup_logging
import logging


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting bot polling")
    register_admin_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
