# first part invoels BUSINESS GRAPH
# All directors/shareholdars involved
# if they're involved with other companies get that depth(configurable not too much depth)
# for a given director fetch all the companies they are involved in
# visualise it
## https://pypi.org/project/companies-house/ Companies House Python API (Just need to consume it)
#07798925


"""
TO DO:
    1. Fix issue with not being able to reload
    2. Find a way to recall this function and build it onto tree depending on depth. (HARD)
    3. Add a score computation to the company
    4. test_something
    5. Clean Code up // comment
"""
import PySimpleGUI as sg
import requests
import json
import re
import argparse
import uuid
import tkinter as tk
from tkinter import ttk
from logic import get_associated_companies_info_by_company, get_company_info, getCompanyScore
#10074099 Random Example to show depth -- Works with Depth = 2 before exceeding 500 call limit
#12373908
#07798925 IWOCA -- Get Banned due to many API Calls if depth > 1
officerD = get_associated_companies_info_by_company('10074099',2)

def j_tree(tree, parent, dic):
    for key in sorted(dic.keys()):
        uid = uuid.uuid4()
        if isinstance(dic[key], dict):
            tree.insert(parent, 'end', uid, text=key)
            j_tree(tree, uid, dic[key])
        elif isinstance(dic[key], tuple):
            tree.insert(parent, 'end', uid, text=str(key) + '()')
            j_tree(tree, uid,
                   dict([(i, x) for i, x in enumerate(dic[key])]))
        elif isinstance(dic[key], list):
            tree.insert(parent, 'end', uid, text=str(key) + '[]')
            j_tree(tree, uid,
                   dict([(i, x) for i, x in enumerate(dic[key])]))
        else:
            value = dic[key]
            if isinstance(value, str):
                value = value.replace(' ', '_')
            tree.insert(parent, 'end', uid, text=key, value=value)


def tk_tree_view(data):
    # Setup the root UI
    root = tk.Tk()
    root.title("Company Officers")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Setup the Frames
    tree_frame = ttk.Frame(root, padding="3")
    tree_frame.grid(row=0, column=0, sticky=tk.NSEW)

    # Setup the Tree
    tree = ttk.Treeview(tree_frame, columns=('Values'))
    tree.column('Values', width=20, anchor='center')
    tree.heading('Values', text='Values')
    j_tree(tree, '', data)
    tree.pack(fill=tk.BOTH, expand=1)

    # Limit windows minimum dimensions
    root.update_idletasks()
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
    root.mainloop()

tk_tree_view(officerD)


def HomeDisplay():
    layout = [[sg.Text('Search Company Officers')],[sg.InputText(key='-IN-Officer-')],
             [sg.Button('Go'), sg.Button('Exit')] ,
             [sg.Output(key='-OUT-', size=(80, 20))]]

    window = sg.Window('Window Title', layout, finalize=True)

    event, values = window.read()
    text_input_officers = values['-IN-Officer-']
    officerD = get_associated_companies_info_by_company(text_input_officers)
    tk_tree_view(officerD)
    window.close()

def main():
    HomeDisplay()

#main()
