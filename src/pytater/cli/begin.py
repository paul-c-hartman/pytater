"""
Usage:
  pytater begin [--vosk-model-dir=<dir>] [--vosk-grammar-file=<file>] [--pulse-device-name=<name>] [--sample-rate=<rate>] [--defer-output | --continuous] [--timeout=<seconds>] [--idle-time=<seconds>] [--delay-exit=<seconds>] [--suspend-on-start] [--punctuate-from-previous-timeout=<seconds>] [--full-sentence] [--numbers-as-digits] [--numbers-use-separator] [--numbers-min-value=<value>] [--numbers-no-suffix] [--input=<input-method>] [--output=<output-method>] [--simulate-input-tool=<tool>] [--cookie=<path>] [--] [CONFIG_SCRIPT_ARGUMENTS...]

Starts the dictation process and begins audio recording. Recognized text is processed and typed in according to the specified options until the dictation process is ended using `pytater end` or suspended using `pytater suspend`. `pytater begin` also accepts various options for configuring the behavior of the dictation process, such as specifying the VOSK model to use, setting timeouts, configuring post-processors, and more.

Options:
  --vosk-model-dir=<dir>       Path to the VOSK model, see: https://alphacephei.com/vosk/models [default: ""]
  --vosk-grammar-file=<file>   Path to a JSON grammar file. This restricts the phrases recognized by VOSK for better accuracy. See `vosk_recognizer_new_grm` in the API reference: https://github.com/alphacep/vosk-api/blob/master/src/vosk_api.h
  --pulse-device-name=<name>   The name of the pulse-audio device to use for recording. See the output of "pactl list sources" to find device names (using the identifier following "Name:") [default: ""]
  --sample-rate=<rate>         The sample rate to use for recording [default: 44100]
  --defer-output               Defer output until the pytater is exited. This prevents text being typed during speech. Implied by `--output=STDOUT`
  --continuous                 Only process current phrase on each update. Enable this option when you intend to keep Pytater running for extended periods of time
  --timeout=<seconds>          End pytater after this many seconds of silence (zero disables) [default: 0]
  --idle-time=<seconds>        Time to idle between processing audio. Set to zero for most responsive behavior at the cost of high CPU usage. Clamped to 0..0.5 [default: 0.1]
  --delay-exit=<seconds>       Delay exit by this many seconds after pytater is requested to exit. This can be useful for push-to-talk setups where the user may want to finish speaking before the program exits (zero disables) [default: 0.0]
  --suspend-on-start           Suspend the agent on start. Use this option to prevent the agent from starting to listen immediately. Use `resume`/`suspend` commands to control the agent after starting.
  --punctuate-from-previous-timeout=<seconds>  Time in seconds recognized as a pause in speech, e.g. to insert punctuation. If the user pauses for this long, the agent will attempt to punctuate the previous phrase if auto-punctuation is enabled (zero disables) [default: 0.0]
  --full-sentence               Capitalize the first letter of each sentence. With `--punctuate-from-previous-timeout`, also adds commas and periods in between phrases.
  --numbers-as-digits           Convert numbers to digits, e.g. "one hundred and twenty three" becomes "123"
  --numbers-use-separator       Use a separator for large numbers, e.g. "one million" becomes "1,000,000"
  --numbers-min-value=<value>   Minimum value for numbers to be converted to digits. Numbers below this value will be left as words. [default: 10]
  --numbers-no-suffix           Do not add suffixes to numbers when `--numbers-as-digits` is enabled, e.g. "first" is unchanged instead of "1st"
  --input=<input-method>       Audio recording method to use. Can be one of: PAREC, SOX, PW-CAT [default: PAREC]
  --output=<output-method>     Text output method to use. Can be one of: SIMULATE_INPUT, STDOUT [default: SIMULATE_INPUT]
  --simulate-input-tool=<tool>  Tool to simulate input for when `--output=SIMULATE_INPUT` is used. Can be one of: XDOTOOL, DOTOOL, DOTOOLC, YDOTOOL, WTYPE, STDOUT [default: XDOTOOL]
  --cookie=<path>              Location for writing a temporary cookie (this file is monitored to begin/end dictation) [default: ""]

  Additional arguments used by configuration scripts, extensions, and other tools can be passed after a `--` separator. These arguments are not interpreted by Pytater itself.

"""

from pytater.cli._common import subcommand_handler
from pytater.main import main_begin


def begin_main(arguments):
    main_begin(
        path_to_cookie=arguments["--cookie"],
        vosk_model_dir=arguments["--vosk-model-dir"],
        pulse_device_name=arguments["--pulse-device-name"],
        sample_rate=int(arguments["--sample-rate"]),
        input_method=arguments["--input"],
        progressive=not (arguments["--defer-output"] or arguments["--output"] == "STDOUT"),
        progressive_continuous=arguments["--continuous"],
        full_sentence=arguments["--full-sentence"],
        numbers_as_digits=arguments["--numbers-as-digits"],
        numbers_use_separator=arguments["--numbers-use-separator"],
        numbers_min_value=int(arguments["--numbers-min-value"]),
        numbers_no_suffix=arguments["--numbers-no-suffix"],
        timeout=float(arguments["--timeout"]),
        idle_time=min(float(arguments["--idle-time"]), 0.5),
        delay_exit=float(arguments["--delay-exit"]),
        punctuate_from_previous_timeout=float(arguments["--punctuate-from-previous-timeout"]),
        output=arguments["--output"],
        simulate_input_tool=arguments["--simulate-input-tool"],
        suspend_on_start=arguments["--suspend-on-start"],
        vosk_grammar_file=arguments["--vosk-grammar-file"],
        # config_script_arguments=arguments["CONFIG_SCRIPT_ARGUMENTS"],
    )


main = subcommand_handler("begin", begin_main)
