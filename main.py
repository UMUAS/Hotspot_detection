import os
import json
import threading

import argparse 
from pymavlink import mavutil
from processes.ir_detection import do_ir_detection 
from processes.source_detection import do_source_detection
from processes.kml_generation import do_kml_generation
from processes.kml_transmit import do_kml_transmit
from processes.get_current_coordinates import do_get_current_coordinates

#Global Variables 
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
filepath = None
data = None
mavlink_connection = None
current_coordinates = None 

#Helper functions 
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
def establish_mavlink_connection():
    mavlink_connection = mavutil.mavlink_connection(f'udp:{data["udp_addr"]}:{data["udp_port"]}')
    mavlink_connection.wait_heartbeat()
    print("[o] Mavlink connection established")

def get_valid_coordinate(prompt, min_val, max_val):
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"[x] Value must be between {min_val} and {max_val}. Try again.")
        except ValueError:
            print("[x] Invalid number. Please enter a numeric value.")

def save_state():
    '''Saves current program state to a file.'''
    global data, filepath
    print(f'Writing program state to: {filepath}')
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def is_valid_index(i:int, lst:list):
    return i >= 0 and i < len(lst)

def print_hotspots():
    #TODO
    pass


# Multithreading Setup 
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
def init_ir_threads():
    ir_thread = threading.Thread(target=do_ir_detection)
    coordinates_thread = threading.Thread(target=do_get_current_coordinates, args=[mavlink_connection])
    ir_thread.run()
    coordinates_thread.run()


def init_source_threads():
    source_thread = threading.Thread(target=do_source_detection)
    coordinates_thread = threading.Thread(target=do_get_current_coordinates, args=[mavlink_connection])
    source_thread.run()
    coordinates_thread.run()



# Main Function Logic 
#---------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------#
def main():
    global data, filepath
    parser = argparse.ArgumentParser(description='UMUAS Hotspot Detection Program')
    parser.add_argument("-j", "--json", help="json file for storing", required=False, default="state.json")
    parser.add_argument("-i","--ir",help='initiate IR detection routine', required=False, action='store_true')
    parser.add_argument("-s","--source",help='initiate Source detection routine', required=False, action='store_true')
    parser.add_argument('-g',"--generate",help='initiate KML generation', required=False,default='hotspots.kml', action="store_true")
    parser.add_argument('-t',"--transmit", help="transmit kml file", required=False, action="store_true")
    parser.add_argument("-kf","--kmlfile")
    parser.add_argument("-ka","--kmlserver",help="kml server address. Defaults to 0.0.0.0",default="0.0.0.0")
    parser.add_argument("-kp","--kmlport",help="kml server port number. Defaults to 5000",default=5000 )
    parser.add_argument("-up","--uport", help="mavlink udp port. Defaults to",default="14550")
    parser.add_argument("ua","--uaddress",help="mavlink udp address",default="127.0.0.1")
    
    args = parser.parse_args()

    #error handling for argparser 
    #only run when 1 intruction is called (i.e program cant perform ir_detection, source detection, ... simultaneously )
    if(sum([args.source,args.generate,args.transmit,args.ir] > 1)):
        print("[x] program can't perform more than 1 instruction at a time. exiting ...")
        exit()
    if(sum([args.source,args.generate,args.transmit,args.ir] == 0)):
        print('[x] no instruction passed. exiting ...')
        exit()
    
   
    #Fetch previous state 
    with open(filepath, 'x') as f:
        data = json.loads('{"hotspots": [], "source": {"description": "", "coordinates": ""}, "kml_file_path":"hotspots.kml", "serv_add":"", "serv_port":""}')
        json.dump(data, f, indent=4)
    

    # Run Appropriate Processes
    establish_mavlink_connection()
    if args.ir:
        init_ir_threads()
    elif args.source:
        init_source_threads
    elif args.generate:
        do_kml_generation()
    elif args.transmit:
        do_kml_transmit()
        

    save_state()
    print('Program ended.')




if __name__ == '__main__':
    main()