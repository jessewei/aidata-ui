import os

import types
import pytest
from ailib import ailib


class DummyLogger:
    def __init__(self):
        self.debug_called = False
        self.last_msg = None

    def debug(self, msg):
        self.debug_called = True
        self.last_msg = msg


class DummyLoggerModule:
    @staticmethod
    def setup_logger(name, level, format, base_log_folder):
        return DummyLogger()


@pytest.fixture(autouse=True)
def patch_logger(monkeypatch):
    monkeypatch.setattr(ailib, "logger", DummyLoggerModule())


@pytest.fixture(autouse=True)
def patch_cfg_apps(monkeypatch):
    dummy_cfg = {
        "ailib": {
            "logging": {"level": "DEBUG", "format": "%(message)s", "base_log_folder": "/tmp"}
        },
        "application": {
            "version": "1.0.0",
            "description": "Test AI Data Application",
            "list": ["app1", "app2"],
            "include": [
                {"name": "inc1", "cfg_filename": "inc1.cfg"},
                {"name": "inc2", "cfg_filename": "inc2.cfg"},
            ],
        },
    }
    monkeypatch.setattr(ailib, "cfg_apps", dummy_cfg)


def test_is_in_container_true(monkeypatch):
    monkeypatch.setitem(os.environ, "container", "1")
    assert ailib.is_in_container() is True


def test_is_in_container_false(monkeypatch):
    monkeypatch.delenv("container", raising=False)
    assert ailib.is_in_container() is False


def test_aidataapp_init_and_logger():
    app = ailib.AiDataApp("ailib")
    assert app.get_name() == "ailib"
    assert isinstance(app.logger, DummyLogger)
    assert app.logger.debug_called
    assert app.logger.last_msg is not None
    assert "Initializing ailib application" in app.logger.last_msg


def test_get_version():
    app = ailib.AiDataApp("ailib")
    assert app.get_version() == "1.0.0"


def test_get_description():
    app = ailib.AiDataApp("ailib")
    assert app.get_description() == "Test AI Data Application"


def test_get_list():
    app = ailib.AiDataApp("ailib")
    assert app.get_list() == ["app1", "app2"]


def test_get_include():
    app = ailib.AiDataApp("ailib")
    assert isinstance(app.get_include(), list)
    assert app.get_include()[0]["name"] == "inc1"


def test_get_include_name():
    app = ailib.AiDataApp("ailib")
    assert app.get_include_name(1) == "inc2"


def test_get_include_cfg_filename():
    app = ailib.AiDataApp("ailib")
    assert app.get_include_cfg_filename(0) == "inc1.cfg"


def test_get_app_cfg():
    app = ailib.AiDataApp("ailib")
    cfg = app.get_app_cfg()
    assert "logging" in cfg


def test_main_prints_hello(monkeypatch, capsys):
    monkeypatch.setattr(
        ailib, "AiDataApp", lambda name: type("DummyApp", (), {"get_name": lambda self: "ailib"})()
    )
    ailib.main()
    captured = capsys.readouterr()
    assert "Hello from ailib!" in captured.out
