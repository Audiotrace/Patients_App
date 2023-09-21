
import Levenshtein as lev
from itertools import permutations


class GreekLanguage:

    @staticmethod
    def remove_accents(input_str: str) -> str:
        replacements = {
            'ά': 'α', 'έ': 'ε', 'ή': 'η', 'ί': 'ι', 'ό': 'ο', 'ύ': 'υ', 'ώ': 'ω',
            'Ά': 'Α', 'Έ': 'Ε', 'Ή': 'Η', 'Ί': 'Ι', 'Ό': 'Ο', 'Ύ': 'Υ', 'Ώ': 'Ω',
            'ϊ': 'ι', 'ΐ': 'ι', 'ϋ': 'υ', 'ΰ': 'υ', 'Ϊ': 'Ι', 'Ϋ': 'Υ'
        }

        for old, new in replacements.items():
            input_str = input_str.replace(old, new)

        return input_str

    @staticmethod
    def calculate_levenshtein_distance(str1: str, str2: str) -> int:

        original_text = GreekLanguage.remove_accents(
            str1).upper()

        string_in_test = GreekLanguage.remove_accents(
            str2).upper()

        original_text_without_whitespace = original_text.split()
        string_in_test_without_whitespace = string_in_test.split()

        if len(string_in_test_without_whitespace) > 3 or len(string_in_test_without_whitespace) < 2:

            return 100

        minimum_distance = [47, 0]
        split_words = string_in_test_without_whitespace

        combinations = list(permutations(split_words))
        minimum_distance = [100, 0]

        for idx, possibility in enumerate(combinations):
            combined_string = "".join(possibility)
            distance = lev.distance(
                "".join(original_text_without_whitespace), combined_string, score_cutoff=3)

            if distance < minimum_distance[0]:
                minimum_distance[0] = distance
                minimum_distance[1] = idx

        return minimum_distance[0]


if __name__ == "__main__":
    pass
