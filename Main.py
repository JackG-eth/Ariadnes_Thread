import PySimpleGUI as sg
import uuid
import tkinter as tk
from tkinter import ttk
from Logic import get_associated_companies_info_by_company, get_company_info, getCompanyScore
# 07798925 IWOCA -- Get Banned due to many API Calls if depth > 1

"""
    4. test_something
    5. Write a readme about how it works/issues
"""

"""
# Setup the root UI to display data as tree-like structure
Args:
    Tree: Created in tk_tree_view(data):
    Parent: " "
    Dic: Data(Dictionary)
"""


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


"""
# Setup the root UI to display data as tree-like structure
Args:
    Dictionary  object: Complex object containing (Officer Name,Companyies,Risk%)
"""


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


"""
Creates a GUI for the user allowing them to search a company
Args:
    company_no (str): Registered company number.
    depth (int): How far back they wish to investigate
Returns:
    Information Companies House holds on the company and their associated officers etc...
"""


def HomeDisplay():

    # Defining the layout of the GUI
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Enter CompanyID')],
        [sg.InputText(key='-CompanyID-')],
        [sg.Text('Enter Depth')],
        [sg.InputText(key='-Depth-')],
        [sg.Button('Search'), sg.Button('Exit')]]

    # Create the window
    window = sg.Window('Search a company', layout, grab_anywhere=True)

    # The event loop
    while True:
        # Read the event that happened and the values dictionary
        event, values = window.read()
        text_input_officers = values['-CompanyID-']
        depth = values['-Depth-']
        # If user closed window with X or if user clicked "Exit" button then
        # exit
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Search':
            # if user does not enter a depth field default to 0
            if(depth == ''):
                depth = 0
            if(text_input_officers != '' and len(text_input_officers) == 8):
                officerD = get_associated_companies_info_by_company(
                    text_input_officers, int(depth))
                tk_tree_view(officerD)
            else:
                print("Invalid CompanyID")

    window.close()


"""
Calls HomeDisplay Function
"""


def main():
    HomeDisplay()


main()
