import json
import os

loadfile = open('drug-ndc-0001-of-0001.json')
dataset = json.load(loadfile)

def MedFormatting(item):
    generic_name = item.get('generic_name')
    labeler_name = item.get('labeler_name')
    brand_name = item.get('brand_name')
    ingredient_list = []
    for ingredient in item.get('active_ingredients'):
        ingredient_set = {ingredient['name']},{ingredient['strength']}
        ingredient_list.append(ingredient_set)
    package_list = []
    for package in item.get('packaging'):
        package_set = {package['package_ndc']},{package['description']},{package['marketing_start_date']},{package['sample']}
        package_list.append(package_set)
    pakcage_info = PackageLookup(package_list)
    med_dict = dict(generic_name = generic_name, manufacturer = labeler_name, brand_name = brand_name, package_info = pakcage_info, ingredients = ingredient_list)
    return med_dict

def DatabaseLookup(ndc_number):
    for item in dataset['results']:
        npc_code = item.get('product_ndc').replace("-","")
        if npc_code in ndc_number:
            print('Found Item')
            return item

def UpcToNdc(upc_input):
    #If UPC is 11 digits, leave alone. If 12, format the data
    if len(upc_input) == 12:       
        upc_input = upc_input[1:-1]   
    # elif len(upc_input) != 11:
    #     raise ValueError("Invalid UPC format. Must be 11 or 12 digits.")
    ndc_input = upc_input[:-2]
    package_code = upc_input[-2:]
    return ndc_input + package_code

def PackageLookup(packages):
    for package in packages:
        package_ndc = package[0].pop()
        if ndc_input == package_ndc.replace("-",""):
            return package[1].pop()
        

os.system('clear')
user_input = ''
while user_input != 'quit':
    user_input = input('Product NDC or \'quit\' to exit: ')
    if user_input != 'quit':
        ndc_input = UpcToNdc(user_input)
        search_item = DatabaseLookup(ndc_input)
        if search_item is not None:
            med_dict = MedFormatting(search_item)
            print("Generic Name: " + med_dict['generic_name'])
            print("Manufacturer: " + med_dict['manufacturer'])
            print("Brand Name: " + med_dict['brand_name'])
            print("Package Info: " + med_dict['package_info'])
            print("Active Ingredients:")
            for ingredient in med_dict['ingredients']:
                ingredient_name = ingredient[0].pop()
                ingredient_dosage = ingredient[1].pop()
                print(ingredient_name + ": " + ingredient_dosage)
        else:
            print("No item found")
    print('End of Operation')

    #test codes
    # Lisinopril 5mg - 
    # 368180513018
    # 6810-513-01  (9 digits)
    #returns Generic name, Manufacturer, brand name, package info (100 tablet in 1 bottle), active ingredients

    # Hydrocortizone 2.5% - 
    # 351672300326
    # 51672-3003-2 (10 digits)
    #returns: Generic name, manufacturer, brand name, package info (1 tube in 1 carton, 28.35g/tube), active ingredients

    