import tkinter as tk
from inc_search.trie import Trie
from inc_search._utils.utils import get_all_apps
from inc_search.gui import GUI


HEIGHT = 20
WIDTH = 40

app_dict = get_all_apps()
trie = Trie()
trie.add_all([*app_dict])

root = tk.Tk()
GUI(root, app_dict, trie, HEIGHT, WIDTH)
root.mainloop()
