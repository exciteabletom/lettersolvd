import sqlite3



def init_db():
    con = sqlite3.connect('words.sqlite')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS words ( 
    word STRING PRIMARY KEY,
    length INTEGER
    );
    """)
    con.commit()

    with open("/usr/share/dict/american-english", "r") as f:
        for line in f:
            word = line.strip().lower()
            if not word.isalpha():
                continue

            word_len = len(word)  # Avoid computing this twice by saving to var
            if word_len < 4:
                continue

            for letter in "abcdefghijklmnopqrstuvwxyz":
                if (letter + letter) in word:
                    continue

            print(word, word_len)
            cur.execute(
                """
                INSERT OR IGNORE INTO words 
                (word, length)
                VALUES (?, ?)
                """, (word, word_len)
            )

    con.commit()
    con.close()


def get_valid_words(box: list[list[str]]) -> list[str]:
    illegal_letter_pairs: list[str] = []
    all_letters = []
    for side in box:
        for letter in side:
            if letter is None:
                continue
            all_letters.append(letter)

            for letter2 in side:
                if letter2 is None:
                    continue
                illegal_letter_pairs.append(letter + letter2)

    all_letters = set(all_letters)

    sub_query = "("
    for pair in illegal_letter_pairs:
        sub_query += f"instr(word, '{pair}') + "
    sub_query = sub_query[:-2] + ")"

    query = f"""SELECT word FROM words WHERE {sub_query} = 0 ORDER BY length DESC"""

    con = sqlite3.connect('words.sqlite')
    cur = con.cursor()
    cur.execute(query)

    valid_words: list[str] = []
    for word in cur.fetchall():
        if set(word[0]).issubset(all_letters):
            valid_words.append(word[0])
    con.close()

    return valid_words