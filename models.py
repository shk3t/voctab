from utils import *


class Menu:
    message = None

    def __init__(self, *options, default_action=None, main=False):
        self.options = dict(enumerate(options, 1))
        self.default_action = (
            default_action if default_action else Menu._default_default_action
        )
        self.is_main = main

    def show(self):
        response = None
        while not response:
            self._show_message()
            self._show_options()
            index = self._prompt_option()
            clear_console()
            response = self._run_action(index)

    def show_message(message):
        Menu.message = message

    def go_back():
        return "Go back"

    def goto_main(message=None):
        if message:
            Menu.message = message
        clear_console()
        raise GoToMainMenuException

    def _show_options(self):
        for (index, option) in self.options.items():
            print(f"{index}. {option.label}")

    def _prompt_option(self):
        index = input("Select option: ")
        if index.isnumeric():
            return int(index)
        return index

    def _run_action(self, index):
        action = self.options.get(index, self.default_action)
        if self.is_main:
            try:
                return action()
            except GoToMainMenuException:
                return None
        return action()

    def _show_message(self):
        if Menu.message:
            print(Menu.message, end="\n\n")
            Menu.message = None

    def _default_default_action():
        Menu.message = "Wrong option, select another"


class Option:
    def __init__(self, label, action):
        self.label = label
        self.action = action

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)

    def not_implemented():
        Menu.message = "Sorry, this feature is not implemented"


class Entry:
    mode = TMode.ENtoRU

    def __init__(self, en_content, ru_content, success_count, fail_count):
        self.en_content = en_content
        self.ru_content = ru_content
        self.success_count = success_count
        self.fail_count = fail_count


# class Entries(list):
#     def __init__(self, args):
#         list.__init__(args)
