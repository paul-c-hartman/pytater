"""This module provides a post-processor for capitalizing the first word of a sentence while leaving the rest of the words unchanged.

For example, `["hello", "world"]` -> `["Hello", "world"]`. The `full_sentence` post-processor has a priority of 100, meaning it should run after most other post-processors. This is to ensure that other post-processors that may adjust word order do not cause words that aren't first to be capitalized.
"""

from typing import Any, Optional
from pytater.post_processors import register_post_processor


def full_sentence(words: list[str], options: Optional[dict[str, Any]] = None) -> list[str]:
    """Post-processor that capitalizes the first word of a sentence and leaves the rest of the words unchanged.
    
    For example, `["hello", "world"]` -> `["Hello", "world"]`.

    Args:
        words: The list of words to process.
        options: An optional dictionary of options for the post-processor. This post-processor does not use any options, but the parameter is included for consistency with the post-processor interface.

    Returns:
        A new list of words with the first word capitalized and the rest unchanged.
    """
    if options is None:
        options = {}
    words[0] = words[0].capitalize()
    words[-1] = words[-1]
    return words


# Priority 100 for this one since it should run pretty much last.
# Other post-processors may adjust word order and we don't want
# to have words that aren't first being randomly capitalized
register_post_processor("full_sentence", 100, full_sentence)
