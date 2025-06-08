import types
import pytest

# Ensure project root on sys.path
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.gsheet_cache as gc


class DummySheet:
    def __init__(self, id_):
        self.id = id_
        self.get_all_records_call_count = 0
        self.records = [{"id": id_}]

    def get_all_records(self):
        self.get_all_records_call_count += 1
        return self.records


class DummyClient:
    def __init__(self, calls):
        self.calls = calls
        self.storage = {}

    def open_by_url(self, url):
        self.calls["open_by_url"] += 1
        if url not in self.storage:
            self.storage[url] = DummySheet(url)
        sheet = self.storage[url]

        def worksheet(name):
            self.calls["worksheet"] += 1
            key = f"{url}:{name}"
            if key not in self.storage:
                self.storage[key] = DummySheet(key)
            return self.storage[key]

        return types.SimpleNamespace(sheet1=sheet, worksheet=worksheet)


def setup_gspread_stubs(monkeypatch):
    calls = {"open_by_url": 0, "worksheet": 0}
    monkeypatch.setattr(gc, "_CACHE", {})
    monkeypatch.setattr(gc.Credentials, "from_service_account_file", lambda *a, **k: None)
    monkeypatch.setattr(gc.gspread, "authorize", lambda creds: DummyClient(calls))
    return calls


def test_get_sheet_caching(monkeypatch):
    calls = setup_gspread_stubs(monkeypatch)
    sheet1 = gc.get_sheet("http://sheet-url")
    sheet2 = gc.get_sheet("http://sheet-url")
    assert sheet1 is sheet2
    assert calls["open_by_url"] == 1


def test_get_worksheet_caching(monkeypatch):
    calls = setup_gspread_stubs(monkeypatch)
    ws1 = gc.get_worksheet("http://sheet-url", "data")
    ws2 = gc.get_worksheet("http://sheet-url", "data")
    assert ws1 is ws2
    assert calls["open_by_url"] == 1
    assert calls["worksheet"] == 1


def test_get_all_records_caching(monkeypatch):
    dummy = DummySheet("42")
    monkeypatch.setattr(gc, "_CACHE", {})
    records1 = gc.get_all_records(dummy)
    records2 = gc.get_all_records(dummy)
    assert records1 is records2
    assert dummy.get_all_records_call_count == 1
