import tkinter as tk
import tkinter.font as tkFont
from inc_search._utils.utils import open_app
import sys


class GUI:
    def __init__(self, root, app_dict, trie, HEIGHT, WIDTH):
        self.app_dict = app_dict
        self.trie = trie
        self.root = root
        self.root.bind('<Escape>', self.close)
        self.root.bind('<Control-bracketleft>', self.close)
        self.root.bind("<Return>", self.on_select)
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        self.root.option_add("*Font", default_font)

        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack()
        self.entry.focus()
        self.entry.bind('<KeyRelease>', self.on_keyrelease)

        self.listbox = tk.Listbox(root, width=WIDTH, height=HEIGHT)
        self.listbox.pack()
        self.listbox.bind("<j>", self.next_selection)
        self.listbox.bind("<k>", self.prev_selection)
        self.listbox_update([*self.app_dict])

    def on_keyrelease(self, event):

        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()

        # get data from app_dict
        if value == '':
            data = self.trie.search_with_wildcard('*')
        else:
            data = self.trie.search_with_wildcard(
                '*'+''.join([*value[::1]])+'*')

        # update data in listbox
        self.listbox_update(data)

    def listbox_update(self, data):
        # delete previous data
        self.listbox.delete(0, 'end')

        # sorting data
        data = sorted(data, key=str.lower)

        # put new data
        for item in data:
            self.listbox.insert('end', item)

    def on_select(self, event):
        cur_selection = self.listbox.curselection()
        if len(cur_selection) > 0:
            open_app(self.app_dict, self.listbox.get(cur_selection[0]))
            self.root.withdraw()
            sys.exit()
        else:
            open_app(self.app_dict, self.listbox.get(0))
            self.root.withdraw()
            sys.exit()

    def close(self, event):
        self.root.withdraw()
        sys.exit()

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

    def next_selection(self, event):
        cur_selection = self.listbox.curselection()

        # default next selection is the beginning
        next_selection = 0

        # make sure at least one item is selected
        if len(cur_selection) > 0:
            # Get the last selection, remember they are strings for some reason
            # so convert to int
            last_selection = int(cur_selection[-1])

            # clear current selections
            self.listbox.selection_clear(cur_selection)

            # Make sure we're not at the last item
            if last_selection < self.listbox.size() - 1:
                next_selection = last_selection + 1

        self.listbox.activate(next_selection)
        self.listbox.selection_set(next_selection)
        self.listbox.see(next_selection)

    def prev_selection(self, event):
        cur_selection = self.listbox.curselection()
        next_selection = self.listbox.size() - 1

        if len(cur_selection) > 0:
            last_selection = int(cur_selection[-1])
            self.listbox.selection_clear(cur_selection)

            if last_selection > 0:
                next_selection = last_selection - 1

        self.listbox.activate(next_selection)
        self.listbox.selection_set(next_selection)
        self.listbox.see(next_selection)
