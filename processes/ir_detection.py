
def do_ir_detection():
    global data 
    global save_state
    global current_coordinates 
    global print_hotspots 
    global is_valid_index
    global get_valid_coordinate
    '''
    === IR Detection ===
    Options:
    "add" - Add current GPS position as IR source.
    "rem" - Remove an IR source.
    "set" - Change coordinates of an IR source.
    "list" - List of IR sources added.
    "exit" - Exit IR detection.
    '''
    options = ["add", "rem", "set", "list", "exit"]

    while True:
        print(do_ir_detection.__doc__)

        option = input('Choose option: ').lower()
        while option not in options:
            option = input('Invalid input! Try again: ').lower()

        if(option == 'exit'):
            print('Exiting IR detection.')
            save_state()
            print("program state saved to JSON file")
            break

       

        if(option == 'add'):
            data["hotspots"].push(current_coordinates)
            save_state()
            print("[o] New hotspot added and program state saved to JSON file")
            

        elif(option == 'rem'):
            print_hotspots()
            print('Remove a hotspot by its index in the list. To cancel, type "cancel".')

            indexStr = input('Choose option:').lower()
            while (not indexStr.isnumeric() and indexStr != "cancel") or (indexStr.isnumeric() and is_valid_index(int(indexStr))):
                indexStr = input('Invalid input! Try again: ').lower()

            if(indexStr == 'cancel'):
                continue
            else:
                hotspot_index = int(indexStr)
                data["hotspots"].pop(hotspot_index)
            save_state()
            print("[o] Hotspot removed and program state saved to JSON file")

            

        elif(option == 'set'):
            print_hotspots()
            print("Modify Hotspot coordinates by its index in the list. To cancel, type 'cancel'.")

            indexStr = input ("Choose hotspot: ").lower()
            while (not indexStr.isnumeric() and indexStr != "cancel") or (indexStr.isnumeric() and is_valid_index(int(indexStr))):
                indexStr = input('Invalid input! Try again: ').lower()

            if(indexStr == "cancel"):
                continue
            else:
                hotspot_index = int(indexStr)
                latitude = get_valid_coordinate("Enter latitude (-90 to 90): ", -90, 90)
                longitude = get_valid_coordinate("Enter longitude (-180 to 180): ", -180, 180)
                data["hotspots"][hotspot_index] = (longitude,latitude)
            save_state()
            print("[o] Hotspot data modified and program state saved to JSON file")

        
        elif(option == 'list'):
            print_hotspots()



