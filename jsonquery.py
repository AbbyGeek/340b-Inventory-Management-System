import json

loadfile = open('drug-ndc-0001-of-0001.json')
dataset = json.load(loadfile)
"""
PROBLEMS:
-Quantity not updating past 1
"""
def MedFormatting(item, ndc_input):
    generic_name = item.get('generic_name')
    brand_name = item.get('brand_name')
    manufacturer = item.get('labeler_name')
    package_list = []
    for package in item.get('packaging'):
         package_set = {package['package_ndc']},{package['description']},{package['marketing_start_date']},{package['sample']}
         package_list.append(package_set)
    package_info = PackageLookup(package_list, ndc_input)
    dosage_form = item.get('dosage_form')
    route_list = ""
    for route in item.get('route'):
        route_list += route
    pharm_class_list = ""
    for pharm_class in item.get('pharm_class'):
        pharm_class_list += pharm_class
    med_dict = dict(
        ndc_code = ndc_input, 
        generic_name = generic_name, 
        brand_name = brand_name, 
        manufacturer = manufacturer,
        package_info = package_info, 
        dosage_form = dosage_form, 
        route = route_list,
        pharm_class = pharm_class_list,
        quantity = 1         
    )
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

def PackageLookup(packages, ndc_input):
    for package in packages:
        package_ndc = package[0].pop()
        if ndc_input == package_ndc.replace("-",""):
            return package[1].pop()