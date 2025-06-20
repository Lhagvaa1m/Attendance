# ==== sheets/employees.py ====
# Employees sheet-тэй холбоотой бүх функцүүд (хайлт, бүртгэл)
from sheets.base import get_sheet
from config import SHEET_URL_EMPLOYEES
from utils.gsheet_cache import get_all_records
import logging

logger = logging.getLogger(__name__)

def find_employee_register_row(register_number):
    # Регистрийн дугаараар ажилтны мэдээллийг хайх
    sheet = get_sheet(SHEET_URL_EMPLOYEES)
    records = sheet.get_all_records()
    for idx, row in enumerate(records):
        if str(row['register_number']) == str(register_number):
            logger.debug("Found employee row for %s", register_number)
            return idx + 2, row
    return None, None

def is_employee_register_number_exists(register_number):
    # Регистрийн дугаар exists эсэхийг шалгах
    sheet = get_sheet(SHEET_URL_EMPLOYEES)
    register_numbers = sheet.col_values(1)[1:]
    return str(register_number) in register_numbers

def register_employee_telegram_id(register_number, telegram_user_id):
    # Telegram ID-г тухайн ажилтанд хадгалах
    sheet = get_sheet(SHEET_URL_EMPLOYEES)
    row_number, row = find_employee_register_row(register_number)
    if row_number:
        sheet.update_cell(row_number, 4, str(telegram_user_id))
        logger.info(
            "Linked telegram id %s to register %s", telegram_user_id, register_number
        )
        return True
    return False


def get_all_employees():
    """Return all employee records from the employees sheet."""
    sheet = get_sheet(SHEET_URL_EMPLOYEES)
    return get_all_records(sheet)
