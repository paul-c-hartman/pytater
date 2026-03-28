import pytest
import argparse
from nerd_dictation.cli.cancel import main, callback

func_stub = lambda args: args

@pytest.fixture
def setup_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    main(subparsers)
    subparsers.choices['cancel'].set_defaults(func=func_stub)
    return parser

def test_cancel_subcommand_exists(setup_parser):
    args = setup_parser.parse_args(['cancel'])
    assert hasattr(args, 'func')

def test_options_for_cancel(setup_parser):
    pass # No options to test for cancel command.

def test_default_options_for_cancel(setup_parser):
    pass # No options to test for cancel command.

def test_callback(setup_parser):
    pass # Just calls main_cancel which is tested elsewhere