"""This module provides a post-processor for converting numbers expressed in English words into digits.

For example, "two hundred and fifty six" -> "256". The `numbers` post-processor has a priority of 10.
"""

from typing import Tuple, Dict, Set, List, Optional, Any
from pytater.post_processors import register_post_processor


def from_words_to_digits_setup_once() -> (
    Tuple[Dict[str, Tuple[int, int, str, bool]], Set[str], Set[str], Set[str], Set[str]]
):
    """One-time setup for the numbers post-processor.
    
    Initializes the mapping of number words to their numeric values and other related sets for validation.

    Returns:
        A tuple containing:
        - A dictionary mapping number words to a tuple of (scale, increment, suffix, is_final).
        - A set of valid digit words that can be used to start numeric expressions.
        - A set of valid unit words (e.g. "one", "twenty").
        - A set of valid scale words (e.g. "hundred", "thousand").
        - A set of valid zero words (e.g. "zero").
    """
    number_words = {}
    # A set of words that can be used to start numeric expressions.
    valid_digit_words: Set[str] = set()

    # Singles.
    units = (
        (("zero", ""), ("zeroes", "'s"), ("zeroth", "th")),
        (("one", ""), ("ones", "'s"), ("first", "st")),
        (("two", ""), ("twos", "'s"), ("second", "nd")),
        (("three", ""), ("threes", "'s"), ("third", "rd")),
        (("four", ""), ("fours", "'s"), ("fourth", "th")),
        (("five", ""), ("fives", "'s"), ("fifth", "th")),
        (("six", ""), ("sixes", "'s"), ("sixth", "th")),
        (("seven", ""), ("sevens", "'s"), ("seventh", "th")),
        (("eight", ""), ("eights", "'s"), ("eighth", "th")),
        (("nine", ""), ("nines", "'s"), ("ninth", "th")),
        (("ten", ""), ("tens", "'s"), ("tenth", "th")),
        (("eleven", ""), ("elevens", "'s"), ("eleventh", "th")),
        (("twelve", ""), ("twelves", "'s"), ("twelfth", "th")),
        (("thirteen", ""), ("thirteens", "'s"), ("thirteenth", "th")),
        (("fourteen", ""), ("fourteens", "'s"), ("fourteenth", "th")),
        (("fifteen", ""), ("fifteens", "'s"), ("fifteenth", "th")),
        (("sixteen", ""), ("sixteens", "'s"), ("sixteenth", "th")),
        (("seventeen", ""), ("seventeens", "'s"), ("seventeenth", "th")),
        (("eighteen", ""), ("eighteens", "'s"), ("eighteenth", "th")),
        (("nineteen", ""), ("nineteens", "'s"), ("nineteenth", "th")),
    )

    # Tens.
    units_tens = (
        (("", ""), ("", ""), ("", "")),
        (("", ""), ("", ""), ("", "")),
        (("twenty", ""), ("twenties", "'s"), ("twentieth", "th")),
        (("thirty", ""), ("thirties", "'s"), ("thirtieth", "th")),
        (("forty", ""), ("forties", "'s"), ("fortieth", "th")),
        (("fifty", ""), ("fifties", "'s"), ("fiftieth", "th")),
        (("sixty", ""), ("sixties", "'s"), ("sixtieth", "th")),
        (("seventy", ""), ("seventies", "'s"), ("seventieth", "th")),
        (("eighty", ""), ("eighties", "'s"), ("eightieth", "th")),
        (("ninety", ""), ("nineties", "'s"), ("ninetieth", "th")),
    )

    # Larger scales.
    scales = (
        ((("hundred", ""), ("hundreds", "s"), ("hundredth", "th")), 2),
        ((("thousand", ""), ("thousands", "s"), ("thousandth", "th")), 3),
        ((("million", ""), ("millions", "s"), ("millionth", "th")), 6),
        ((("billion", ""), ("billions", "s"), ("billionth", "th")), 9),
        ((("trillion", ""), ("trillions", "s"), ("trillionth", "th")), 12),
        ((("quadrillion", ""), ("quadrillions", "s"), ("quadrillionth", "th")), 15),
        ((("quintillion", ""), ("quintillions", "s"), ("quintillionth", "th")), 18),
        ((("sextillion", ""), ("sextillions", "s"), ("sextillionth", "th")), 21),
        ((("septillion", ""), ("septillions", "s"), ("septillionth", "th")), 24),
        ((("octillion", ""), ("octillions", "s"), ("octillionth", "th")), 27),
        ((("nonillion", ""), ("nonillions", "s"), ("nonillionth", "th")), 30),
        ((("decillion", ""), ("decillions", "s"), ("decillionth", "th")), 33),
        ((("undecillion", ""), ("undecillions", "s"), ("undecillionth", "th")), 36),
        ((("duodecillion", ""), ("duodecillions", "s"), ("duodecillionth", "th")), 39),
        ((("tredecillion", ""), ("tredecillions", "s"), ("tredecillionth", "th")), 42),
        ((("quattuordecillion", ""), ("quattuordecillions", "s"), ("quattuordecillionth", "th")), 45),
        ((("quindecillion", ""), ("quindecillions", "s"), ("quindecillionth", "th")), 48),
        ((("sexdecillion", ""), ("sexdecillions", "s"), ("sexdecillionth", "th")), 51),
        ((("septendecillion", ""), ("septendecillions", "s"), ("septendecillionth", "th")), 54),
        ((("octodecillion", ""), ("octodecillions", "s"), ("octodecillionth", "th")), 57),
        ((("novemdecillion", ""), ("novemdecillions", "s"), ("novemdecillionth", "th")), 60),
        ((("vigintillion", ""), ("vigintillions", "s"), ("vigintillionth", "th")), 63),
        ((("centillion", ""), ("centillions", "s"), ("centillionth", "th")), 303),
    )

    # Divisors (not final).
    number_words["and"] = (1, 0, "", False)

    # Perform our loops and start the swap.
    for idx, word_pairs in enumerate(units):
        for word, suffix in word_pairs:
            number_words[word] = (1, idx, suffix, True)
    for idx, word_pairs in enumerate(units_tens):
        for word, suffix in word_pairs:
            number_words[word] = (1, idx * 10, suffix, True)
    for word_pairs, power in scales:
        for word, suffix in word_pairs:
            number_words[word] = (10**power, 0, suffix, True)

    # Needed for 'imply_single_unit'
    valid_scale_words = set()
    for word_pairs, _power in scales:
        for word, _suffix in word_pairs:
            valid_scale_words.add(word)

    valid_unit_words = set()
    for units_iter in (units, units_tens):
        for word_pairs in units_iter:
            for word, _suffix in word_pairs:
                valid_unit_words.add(word)

    valid_zero_words = {word for (word, _suffix) in units[0]}

    valid_digit_words.update(number_words.keys())
    valid_digit_words.remove("and")
    valid_digit_words.remove("")
    return (
        number_words,
        valid_digit_words,
        valid_unit_words,
        valid_scale_words,
        valid_zero_words,
    )


# Originally based on: https://ao.gl/how-to-convert-numeric-words-into-numbers-using-python/
# A module like class can't be instanced.
class from_words_to_digits:
    """A class for converting numbers expressed in English words into digits.
    
    For example, "two hundred and fifty six" -> "256". Originally based on: https://ao.gl/how-to-convert-numeric-words-into-numbers-using-python/
    """
    (
        _number_words,
        valid_digit_words,
        valid_unit_words,
        valid_scale_words,
        valid_zero_words,
    ) = from_words_to_digits_setup_once()

    @staticmethod
    def _parse_number_as_whole_value(
        word_list: List[str],
        word_list_len: int,
        word_index: int,
        imply_single_unit: bool = False,
        force_single_units: bool = False,
    ) -> Tuple[str, str, int, bool]:
        """Parse a number from a list of words starting at the given index.

        Returns:
            A tuple containing:
            - The parsed number as a string.
            - A suffix if applicable (e.g. "th" for "fifth").
            - The index of the next word after the parsed number.
            - A boolean indicating whether the parsed number can be reformatted with a separator (e.g. "1,000" instead of "1000").
        """
        number_words = from_words_to_digits._number_words
        valid_scale_words = from_words_to_digits.valid_scale_words
        valid_unit_words = from_words_to_digits.valid_unit_words
        valid_zero_words = from_words_to_digits.valid_zero_words

        only_scale = imply_single_unit

        # Allow reformatting for a regular number.
        allow_reformat = True

        # Primary loop.
        current = result = 0
        suffix = ""

        # This prevents "one and" from being evaluated.
        is_final = False
        # increment_final = 0  # UNUSED.
        increment_final_real = 0
        scale_final = 0
        word_index_final = -1
        result_final = ("", "", word_index, allow_reformat)

        # Loop while splitting to break into individual words.
        while word_index < word_list_len:
            word_data = number_words.get(word_list[word_index])

            if word_data is None:
                # raise Exception('Illegal word: ' + word)
                break

            # When explicitly stated, the word "zero" should terminate the current number and start a new value.
            # Since it doesn't make sense to say "fifty zero" as it does to say "fifty one".
            if word_index_final != -1 and word_list[word_index] in valid_zero_words:
                break

            # Use the index by the multiplier.
            scale, increment, suffix, is_final = word_data
            increment_real = increment
            if force_single_units:
                if increment != 0:
                    increment = 1

            # This prevents "three and two" from resolving to "5".
            # which we never want, unlike "three hundred and two" which resolves to "302"
            if word_index_final != -1:
                if not is_final:
                    if word_list[word_index_final - 1] in valid_unit_words:
                        break

                # Check the unit words can be combined!
                # Saying "twenty one" makes sense but the following cases don't:
                # - "twenty twelve"
                # - "ninety fifty"
                if scale_final == scale:
                    if word_list[word_index] in valid_unit_words and word_list[word_index_final] in valid_unit_words:
                        if not (increment_final_real >= 20 and increment_real < 10):
                            break

            if imply_single_unit:
                if only_scale:
                    if word_list[word_index] not in valid_scale_words:
                        only_scale = False

                    if only_scale and current == 0 and result == 0:
                        current = 1 * scale
                        word_index += 1
                        break

            current = (current * scale) + increment

            # If larger than 100 then push for a round 2.
            if scale > 100:
                result += current
                current = 0

            word_index += 1

            if is_final:
                result_final = ("{:d}".format(result + current), suffix, word_index, allow_reformat)
                word_index_final = word_index
                scale_final = scale
                # increment_final = increment
                increment_final_real = increment_real

            # Once there is a suffix, don't attempt to parse extra numbers.
            if suffix:
                break

        if not is_final:
            # Use the last final result as the output (this resolves problems with a trailing 'and')
            return result_final

        # Return the result plus the current.
        return "{:d}".format(result + current), suffix, word_index, allow_reformat

    @staticmethod
    def _allow_follow_on_word(w_prev: str, w: str) -> bool:
        """Returns True if the current word can follow the previous word without delimiting.
        
        For example, "thirteen and fifty five" should be parsed as "13 and 55" without delimiting "fifty".

        Args:
            w_prev: The previous word.
            w: The current word.
        
        Returns:
            True if the current word can follow the previous word without delimiting, False otherwise.
        """
        valid_unit_words = from_words_to_digits.valid_unit_words
        number_words = from_words_to_digits._number_words

        if w_prev not in valid_unit_words:
            return False
        if w not in valid_unit_words:
            return False
        increment_prev = number_words[w_prev][1]
        increment = number_words[w][1]
        if (increment_prev >= 20) and (increment < 10) and (increment != 0):
            return True
        return False

    @staticmethod
    def parse_number_calc_delimiter_from_series(
        word_list: List[str],
        word_index: int,
        word_index_len: int,
    ) -> int:
        """Delimit numbers in a series.
        
        For example, "twenty twenty and twenty twenty one" should be parsed as "2020 and 2021" with the first "twenty" delimiting the first number and the second "twenty" delimiting the second number.

        Args:
            word_list: The list of words to parse.
            word_index: The index of the first word to parse.
            word_index_len: The length of the list of words to parse.
        
        Returns:
            The index of the next word after the parsed number.
        """
        valid_unit_words = from_words_to_digits.valid_unit_words
        number_words = from_words_to_digits._number_words

        i = word_index
        i_span_beg = word_index
        w_prev = ""
        result_prev = None
        result_test = None
        while i < word_index_len:
            w = word_list[i]
            if w not in number_words:
                break

            if (i != word_index) and from_words_to_digits._allow_follow_on_word(word_list[i - 1], w):
                # Don't set `w_prev` so we can detect "thirteen and fifty five" without the last "five" delimiting.
                pass
            else:
                if (w_prev not in {"", "and"}) and w in valid_unit_words:
                    # Exception ... allow "thirty three", two words...
                    result_prev = result_test
                    result_test = from_words_to_digits._parse_number_as_whole_value(
                        word_list,
                        i,  # Limit.
                        i_span_beg,  # Split start.
                        force_single_units=True,
                    )
                    # NOTE: in *almost* all cases this assertion is valid.
                    # `assert i == result_test[2]`.
                    # However these may not be equal if there are multiple disconnected series.
                    # e.g. `twenty twenty and twenty twenty one` -> `2020 and 2021`, see: #92.
                    assert i >= result_test[2]
                    if result_test[2] == i:
                        if result_prev:
                            if len(result_prev[0]) == len(result_test[0]):
                                return result_prev[2]
                    i_span_beg = i
                w_prev = w
            i += 1

        result_prev = result_test
        result_test = from_words_to_digits._parse_number_as_whole_value(
            word_list,
            i,  # Limit.
            i_span_beg,  # Split start.
            force_single_units=True,
        )

        if result_prev:
            if len(result_prev[0]) == len(result_test[0]):
                return result_prev[2]

        return word_index_len

    @staticmethod
    def parse_number_calc_delimiter_from_slide(
        word_list: List[str],
        word_index: int,
        word_index_len: int,
    ) -> int:
        """Delimit numbers in a sliding manner.
        
        For example, "one hundred two hundred" should be parsed as "100 200" with the first "one" delimiting the first number and the second "two" delimiting the second number.

        Args:
            word_list: The list of words to parse.
            word_index: The index of the first word to parse.
            word_index_len: The length of the list of words to parse.
        
        Returns:
            The index of the next word after the parsed number.
        """
        valid_unit_words = from_words_to_digits.valid_unit_words
        number_words = from_words_to_digits._number_words
        i = word_index
        w_prev = ""
        while i < word_index_len:
            w = word_list[i]
            if w not in number_words:
                break
            if (i != word_index) and from_words_to_digits._allow_follow_on_word(word_list[i - 1], w):
                # Don't set `w_prev` so we can detect "thirteen and fifty five" without the last "five" delimiting.
                pass
            else:
                if (w_prev not in {"", "and"}) and w in valid_unit_words:
                    result_test_lhs = from_words_to_digits._parse_number_as_whole_value(
                        word_list,
                        i,  # Limit.
                        word_index,  # Split start.
                        force_single_units=True,
                    )
                    result_test_rhs = from_words_to_digits._parse_number_as_whole_value(
                        word_list,
                        word_index_len,  # Limit.
                        i,  # Split start.
                        force_single_units=True,
                    )

                    # If the number on the right is larger, split here.
                    if len(result_test_lhs[0]) <= len(result_test_rhs[0]):
                        return result_test_lhs[2]

                w_prev = w
            i += 1

        return word_index_len

    @staticmethod
    def parse_number(
        word_list: List[str],
        word_index: int,
        imply_single_unit: bool = False,
    ) -> Tuple[str, str, int, bool]:
        """Parse a number from a list of words starting at the given index.
        Returns:
            A tuple containing:
            - The parsed number as a string.
            - A suffix if applicable (e.g. "th" for "fifth").
            - The index of the next word after the parsed number.
            - A boolean indicating whether the parsed number can be reformatted with a separator (e.g. "1,000" instead of "1000").
        """
        word_list_len = len(word_list)

        # Delimit, prevent accumulating "one hundred two hundred" -> "300" for example.
        word_list_len = from_words_to_digits.parse_number_calc_delimiter_from_series(
            word_list,
            word_index,
            word_list_len,
        )
        word_list_len = from_words_to_digits.parse_number_calc_delimiter_from_slide(
            word_list,
            word_index,
            word_list_len,
        )

        return from_words_to_digits._parse_number_as_whole_value(
            word_list,
            word_list_len,
            word_index,
            imply_single_unit=imply_single_unit,
        )

    @staticmethod
    def parse_numbers_in_word_list(
        word_list: List[str],
        numbers_use_separator: bool = False,
        numbers_min_value: Optional[int] = None,
        numbers_no_suffix: bool = False,
    ) -> None:
        """Parses numbers from a list of words in place.
        
        Modifies the list directly. For example, `["twenty", "five"]` -> `["25"]`.

        Args:
            word_list: The list of words to parse.
            numbers_use_separator: Whether to use a separator (e.g. "1,000" instead of "1000") when formatting the parsed numbers.
            numbers_min_value: If not None, numbers below this value will not be replaced with their digit representations. This can be useful to prevent small numbers from being replaced, for example if you want to keep "one" as a word but replace "twenty" with "20".
            numbers_no_suffix: Whether to ignore suffixes (e.g. "th" for "fifth") when parsing numbers. If True, "fifth" will be parsed as "5" instead of "5th".
        """
        i = 0
        i_number_prev = -1
        orig_word_list = word_list.copy()
        while i < len(word_list):
            if word_list[i] in from_words_to_digits.valid_digit_words:
                number, suffix, i_next, allow_reformat = from_words_to_digits.parse_number(
                    word_list, i, imply_single_unit=True
                )
                if i != i_next:
                    if numbers_no_suffix and suffix:
                        i += 1
                        continue

                    word_list[i:i_next] = [
                        ("{:,d}".format(int(number)) if (numbers_use_separator and allow_reformat) else number)
                        + suffix
                    ]

                    if (i_number_prev != -1) and (i_number_prev + 1 != i):
                        words_between = tuple(word_list[i_number_prev + 1 : i])
                        found = True
                        # While more could be added here, for now this is enough.
                        if words_between == ("point",):
                            word_list[i_number_prev : i + 1] = [word_list[i_number_prev] + "." + word_list[i]]
                        elif words_between == ("minus",):
                            word_list[i_number_prev : i + 1] = [word_list[i_number_prev] + " - " + word_list[i]]
                        elif words_between == ("plus",):
                            word_list[i_number_prev : i + 1] = [word_list[i_number_prev] + " + " + word_list[i]]
                        elif words_between == ("divided", "by"):
                            word_list[i_number_prev : i + 1] = [word_list[i_number_prev] + " / " + word_list[i]]
                        elif words_between in {("multiplied", "by"), ("times",)}:
                            word_list[i_number_prev : i + 1] = [word_list[i_number_prev] + " * " + word_list[i]]
                        elif words_between == ("modulo",):
                            word_list[i_number_prev : i + 1] = [word_list[i_number_prev] + " % " + word_list[i]]
                        else:
                            found = False

                        if found:
                            i = i_number_prev

                    i_number_prev = i
                    i -= 1
            i += 1

        # Group numbers - recite single digit phone numbers for example.
        # This could be optional, but generally seems handy (good default behavior),
        # e.g. "twenty twenty" -> "2020".
        i = 0
        while i < len(word_list):
            if word_list[i].isdigit() and len(word_list[i]) <= 2:
                j = i + 1
                while j < len(word_list):
                    if word_list[j].isdigit() and len(word_list[j]) <= 2:
                        j += 1
                    else:
                        break
                if i + 1 != j:
                    word_list[i:j] = ["".join(word_list[i:j])]
                    orig_word_list[i:j] = ["".join(orig_word_list[i:j])]
                if numbers_min_value is not None and int(word_list[i]) < numbers_min_value:
                    word_list[i:j] = orig_word_list[i:j]

                i = j
            else:
                i += 1


def replace_numbers(words: list[str], options: Optional[dict[str, Any]] = None) -> list[str]:
    """Post-processor that replaces numbers expressed in English words with their digit representations.
    
    For example, `["twenty", "five"]` -> `["25"]`.

    Args:
        words: The list of words to process.
        options: A dictionary of options for the post-processor. The following options are supported:
            - `numbers_use_separator`: Whether to use a separator (e.g. "1,000" instead of "1000") when formatting the parsed numbers.
            - `numbers_min_value`: If not None, numbers below this value will not be replaced with their digit representations. This can be useful to prevent small numbers from being replaced, for example if you want to keep "one" as a word but replace "twenty" with "20".
            - `numbers_no_suffix`: Whether to ignore suffixes (e.g. "th" for "fifth") when parsing numbers. If True, "fifth" will be parsed as "5" instead of "5th".
    
    Returns:
        The list of words with numbers replaced by their digit representations where applicable.
    """
    if options is None:
        options = {}
    from_words_to_digits.parse_numbers_in_word_list(
        words,
        numbers_use_separator=options.get("numbers_use_separator", False),
        numbers_min_value=options.get("numbers_min_value", None),
        numbers_no_suffix=options.get("numbers_no_suffix", False),
    )
    return words


# Priority 10 as a sensible default
register_post_processor("numbers", 10, replace_numbers)
