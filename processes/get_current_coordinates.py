def get_current_coordinates(mavlink_connection):  #should be run as a seperate thread to constantly update current coordinates
    global mavlink_connection
    global  current_coordinates
    while True: 
        msg = mavlink_connection.recv_match()
        if not msg:
            continue
        if msg.get_type() == "GLOBAL_POSITION_INT":
           latitude = msg.lat
           longitude = msg.lon 
           current_coordinates = (latitude,longitude)

