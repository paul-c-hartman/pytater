from typing import Any, List, Dict
import pytest
from pytater.post_processors import post_processors, register_post_processor, process_text
from pytater.post_processors.full_sentence import full_sentence

# pylint: disable=redefined-outer-name,unused-argument


def reverse_words(words: List[str], _options: Dict[str, Any]) -> List[str]:
    return words[::-1]


test_words = "test words"


@pytest.fixture
def cleared_processors():
    original_processors = post_processors.copy()
    post_processors.clear()
    yield
    post_processors[:] = original_processors


def test_register_post_processor() -> None:
    original_length = len(post_processors)
    post_processor = ("dummy", 10, reverse_words)
    register_post_processor(*post_processor)
    assert post_processor in post_processors
    assert len(post_processors) - original_length == 1
    assert process_text(test_words, options={"dummy": {"enabled": True}}) == "words test"


def test_load_post_processor(cleared_processors) -> None:
    post_processors[:] = [("full_sentence", 100, full_sentence)]
    assert len(post_processors) == 1
    assert process_text(test_words, options={"full_sentence": {"enabled": True}}) == "Test words"


def test_process_text_with_no_processors() -> None:
    assert process_text(test_words) == test_words


def test_process_text_with_processors() -> None:
    register_post_processor("reverse", 10, reverse_words)
    assert process_text(test_words, options={"reverse": {"enabled": True}}) == "words test"
    assert (
        process_text(test_words, options={"reverse": {"enabled": True}, "full_sentence": {"enabled": True}})
        == "Words test"
    )
