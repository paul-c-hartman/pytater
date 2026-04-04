"""This file implements an example post-processor that capitalizes every word in the text.

It's meant to be used solely as an example of how to implement a post-processor. Post-processors should implement some function taking a list of words and an optional dictionary of options and return a modified list of words, and then be registered using the `pytater.post_processors.register_post_processor` function with a name and a priority.
"""

from typing import Any, Optional
from pytater.post_processors._load import register_post_processor


def capitalize_all_words(words: list[str], options: Optional[dict[str, Any]] = None) -> list[str]:
    """Example post-processor that capitalizes every word in the text.
    
    For example, `["hello", "world"]` -> `["Hello", "World"]`.

    Args:
        words: The list of words to process.
        options: An optional dictionary of options for the post-processor. This post-processor does not use any options, but the parameter is included for consistency with the post-processor interface.
    
    Returns:
        A new list of words with every word capitalized.
    """
    if options is None:
        options = {}
    for i, word in enumerate(words):
        words[i] = word.capitalize()
    return words


register_post_processor("_example", 10, capitalize_all_words)
