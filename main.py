from dict_utils import get_valid_words


def solve(box):
    needed_letters = [letter for side in box for letter in side]
    current_letter: str = ""
    valid_words = get_valid_words(box)
    solution = []

    while len(needed_letters) > 0:

        possible_starting_letters = [current_letter]
        if not current_letter:
            possible_starting_letters = needed_letters

        best_scoring_word = tuple(["", 100])

        # determine best scoring word
        for c_letter in possible_starting_letters:
            for word in valid_words:
                if set(needed_letters).issubset(word) and word[0] == c_letter:
                    needed_letters = []
                    best_scoring_word = (word, 0)
                    break

            if len(needed_letters) == 0: break
            # Lower score is better
            for word in valid_words:
                if word.startswith(c_letter) and word not in solution:
                    score = (len(set(needed_letters).difference(set(word))))
                    if score < best_scoring_word[1]:
                        best_scoring_word = (word, score)

        for letter in best_scoring_word[0]:
            try:
                needed_letters.remove(letter)
            except ValueError:
                pass
        if not best_scoring_word[0]:
            solution = []
            break
        solution.append(best_scoring_word[0])
        current_letter = best_scoring_word[0][-1]

    return solution
