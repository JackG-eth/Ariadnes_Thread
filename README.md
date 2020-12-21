This project allows you to find out a list of who's working at a company and all of the companies they are associated with depending on the depth you wish to choose:
  1.) Important note: depths above 1 do not tend to work unless the company you choose to test is extremely small as the function tends to reach the maximum limit of 500 calls in 5 minutes
  2.) If you have an API_key that allows you to make more calls then there will be no issues using a higher depth
  3.) The risk calculation formula Definitely needs work but it how it is integrated does not need to change

I ran the project using anaconda and its imperative that you have the following libraries installed:
  import PySimpleGUI as sg
  import uuid
  import tkinter as tk
  from tkinter import ttk
  import re
  from companies_house.api import CompaniesHouseAPI

How to use:
  Run Main.py, or tests.py:
  args:
    Enter a valid company_id such as '07798925'
    Enter a depth, if this field is empty a depth of 1 will be assumed.
  return:
    A tree-like structure containing all the officers and their associated companies with a risk investment value

This system is scaled to cater for any number of requests, although potentially using some sort of parallelisation would seem appropriate.


Note:
 I haven't used to python in a while so this project took a little longer than expected. I had to get a working environment first and remember a lot of the syntax and how certain data structures worked so please bare this in mind when marking it! I did, however, thoroughly enjoy this project!
