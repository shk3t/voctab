#!/usr/bin/env python3.10
import actions
from models import Menu, Option
from utils import clear_console, argwrap, TMode


if __name__ == "__main__":
    clear_console()

    practice_menu = Menu(
        Option("EN to RU", argwrap(actions.start_practice, TMode.ENtoRU)),
        Option("RU to EN", argwrap(actions.start_practice, TMode.RUtoEN)),
        Option("Back", Menu.go_back),
    )

    start_menu = Menu(
        Option("Start practice", practice_menu.show),
        # Option("Edit vocabulary", Option.not_implemented),
        Option("Import translation spreadsheet", actions.import_spreadsheet),
        # Option("Show statistics", Option.not_implemented),
        # Option("Options", Option.not_implemented),
        Option("Quit", quit),
        main=True,
    )

    start_menu.show()
