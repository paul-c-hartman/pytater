"""
This file implements an example post-processor that capitalizes every word in the text.
It's meant to be used solely as an example of how to implement a post-processor.
"""

from typing import Any, Optional
from pytater.post_processors import register_post_processor


def capitalize_all_words(words: list[str], options: Optional[dict[str, Any]] = None) -> list[str]:
    """
    Example post-processor that capitalizes every word in the text. For example, `["hello", "world"]` -> `["Hello", "World"]`.
    """
    if options is None:
        options = {}
    for i, word in enumerate(words):
        words[i] = word.capitalize()
    return words


register_post_processor("_example", 10, capitalize_all_words)
