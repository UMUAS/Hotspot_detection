
import os
import json
# from pymavlink import mavutil

filepath = None
data = None
connection = None #Pixhawk connection

def main():
    '''
    Options:
    "1" - Start IR detection.
    "2" - Start source detection.
    "3" - Generate KML file.
    "4" - Transmit KML file.
    "exit" - Exit program.
    '''

    global data, filepath
    filepath = 'records.json'
    i = 1
    while os.path.exists(filepath):
        filepath = f'records ({i}).json'
        i+=1

    with open(filepath, 'x') as f:
        data = json.loads('{"hotspots": [], "source": {"description": "", "coordinates": ""}}')
        json.dump(data, f, indent=4)
    
    options = {
        '1': do_ir_detection,
        '2': do_source_detection,
        '3': do_kml_generation,
        '4': do_transmit_kml,
        'exit': None
    }
    while True:
        print(main.__doc__)

        option = input('Choose option: ').lower()
        while option not in options:
            option = input('Invalid input! Try again: ').lower()

        if(option == 'exit'):
            break

        options[option]()

    # Connect to the Pixhawk over UDP
    # connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')

    # Wait for a heartbeat so we know the connection is active
    # connection.wait_heartbeat()

    save_temp()

    print('Program ended.')

#initlize seperate thread for each task
def init():
    pass

def do_ir_detection():
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
            break

        hotspots:list = data['hotspots']

        if(option == 'add'):
            ... #TODO

        elif(option == 'rem'):
            print('Hotspots:')
            print_list(hotspots)
            print(f'Remove a hotspot by its index in the list. To cancel, type "cancel".')

            indexStr = input('Choose option:').lower()
            while (not indexStr.isnumeric() and indexStr != "cancel") or (indexStr.isnumeric() and is_valid_index(int(indexStr))):
                indexStr = input('Invalid input! Try again: ').lower()

            if(indexStr == 'cancel'):
                continue

            i = int(indexStr)
            hotspots.pop(i)

            save_temp()

        elif(option == 'set'):
            ... #TODO

        elif(option == 'list'):
            print('Hotspots:')
            print_list(hotspots)

def do_source_detection():
    '''
    === Fire Source Detection ===
    Options:
    "pos" - Set coordinates as the current GPS position.
    "desc" - Set description.
    "info" - Current source information.
    "exit" - Exit source detection.
    '''
    options = ["pos", "desc", "info", "exit"]

    while True:
        print(do_source_detection.__doc__)

        option = input('Choose option: ').lower()
        while option not in options:
            option = input('Invalid input! Try again: ').lower()

        if(option == 'exit'):
            print('Exiting source detection.')
            break

        if(option == 'pos'):
            option = input('Are you sure you want to update coordinates for the Fire Source? (y/n):')
            if(option.lower() != 'y'): continue

            data['source']['coordinates'] = get_current_coordinates() #TODO

            save_temp()

        elif(option == 'desc'):
            print(f'Current source description:\n{data['source']['description']}')
            option = input('Change description to (or enter "cancel"). New description:\n')
            if(option.lower() == 'cancel'):
                continue

            data['source']['description'] = option

            print('Description changed.')

            save_temp()
        elif(option == 'info'):
            print(f'Source description:\n{data['source']['description']}')
            print(f'Source coordinates:\n{data['source']['coordinates']}')



def do_transmit_kml():
    print('Attempting to send KML file...')

    #TODO

    print('Failed! Attempt to send KML file filed!')
    print('Success! Sent KML file!')

def get_current_coordinates():
    return None #TODO

def save_temp():
    '''Saves temp data to a file.'''
    global data, filepath
    print(f'Writing temporary recordings to: {filepath}')
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def is_valid_index(i:int, lst:list):
    return i >= 0 and i < len(lst)

def print_list(lst:list):
    for i in range(len(lst)):
        print(f'{i}: {lst[i]}')

if __name__ == '__main__':
    main()