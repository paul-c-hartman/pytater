from nerd_dictation.post_processors import register_post_processor
from typing import Any

def full_sentence(words: list[str], options: dict[str, Any] = {}) -> list[str]:
    words[0] = words[0].capitalize()
    words[-1] = words[-1]
    return words

# Priority 100 for this one since it should run pretty much last.
# Other post-processors may adjust word order and we don't want
# to have words that aren't first being randomly capitalized
register_post_processor("full_sentence", 100, full_sentence)