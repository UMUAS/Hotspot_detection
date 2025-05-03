import socket


def do_kml_transmit():
    global data 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print('[i] Attempting to send KML file...')
            sock.bind((data["serv_add"], data["serv_port"]))
            sock.listen()
            conn, addr = sock.accept()
            with conn:
                print(f'[o] Connected to receiver at {addr}')
                with open(data["kml_file_path"],"rb") as f: 
                    #send kml file in lines
                    lines = f.readlines()
                    for i in lines: 
                        conn.send(i)
        print('[o] KML file sent successfuly')
    except:
        print('[x] Failed to send KML file')



        
