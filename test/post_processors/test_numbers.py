# from pytater.post_processors.numbers import replace_numbers
from pytater.post_processors import process_text


def test_numbers() -> None:
    mappings = {
        "one": "1",
        "five": "5",
        "ten": "10",
        "twenty one": "21",
        "one hundred": "100",
        "one hundred and five": "105",
        "one thousand": "1000",
        "one million": "1000000",
        "one billion": "1000000000",
        "one trillion": "1000000000000",
        "a sentence with words and a number in it: one hundred and five": "a sentence with words and a number in it: 105",
        "one with a suffix: thirty second": "1 with a suffix: 32nd",
        "ensure consecutive numbers don't get merged: one hundred two hundred": "ensure consecutive numbers don't get merged: 100 200",
    }
    for input_text, expected_output in mappings.items():
        assert process_text(input_text, {"numbers": {"enabled": True}}) == expected_output
