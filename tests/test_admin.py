import sys
import os
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Provide minimal aiogram stubs so that mybot package can be imported
aiogram_module = types.ModuleType("aiogram")
aiogram_types = types.ModuleType("aiogram.types")
aiogram_types.Message = type("Message", (), {"get_args": lambda self: ""})
aiogram_module.types = aiogram_types
class _Bot:
    def __init__(self, *args, **kwargs):
        pass

class _Dispatcher:
    def __init__(self, *args, **kwargs):
        pass

    def message_handler(self, *args, **kwargs):
        def decorator(func):
            return func
        return decorator

aiogram_module.Bot = _Bot
aiogram_module.Dispatcher = _Dispatcher
fsm_memory = types.ModuleType("aiogram.contrib.fsm_storage.memory")
fsm_memory.MemoryStorage = object
fsm_storage = types.ModuleType("aiogram.contrib.fsm_storage")
fsm_storage.memory = fsm_memory
aiogram_contrib = types.ModuleType("aiogram.contrib")
aiogram_contrib.fsm_storage = fsm_storage
aiogram_module.contrib = aiogram_contrib
sys.modules.setdefault("aiogram", aiogram_module)
sys.modules.setdefault("aiogram.types", aiogram_types)
sys.modules.setdefault("aiogram.contrib", aiogram_contrib)
sys.modules.setdefault("aiogram.contrib.fsm_storage", fsm_storage)
sys.modules.setdefault("aiogram.contrib.fsm_storage.memory", fsm_memory)

# Stub gspread and google-auth to avoid import errors
gspread_module = types.ModuleType("gspread")
gspread_module.client = types.SimpleNamespace(Client=object)
gspread_module.authorize = lambda *a, **k: types.SimpleNamespace(open_by_url=lambda url: types.SimpleNamespace(sheet1=None, worksheet=lambda name: None))
gspread_module.Worksheet = object
sys.modules.setdefault("gspread", gspread_module)
google_module = types.ModuleType("google")
oauth2_module = types.ModuleType("google.oauth2")
service_account_module = types.ModuleType("google.oauth2.service_account")
service_account_module.Credentials = type("Credentials", (), {"from_service_account_file": lambda *a, **k: None})
oauth2_module.service_account = service_account_module
google_module.oauth2 = oauth2_module
sys.modules.setdefault("google", google_module)
sys.modules.setdefault("google.oauth2", oauth2_module)
sys.modules.setdefault("google.oauth2.service_account", service_account_module)

from mybot.handlers.admin import _get_admin_ids, is_admin


def test_get_admin_ids_parsing(monkeypatch):
    monkeypatch.setenv("ADMIN_IDS", "1, 2,3")
    assert _get_admin_ids() == {1, 2, 3}


def test_is_admin(monkeypatch):
    monkeypatch.setenv("ADMIN_IDS", "42")
    assert is_admin(42) is True
    assert is_admin(1) is False
