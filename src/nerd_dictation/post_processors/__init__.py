import sys
from typing import Any, Callable, Optional

post_processors = []


def register_post_processor(
    name: str, priority: int, post_process_fn: Callable[[list[str], dict[str, Any]], list[str]]
) -> None:
    """
    Register a post processor function that will be called to process the text after it is recognized.
     - name: The name of the post processor, used for configuration and debugging.
     - priority: The priority of the post processor, lower numbers will be run first.
     - post_process_fn: The function that will be called to process the text.
    """
    post_processors.append((name, priority, post_process_fn))


# Built-in post processors that are always available
import nerd_dictation.post_processors.full_sentence
import nerd_dictation.post_processors.numbers


def process_text(
    text: str,
    options: Optional[dict[str, dict[str, Any]]] = None,
    # full_sentence: bool = False, # options['full_sentence']['enabled']: bool
    # numbers_as_digits: bool = False, # options['numbers']['as_digits']: bool
    # numbers_use_separator: bool = False, # options['numbers']['use_separator']: bool
    # numbers_min_value: Optional[int] = None, # options['numbers']['min_value']: Optional[int]
    # numbers_no_suffix: bool = False, # options['numbers']['no_suffix']: bool
) -> str:
    """
    Process the text with all registered post processors.
    """

    if options is None:
        options = {}

    # Make absolutely sure we never add new lines in text that is typed in.
    # As this will press the return key when using automated key input.
    text = text.replace("\n", " ")
    words = text.split(" ")

    # Handle post processors that are registered by user configuration.
    for name, _priority, post_process_fn in sorted(post_processors, key=lambda x: x[1]):
        try:
            processor_options = options.get(name, {})
            if processor_options.get("enabled", False):
                print(f"Running post processor {name!r} with options {processor_options!r}")
                words = post_process_fn(words, processor_options)
            else:
                print(f"Skipping post processor {name!r} as it is not enabled")
        except Exception as ex:
            sys.stderr.write(f"Failed to run post processor {name!r} with error {str(ex)}\n")
            sys.exit(1)

    # Optional?
    # if options.get("full_sentence", {}).get("enabled"):
    #     words[0] = words[0].capitalize()
    #     # words[-1] = words[-1]

    return " ".join(words)
