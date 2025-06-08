"""Admin-related command handlers for the Attendance bot."""

import os
from aiogram import Dispatcher, types
import logging
from config import SHEET_URL_LOCATION, CREDS_FILE, WORKSHEET_NAME
from sheets.base import get_offices_from_sheet
try:  # pragma: no cover - fallback for test stubs
    from aiogram.types import ReplyKeyboardRemove
except Exception:  # pragma: no cover - fallback for tests without this class
    class ReplyKeyboardRemove:  # type: ignore
        def __init__(self, *args, **kwargs) -> None:
            pass

# Parsed list of admin Telegram IDs will be loaded from the environment
ADMIN_IDS: list[int] = []
logger = logging.getLogger(__name__)


def _get_admin_ids() -> set[int]:
    """Return the set of admin IDs from the ``ADMIN_IDS`` environment variable."""
    raw = os.environ.get("ADMIN_IDS", "")
    return {int(part) for part in raw.split(',') if part.strip()}


def is_admin(user_id: int) -> bool:
    """Check if ``user_id`` is listed as an admin."""
    return user_id in _get_admin_ids()


def register_admin_handlers(dp: Dispatcher) -> None:
    """Register admin command handlers with the provided dispatcher."""

    @dp.message_handler(commands=["admin_menu"])
    async def admin_menu(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        text = (
            "Admin commands:\n"
            "/report – Daily attendance report\n"
            "/users – List all registered users\n"
            "/offices – List office locations\n"
            "/add_office – Add a new office\n"
            "/edit_office – Edit office information\n"
            "/remove_office – Remove an office\n"
            "/broadcast – Send a message to all users\n"
            "/alerts – Show alert logs\n"
            "/logs – Last 20 log entries\n"
            "/add_admin – Add new admin\n"
            "/remove_admin – Remove admin\n"
            "/backup – Generate a backup file\n"
            "/settings – Show bot settings"
        )
        await message.answer(text, reply_markup=ReplyKeyboardRemove())

    @dp.message_handler(commands=["report"])
    async def report(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        # TODO: implement report generation
        await message.answer(
            "Daily attendance report not implemented yet.",
            reply_markup=ReplyKeyboardRemove(),
        )

    @dp.message_handler(commands=["users"])
    async def users(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        # TODO: fetch actual user list
        await message.answer(
            "User listing not implemented yet.", reply_markup=ReplyKeyboardRemove()
        )

    @dp.message_handler(commands=["offices"])
    async def offices(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        try:
            offices = get_offices_from_sheet(
                SHEET_URL_LOCATION, CREDS_FILE, WORKSHEET_NAME
            )
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to load offices: %s", exc)
            await message.answer(
                "Could not load offices.", reply_markup=ReplyKeyboardRemove()
            )
            return

        if not offices:
            await message.answer(
                "No offices configured.", reply_markup=ReplyKeyboardRemove()
            )
            return

        lines = ["Offices:"]
        for office in offices:
            name = office.get("name", "?")
            lat = office.get("lat")
            lon = office.get("lon")
            lines.append(f"- {name} ({lat}, {lon})")

        await message.answer("\n".join(lines), reply_markup=ReplyKeyboardRemove())

    @dp.message_handler(commands=["add_office"])
    async def add_office(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Send office name and coordinates to add.",
            reply_markup=ReplyKeyboardRemove(),
        )

    @dp.message_handler(commands=["edit_office"])
    async def edit_office(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Send updated office information.", reply_markup=ReplyKeyboardRemove()
        )

    @dp.message_handler(commands=["remove_office"])
    async def remove_office(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Specify which office to remove.", reply_markup=ReplyKeyboardRemove()
        )

    @dp.message_handler(commands=["broadcast"])
    async def broadcast(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Send a message to broadcast to all users.",
            reply_markup=ReplyKeyboardRemove(),
        )

    @dp.message_handler(commands=["alerts"])
    async def alerts(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Alert logs not available yet.", reply_markup=ReplyKeyboardRemove()
        )

    @dp.message_handler(commands=["logs"])
    async def logs(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Last 20 log entries.", reply_markup=ReplyKeyboardRemove()
        )

    @dp.message_handler(commands=["add_admin"])
    async def add_admin(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Provide Telegram ID to grant admin rights.",
            reply_markup=ReplyKeyboardRemove(),
        )

    @dp.message_handler(commands=["remove_admin"])
    async def remove_admin(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Provide Telegram ID to revoke admin rights.",
            reply_markup=ReplyKeyboardRemove(),
        )

    @dp.message_handler(commands=["backup"])
    async def backup(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Backup feature not implemented yet.",
            reply_markup=ReplyKeyboardRemove(),
        )

    @dp.message_handler(commands=["settings"])
    async def settings(message: types.Message) -> None:
        if not is_admin(message.from_user.id):
            return
        await message.answer(
            "Bot settings are not configurable yet.",
            reply_markup=ReplyKeyboardRemove(),
        )

