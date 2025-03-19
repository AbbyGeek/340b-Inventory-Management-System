import os
from jsonquery import UpcToNdc, DatabaseLookup, MedFormatting
from inventorydb import CreateDb, AddMed
"""
TODO: 
-Highlight medications when below certain quantity to alert to low stock
-Add/Subtract from inventory switch
-display most recent added/removed med under table
"""

def Main():
    os.system('clear')
    from db_display import GUISetup
    CreateDb()
    GUISetup()
    user_input = ''
    while user_input != 'quit':
        user_input = input('Product NDC or \'quit\' to exit: ')
        if user_input != 'quit':
            ndc_input = UpcToNdc(user_input)
            search_item = DatabaseLookup(ndc_input)
            if search_item is not None:
                med_dict = MedFormatting(search_item, ndc_input)
                AddMed(med_dict)

Main()

"""
    test codes
    Lisinopril 5mg - 
    368180513018

    Hydrocortizone 2.5% - 
    351672300326
"""