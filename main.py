import os
from jsonquery import UpcToNdc, DatabaseLookup, MedFormatting
from inventorydb import CreateDb, AddMed
from db_display import FetchDataAsync, GUISetup
"""
TODO: 
-display most recent added/removed med under table
-issues with buspirone 5mg
-text box should always stay selected
- Tell Yashita Redy to go fuck herself and that I've never been happier since getting kicked from her team.
    I'm not a failure. I'm not a waste. I'm not the best programmer in the world, but I am capable of figuring this out, despite her best wishes.
"""
 
def Main():
    os.system('clear')
    CreateDb()
    GUISetup()
    FetchDataAsync()

Main()

"""
    test codes
    Lisinopril 5mg - 
    368180513018

    Hydrocortizone 2.5% - 
    351672300326

    Metformin 500mg
    365862008015

    Metformin 100mg
    370010065017
"""