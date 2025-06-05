import time
from typing import Any

import gspread
from google.oauth2.service_account import Credentials

from config import CREDS_FILE, SCOPES

# Basic in-memory cache storage
_CACHE = {}
# Time-to-live for cached items (seconds)
_TTL = 300  # 5 minutes
# Retry configuration
_RETRY_COUNT = 3
_RETRY_DELAY = 1  # seconds


def _with_retry(func):
    """Retry decorator for gspread operations."""

    def wrapper(*args, **kwargs):
        last_exc = None
        for _ in range(_RETRY_COUNT):
            try:
                return func(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                time.sleep(_RETRY_DELAY)
        raise last_exc

    return wrapper


def _authorize() -> gspread.client.Client:
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


@_with_retry
def _open_sheet(url: str) -> gspread.Worksheet:
    client = _authorize()
    return client.open_by_url(url).sheet1


@_with_retry
def _open_worksheet(url: str, worksheet_name: str) -> gspread.Worksheet:
    client = _authorize()
    return client.open_by_url(url).worksheet(worksheet_name)


def get_sheet(url: str) -> gspread.Worksheet:
    """Return a Worksheet object with caching and retry."""
    now = time.time()
    cache_key = f"sheet:{url}"
    if cache_key in _CACHE:
        sheet, ts = _CACHE[cache_key]
        if now - ts < _TTL:
            return sheet
    sheet = _open_sheet(url)
    _CACHE[cache_key] = (sheet, now)
    return sheet


def get_worksheet(url: str, worksheet_name: str) -> gspread.Worksheet:
    """Return a specific worksheet with caching and retry."""
    now = time.time()
    cache_key = f"sheet:{url}:{worksheet_name}"
    if cache_key in _CACHE:
        sheet, ts = _CACHE[cache_key]
        if now - ts < _TTL:
            return sheet
    sheet = _open_worksheet(url, worksheet_name)
    _CACHE[cache_key] = (sheet, now)
    return sheet


@_with_retry
def get_all_records(sheet: gspread.Worksheet) -> list[dict[str, Any]]:
    """Return all records from a sheet using caching."""
    now = time.time()
    cache_key = f"records:{sheet.id}"
    if cache_key in _CACHE:
        records, ts = _CACHE[cache_key]
        if now - ts < _TTL:
            return records
    records = sheet.get_all_records()
    _CACHE[cache_key] = (records, now)
    return records
