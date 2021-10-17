This was a weekend project to help my friend automate a process he was having to do multiple times a day at work.
It allows you to find out a list of who's working at a company and all of the companies they are associated with depending on the depth you wish to choose:

How to use:
  Run Main.py, or tests.py:
  args:
    Enter a valid company_id such as '07798925'
    Enter a depth, if this field is empty a depth of 1 will be assumed.
  return:
    A tree-like structure containing all the officers and their associated companies with a risk investment value

This system is scaled to cater for any number of requests, although potentially using some sort of parallelisation would seem appropriate.
