import argparse
import textwrap
import tkinter as tk
from argparse import RawTextHelpFormatter

from inc_search._utils.utils import get_all_apps
from inc_search.gui import GUI
from inc_search.trie import Trie

HEIGHT = 20
WIDTH = 40

parser = argparse.ArgumentParser(
    description="Incremental Search and Launch Desktop Applications",
    formatter_class=RawTextHelpFormatter)
parser.add_argument("input",
                    nargs='?',
                    metavar="INPUT",
                    type=str,
                    help=textwrap.dedent('''\
        Input data to search in (split by newline)
        If given, applications lancher will be disable and selected item will be copied to clipboard'''
                                         ))
parser.add_argument("-f",
                    "--fuzzy",
                    help="whether to use fuzzy seach or not",
                    action="store_true")


def main(args):
    if not args.input:
        data = get_all_apps()
    else:
        with open(args.input, "r") as f:
            data = f.read().strip().split('\n')

    trie = Trie()
    trie.add_all([*data])

    root = tk.Tk()
    GUI(root, data, trie, HEIGHT, WIDTH, True if not args.input else False,
        args.fuzzy)
    root.mainloop()


if __name__ == "__main__":
    main(parser.parse_args())
