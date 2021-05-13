import tkinter as tk
from inc_search.trie import Trie
from inc_search._utils.utils import get_all_apps, open_app
import sys


def on_keyrelease(event):

    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()

    # get data from app_dict
    if value == '':
        data = trie.search_with_wildcard('*')
    else:
        data = trie.search_with_wildcard('*'+''.join([*value[::1]])+'*')

    # update data in listbox
    listbox_update(data)


def listbox_update(data):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)


def on_select(event):
    cur_selection = listbox.curselection()
    if len(cur_selection) > 0:
        open_app(app_dict, listbox.get(cur_selection[0]))
        root.withdraw()  # if you want to bring it back
        sys.exit()  # if you want to exit the entire thing
    else:
        open_app(app_dict, listbox.get(0))
        root.withdraw()  # if you want to bring it back
        sys.exit()  # if you want to exit the entire thing


def close(event):
    root.withdraw()  # if you want to bring it back
    sys.exit()  # if you want to exit the entire thing


def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")


def next_selection(event):
    cur_selection = listbox.curselection()

    # default next selection is the beginning
    next_selection = 0

    # make sure at least one item is selected
    if len(cur_selection) > 0:
        # Get the last selection, remember they are strings for some reason
        # so convert to int
        last_selection = int(cur_selection[-1])

        # clear current selections
        listbox.selection_clear(cur_selection)

        # Make sure we're not at the last item
        if last_selection < listbox.size() - 1:
            next_selection = last_selection + 1

    listbox.activate(next_selection)
    listbox.selection_set(next_selection)
    listbox.see(next_selection)


def prev_selection(event):
    cur_selection = listbox.curselection()
    next_selection = listbox.size() - 1

    if len(cur_selection) > 0:
        last_selection = int(cur_selection[-1])
        listbox.selection_clear(cur_selection)

        if last_selection > 0:
            next_selection = last_selection - 1

    listbox.activate(next_selection)
    listbox.selection_set(next_selection)
    listbox.see(next_selection)

# --- main ---


HEIGHT = 20
WIDTH = 40

all_apps, app_dict = get_all_apps()
trie = Trie()
trie.add_all([*app_dict])

root = tk.Tk()
root.bind('<Escape>', close)
root.bind('<Control-bracketleft>', close)
root.bind("<Return>", on_select)

entry = tk.Entry(root, width=40)
entry.pack()
entry.focus()
entry.bind('<KeyRelease>', on_keyrelease)

listbox = tk.Listbox(root, width=WIDTH, height=HEIGHT)
listbox.pack()
listbox.bind("<j>", next_selection)
listbox.bind("<k>", prev_selection)
listbox_update([*app_dict])

root.mainloop()
