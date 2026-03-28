import pytest
import argparse
from nerd_dictation.cli.begin import main, callback

func_stub = lambda args: args

@pytest.fixture
def setup_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    main(subparsers)
    subparsers.choices['begin'].set_defaults(func=func_stub)
    return parser

def test_begin_subcommand_exists(setup_parser):
    args = setup_parser.parse_args(['begin'])
    assert hasattr(args, 'func')

def test_options_for_begin(setup_parser):
    args = setup_parser.parse_args(['begin', '--config', 'config.yaml', '--vosk-model-dir', 'model', '--vosk-grammar-file', 'grammar.txt', '--pulse-device-name', 'default', '--sample-rate', '16000', '--defer-output', '--continuous', '--timeout', '30', '--idle-time', '0.1', '--delay-exit', '0.5', '--suspend-on-start', '--punctuate-from-previous-timeout', '1', '--full-sentence', '--numbers-as-digits', '--numbers-use-separator', '--numbers-min-value', '0', '--numbers-no-suffix', '--input', 'SOX', '--output', 'STDOUT', '--simulate-input-tool', 'DOTOOLC', '--verbose', '1'])
    assert args.config == 'config.yaml'
    assert args.vosk_model_dir == 'model'
    assert args.vosk_grammar_file == 'grammar.txt'
    assert args.pulse_device_name == 'default'
    assert args.sample_rate == 16000
    assert args.defer_output is True
    assert args.progressive_continuous is True
    assert args.timeout == 30
    assert args.idle_time == 0.1
    assert args.delay_exit == 0.5
    assert args.suspend_on_start is True
    assert args.punctuate_from_previous_timeout == 1
    assert args.full_sentence is True
    assert args.numbers_as_digits is True
    assert args.numbers_use_separator is True
    assert args.numbers_min_value == 0
    assert args.numbers_no_suffix is True
    assert args.input_method == 'SOX'
    assert args.output == 'STDOUT'
    assert args.simulate_input_tool == 'DOTOOLC'
    assert args.verbose == 1

def test_default_options_for_begin(setup_parser):
    args = setup_parser.parse_args(['begin'])
    assert args.config is None
    assert args.vosk_model_dir is ""
    assert args.vosk_grammar_file is None
    assert args.pulse_device_name is ""
    assert args.sample_rate == 44100
    assert args.defer_output is False
    assert args.progressive_continuous is False
    assert args.timeout == 0.0
    assert args.idle_time == 0.1
    assert args.delay_exit == 0.0
    assert args.suspend_on_start is False
    assert args.punctuate_from_previous_timeout == 0.0
    assert args.full_sentence is False
    assert args.numbers_as_digits is False
    assert args.numbers_use_separator is False
    assert args.numbers_min_value is None
    assert args.numbers_no_suffix is False
    assert args.input_method == 'PAREC'
    assert args.output == 'SIMULATE_INPUT'
    assert args.simulate_input_tool == 'XDOTOOL'
    assert args.verbose == 0
    assert args.rest is False

def test_callback(setup_parser):
    pass # Just calls main_begin which is tested elsewhere