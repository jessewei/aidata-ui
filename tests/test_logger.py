import os
import logging
import shutil
from pathlib import Path
import pytest
from ailib import logger as logger_mod
from loguru._defaults import LOGURU_FORMAT
from loguru import logger as loguru_logger
from loguru import logger as loguru_logger


def test_setup_logger_creates_log_file(tmp_path, monkeypatch):
    # Patch cfg_apps to avoid dependency on external config
    monkeypatch.setattr(logger_mod, "cfg_apps", {})
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    log_name = "testapp"
    log_file = log_dir / f"{log_name}.log"

    logger = logger_mod.setup_logger(name=log_name, base_log_folder=str(log_dir))
    logger.info("Test log message")

    logger.handlers[0].flush()
    assert log_file.exists()
    with open(log_file, "r") as f:
        content = f.read()
    assert "Test log message" in content


def test_setup_logger_returns_same_logger(monkeypatch, tmp_path):
    monkeypatch.setattr(logger_mod, "cfg_apps", {})
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    log_name = "testapp2"

    logger1 = logger_mod.setup_logger(name=log_name, base_log_folder=str(log_dir))
    logger2 = logger_mod.setup_logger(name=log_name, base_log_folder=str(log_dir))
    assert logger1 is logger2


def test_log_flow_decorator(monkeypatch, caplog, tmp_path):
    monkeypatch.setattr(logger_mod, "cfg_apps", {})
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    log_name = "decorator_test"

    @logger_mod.log_flow(logger_name=log_name)
    def dummy_func(x, y):
        return x + y

    with caplog.at_level(logging.DEBUG):
        result = dummy_func(2, 3)
    assert result == 5
    assert any("FLOW: Entering: dummy_func" in m for m in caplog.messages)
    assert any("FLOW: Exiting: dummy_func" in m for m in caplog.messages)


# def test_format_record_payload(monkeypatch):
#     record = {
#         "extra": {"payload": {"foo": [1, 2, 3]}},
#         "exception": "",
#     }
#     formatted = logger_mod.format_record(record)
#     assert "foo" in formatted
#     assert "<level>" in formatted


def test_intercept_handler_logs(monkeypatch, capsys):
    # Patch loguru logger to print to stdout for test
    loguru_logger.remove()
    loguru_logger.add(lambda msg: print(msg, end=""), format="{message}")

    handler = logger_mod.InterceptHandler()
    log_record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Intercepted message",
        args=(),
        exc_info=None,
    )
    handler.emit(log_record)
    captured = capsys.readouterr()
    assert "Intercepted message" in captured.out


def test_init_logging(monkeypatch):
    # Patch loguru logger to avoid side effects
    loguru_logger.remove()
    loguru_logger.add(lambda msg: None)
    # Patch sys.stdout to avoid actual output
    monkeypatch.setattr(logger_mod.sys, "stdout", open(os.devnull, "w"))
    # Should not raise
    logger_mod.init_logging()
