from nerd_dictation.post_processors import process_text

import nerd_dictation.post_processors.full_sentence

def test_full_sentence() -> None:
    mappings = {
        "test sentence": "Test sentence",
        "test sentence.": "Test sentence.",
        "a much longer sentence with multiple words and no punctuation": "A much longer sentence with multiple words and no punctuation",
        "a much longer sentence with multiple words and punctuation!": "A much longer sentence with multiple words and punctuation!",
    }
    for input_text, expected_output in mappings.items():
        assert process_text(input_text, options={"full_sentence": {"enabled": True}}) == expected_output