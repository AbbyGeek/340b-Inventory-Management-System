from inventorydb import add_medication, get_inventory, dispense_medication

def test_inventory():
    print("\n--- Testing Inventory System ---\n")

    #Test Adding Medication
    print("Adding medication...")
    add_medication("123456789", "Ibuprofen", "Advil", "Pfizer", "200mg Tablet", "Ibuprofen 200mg", 20)
    print("Medication added")

    #Test retrieving inventory
    print("\nFetching inventory...")
    inventory = get_inventory()
    for med in inventory:
        print(med)

    #Test dispensing medication
    print("\nDispensing 5 units of Ibuprofen...")
    dispense_medication("123456789", 5)

    #Check inventory again
    print("\nIpdated Inventory:")
    inventory = get_inventory()
    for med in inventory:
        print(med)

if __name__ == "__main__":
    test_inventory()