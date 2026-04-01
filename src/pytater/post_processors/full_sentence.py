from typing import Any, Optional
from pytater.post_processors import register_post_processor


def full_sentence(words: list[str], options: Optional[dict[str, Any]] = None) -> list[str]:
    """
    Post-processor that capitalizes the first word of a sentence and leaves the rest of the words unchanged. For example, `["hello", "world"]` -> `["Hello", "world"]`.
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
