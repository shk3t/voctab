import difflib
import pandas as pd

import db.init
import db.queries
import db.tables
from utils import *
from models import Menu


def import_spreadsheet():
    # Load file, convert to DF
    filepath = input("Enter path to csv/xlsx file: ")
    try:
        if filepath.endswith(".csv"):
            word_df = pd.read_csv(filepath)
        elif filepath.endswith(".xlsx"):
            word_df = pd.read_excel(filepath)
    except FileNotFoundError:
        Menu.show_message("File not found")

    # Transform DF
    if word_df.shape[1] == 4:
        word_df = word_df.iloc[:, 2:]
    word_df.columns = ["en_content", "ru_content"]

    # Strip accident spaces
    for col in word_df.columns:
        word_df[col] = word_df[col].str.strip("\n").str.strip(" ")

    # Insert entries to database
    db.queries.insert_entries(word_df)
    Menu.show_message("Import completed successfully")


def start_practice(mode=TMode.ENtoRU):
    # Fetch data
    cursor = db.queries.select_unsuc_random_entries()
    if cursor.rowcount == 0:
        Menu.goto_main(message="You already know all the words!")

    # Specify train set size
    size = input("Specify train set size: ")
    if size == "0":
        print("Nice")
        quit()
    size = int(size) if size.isnumeric() else DEFAULT_SETSIZE
    clear_console()

    # Convert to DF
    word_df = pd.DataFrame(cursor.fetchmany(size))

    # Setting translation mode
    column_order = (
        ["en_content", "ru_content"]
        if mode == TMode.ENtoRU
        else ["ru_content", "en_content"]
    )

    # Hint
    print(
        """Quick commands:
    :m      end practice and return to main menu
        """
    )

    # Practice cycle
    for index, (word, translation) in word_df[column_order].iterrows():
        guess = input(f"{word} => ")

        # Quick commands
        if guess.startswith(":"):
            if "m" in guess:
                db.queries.update_stats(word_df)
                Menu.goto_main(message="Statistics saved successfully")
            if "c" in guess:  # TODO think about multiple cases
                try:
                    word_df.loc[index - 1, "success_count"] += 2
                except KeyError:
                    print("No translations to correct!")
                else:
                    print("The previous translation was estimated as correct")
                guess = input(f"{word} => ")  # TODO this is crap

        # Evaluate score
        score = difflib.SequenceMatcher(None, guess, translation).ratio()

        # Previous translation info
        clear_console()
        print(word, "=>", guess)

        # Success case
        if score >= SUCCESS_THRESHOLD:
            print("Correct")
            word_df.loc[index, "success_count"] += 1

        # Additional verification case
        elif score >= FAIL_THRESHOLD:
            print("Additional verification needed")
            print(f"Actual translation: {translation}")
            if input("Was you correct? y/(n): ") in "yY":
                word_df.loc[index, "success_count"] += 1
            else:
                word_df.loc[index, "fail_count"] += 1

        # Fail case
        else:
            print("Wrong")
            print(f"Actual translation: {translation}")
            word_df.loc[index, "fail_count"] += 1

        print()

    # Update statistics
    db.queries.update_stats(word_df)
    Menu.show_message("The practice has ended")
