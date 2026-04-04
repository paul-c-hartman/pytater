import argparse
import pytest
from pytater.cli._common import argparse_cookie

# pylint: disable=redefined-outer-name,unused-argument


def func_stub(_):
    pass


@pytest.fixture
def setup_parser():
    parser = argparse.ArgumentParser()
    argparse_cookie(parser)
    return parser


def test_argparse_cookie(setup_parser):
    args = setup_parser.parse_args(["--cookie", "path/to/cookie"])
    # Specified manually
    assert args.path_to_cookie == "path/to/cookie"
    # Default value
    args = setup_parser.parse_args([])
    assert args.path_to_cookie == ""
