"""This module implements post-processors that can be applied to the text after it is recognized by the speech recognition engine.

Post-processors are functions that take a list of words and return a modified list of words. They can be used to implement features such as capitalizing the first word of a sentence, replacing numbers expressed in English words with their digit representations, and more. Post-processors are registered with a name and a priority, and they are run in order of their priority (lower numbers are run first). Post-processors can also take options, which are passed as a dictionary when the post-processor is run. This allows for flexible configuration of post-processors without needing to hard-code specific features into the post-processor functions themselves.
"""

# Built-in post processors that are always available
import pytater.post_processors.full_sentence
import pytater.post_processors.numbers


# API for registering and running post processors
from pytater.post_processors._load import register_post_processor, process_text, post_processors
