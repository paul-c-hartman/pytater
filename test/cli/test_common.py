import pytest

from pytater.cli._common import subcommand_handler


def test_subcommand_handler_calls_handler():
    arguments = {"value": "test"}
    calls = []

    def handler(received_arguments):
        calls.append(received_arguments)

    subcommand_handler("test", handler)(arguments)

    assert calls == [arguments]


def test_subcommand_handler_exits_with_handler_return_code():
    with pytest.raises(SystemExit) as error:
        subcommand_handler("test", lambda _: 7)({})

    assert error.value.code == 7


def test_subcommand_handler_does_not_exit_when_handler_returns_none():
    subcommand_handler("test", lambda _: None)({})
