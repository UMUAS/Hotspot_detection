

def do_source_detection():
    global current_coordinates
    
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

            data['source']['coordinates'] = current_coordinates #TODO

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