from unittest.mock import patch

from docopt import docopt

from pytater.cli import begin


def parse_begin(arguments):
    return docopt(begin.__doc__, argv=["begin", *arguments])


def test_begin_defaults():
    arguments = parse_begin([])

    assert arguments["--sample-rate"] == "44100"
    assert arguments["--idle-time"] == "0.1"
    assert arguments["--input"] == "PAREC"
    assert arguments["--output"] == "SIMULATE_INPUT"
    assert arguments["--defer-output"] is False
    assert arguments["--continuous"] is False
    assert arguments["CONFIG_SCRIPT_ARGUMENTS"] == []


def test_begin_parses_options_and_passthrough_arguments():
    arguments = parse_begin(
        [
            "--vosk-model-dir",
            "model",
            "--vosk-grammar-file",
            "grammar.json",
            "--pulse-device-name",
            "default",
            "--sample-rate",
            "16000",
            "--defer-output",
            "--timeout",
            "30",
            "--idle-time",
            "0.75",
            "--numbers-as-digits",
            "--numbers-use-separator",
            "--numbers-min-value",
            "100",
            "--input",
            "SOX",
            "--output",
            "STDOUT",
            "--simulate-input-tool",
            "DOTOOLC",
            "--cookie",
            "/tmp/pytater.cookie",
            "--",
            "config.py",
            "--extension-option",
        ]
    )

    assert arguments["--vosk-model-dir"] == "model"
    assert arguments["--vosk-grammar-file"] == "grammar.json"
    assert arguments["--pulse-device-name"] == "default"
    assert arguments["--sample-rate"] == "16000"
    assert arguments["--defer-output"] is True
    assert arguments["--timeout"] == "30"
    assert arguments["--idle-time"] == "0.75"
    assert arguments["--numbers-as-digits"] is True
    assert arguments["--numbers-use-separator"] is True
    assert arguments["--numbers-min-value"] == "100"
    assert arguments["--input"] == "SOX"
    assert arguments["--output"] == "STDOUT"
    assert arguments["--simulate-input-tool"] == "DOTOOLC"
    assert arguments["--cookie"] == "/tmp/pytater.cookie"
    assert arguments["CONFIG_SCRIPT_ARGUMENTS"] == ["config.py", "--extension-option"]


def test_begin_main_translates_arguments_to_main_begin():
    arguments = parse_begin(
        [
            "--sample-rate",
            "16000",
            "--idle-time",
            "0.75",
            "--defer-output",
            "--output",
            "STDOUT",
            "--cookie",
            "/tmp/pytater.cookie",
            "--",
        ]
    )

    with patch("pytater.cli.begin.main_begin") as main_begin:
        begin.begin_main(arguments)

    main_begin.assert_called_once_with(
        path_to_cookie="/tmp/pytater.cookie",
        vosk_model_dir='""',
        pulse_device_name='""',
        sample_rate=16000,
        input_method="PAREC",
        progressive=False,
        progressive_continuous=False,
        full_sentence=False,
        numbers_as_digits=False,
        numbers_use_separator=False,
        numbers_min_value=10,
        numbers_no_suffix=False,
        timeout=0.0,
        idle_time=0.5,
        delay_exit=0.0,
        punctuate_from_previous_timeout=0.0,
        output="STDOUT",
        simulate_input_tool="XDOTOOL",
        suspend_on_start=False,
        vosk_grammar_file=None,
    )
