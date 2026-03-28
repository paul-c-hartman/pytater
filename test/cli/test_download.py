import pytest
import argparse
from nerd_dictation.cli.download import main, callback

func_stub = lambda args: args

@pytest.fixture
def setup_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    main(subparsers)
    subparsers.choices['download'].set_defaults(func=func_stub)
    return parser

def test_download_subcommand_exists(setup_parser):
    args = setup_parser.parse_args(['download'])
    assert hasattr(args, 'func')

def test_options_for_download(setup_parser):
    args = setup_parser.parse_args(['download', '--model', 'large', '--force', '-y'])
    assert args.model == 'large'
    assert args.force is True
    assert args.confirmation is True

def test_default_options_for_download(setup_parser):
    args = setup_parser.parse_args(['download'])
    assert args.model == 'small'
    assert args.force is False
    assert args.confirmation is False

def test_callback(setup_parser):
    pass # Just calls main_download which is tested elsewhere