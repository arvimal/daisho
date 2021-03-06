#!/usr/bin/env python3

# MIT License

# Copyright (C) 2018 Vimal A.R <arvimal@yahoo.in>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import configparser
import datetime
import logging
import os
import pathlib
import sys
import time

from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import ProgressBar
from pygments.token import Token

from client import daisho_add
from client import daisho_db
from client import daisho_list
from client import daisho_help

if sys.version[0] != "3":
    print("\nDaisho requires Python v3")
    print("Exiting!\n")
    sys.exit(1)

HOME = os.getenv("HOME")
DAISHO_HOME = HOME + "/.config/daisho/"
CONFIG = DAISHO_HOME + "daisho.conf"
HISTORY = DAISHO_HOME + "history.txt"
LOG_FILE = DAISHO_HOME + "daisho.log"
daisho_logger = logging.getLogger(__name__)


class Daisho(object):
    """Daisho's main class: Testing"""

    def __init__(self):
        # Check existence of CONFIG
        if all([pathlib.Path(CONFIG).exists()]):
            daisho_logger.info(
                "{} exists, Welcome to Daisho".format(pathlib.Path(CONFIG))
            )
            print("\n\t- Welcome to Daisho -\n")
            # Check if we are able to connect to MongoDB.
            daisho_db.mongo_conn()
            daisho_help.usage()
            self.daisho_prompt()
            daisho_logger.info("Started Daisho prompt.")

        else:
            print("\n\t- Welcome to Daisho -\n")
            print("Initial setup:")
            print("\tCreating Daisho's configurations")

            # Create HOME, CONFIG, HISTORY, and LOG_FILE
            pathlib.Path(DAISHO_HOME).mkdir()
            pathlib.Path(CONFIG).touch(exist_ok=True)
            pathlib.Path(HISTORY).touch(exist_ok=True)
            # pathlib.Path(LOG_FILE).touch(exist_ok=True)
            # Write Daisho's configuration file
            conf_parser = configparser.ConfigParser()
            conf_parser.add_section("Global")
            conf_parser.set("Global", "DAISHO_HOME", DAISHO_HOME)
            conf_parser.set("Global", "CONFIG", CONFIG)
            conf_parser.set("Global", "HISTORY", HISTORY)
            conf_parser.set("Global", "LOG_FILE", LOG_FILE)
            with open(CONFIG, "w") as config_file:
                conf_parser.write(config_file)
            print("\tDone")

            # Configure logging from here
            logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
            logging.info("Generating configuration files.")
            logging.info("#### Daisho starting up ####")
            # Check if we are able to connect to MongoDB.
            daisho_db.mongo_conn()
            daisho_help.usage()
            self.daisho_prompt()
            logging.info("Started Daisho prompt.")

    def daisho_prompt(self):
        """
        Daisho's prompt.
        """
        cmd_list = ["add", "del", "list", "find", "edit", "open", "help", "quit"]
        keyword_completer = WordCompleter(cmd_list, ignore_case=True)

        while True:
            daisho_prompt = prompt(
                "daisho ->> ",
                history=FileHistory(HISTORY),
                auto_suggest=AutoSuggestFromHistory(),
                completer=keyword_completer,
            )
            # Split the input to a list
            values = [i for i in daisho_prompt.split()]
            key_word = values[0].lower()

            if key_word in cmd_list:
                # Case 1: key_word is `help` / `quit` / `list`
                # `help` and `quit` are cases where a single arg is valid.
                # `list` without args should list all tasks and notes [Feature]
                if len(values) == 1:
                    if key_word == "help":
                        self.daisho_help()
                    elif key_word == "quit":
                        sys.exit("\nExiting Daisho.\n")
                    elif key_word == "list":
                        self.list_tasks(criteria="all")
                    else:
                        self.daisho_help()
                        self.daisho_prompt()

                elif len(values) > 1:
                    # Case 2: key_word is "add"
                    if key_word == "add":
                        add_args = ["note", "task"]
                        if values[1].lower() in add_args:
                            daisho_add.add_prompt(job_type=values[1].lower())
                            self.daisho_prompt()
                        else:
                            print(daisho_add.add_prompt.__doc__)
                            self.daisho_prompt()

                    # Case 3: key_word is "list"
                    if key_word == "list":
                        list_args = ["all", "today", "tags", "prio", "trash"]
                        if values[1].lower() in list_args:
                            self.list_tasks(criteria=values[1].lower())
                        else:
                            print(self.list_tasks.__doc__)
                            self.daisho_prompt()

                    # Case 4: key_word is "edit"
                    if key_word == "edit":
                        edit_args = ["task", "note"]
                        if values[1].lower() in edit_args:
                            try:
                                if values[2]:
                                    try:
                                        job_type, num = (
                                            values[1].lower(),
                                            int(values[2]),
                                        )
                                        self.edit_jobs(job_type=job_type, number=num)
                                    except ValueError:
                                        print(self.edit_jobs.__doc__)
                                        self.daisho_prompt()
                            except IndexError:
                                print(self.edit_jobs.__doc__)
                                self.daisho_prompt()
                        else:
                            # print("`edit` takes either `task` or `note` as argument.")
                            print(self.edit_jobs.__doc__)
                            self.daisho_prompt()

                    # Case 5: key_word is "open"
                    if key_word == "open":
                        open_args = ["task", "note"]
                        if values[1].lower() in open_args:
                            try:
                                if values[2]:
                                    try:
                                        job_type, num = (
                                            values[1].lower(),
                                            int(values[2]),
                                        )
                                        self.open_jobs(job_type=job_type, number=num)
                                    except ValueError:
                                        print(self.open_jobs.__doc__)
                                        self.daisho_prompt()
                            except IndexError:
                                print(self.open_jobs.__doc__)
                                self.daisho_prompt()
                        else:
                            # print("`edit` takes either `task` or `note` as argument.")
                            print(self.open_jobs.__doc__)
                            self.daisho_prompt()

            else:
                # if values[0].lower() not in list
                self.daisho_help()

    def list_tasks(self, criteria=None):
        """
        `list` accepts the following arguments:
            * all
            * today
            * date, in `DD-MM-YYYY` format
            * tags
            * prio
            * trash
        """
        print("List called with argument `{}`".format(criteria))
        pass

    def search_tasks(self, *args):
        """
        `search` accepts a keyword, to search.

        It returns the notes / tasks which contain the keyword.
        """
        print(self.search_tasks.__doc__)
        pass

    def edit_jobs(self, job_type, number):
        """
        `edit` accepts the following arguments, and a number.
            * note
            * task

        Example:
            ->> edit note 4 # To edit the 4th note in the list.
            ->> edit task 3 # To edit the 5th task in the list.
        """
        print("\nEditing {}: #{}\n".format(job_type, number))

    def open_jobs(self, job_type, number):
        """
        `open` accepts the following arguments, and a number.
            * note
            * task

        Example:
            ->> open note 4 # To open the 4th note in the list.
            ->> open task 3 # To open the 5th task in the list.
        """
        print("\nEditing {}: #{}\n".format(job_type, number))


if __name__ == "__main__":
    my_daisho = Daisho()
    my_daisho
