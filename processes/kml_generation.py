import simplekml 
def do_kml_generation():
    global data 
    try:
        kml = simplekml.Kml()
        for  i in range(len(data["hotspots"])):
            kml.newpoint(name =f"Hotspot {i}", coords=[data["hotspots"][i]])
            kml.newpoint(name="Fire source", coords = [data["source"]["coordinates"]], description=data["source"]["description"])
        kml.save(data["kml_file_path"])
        print(f"[o] kml file saved to -> {data["kml_file_path"]}")
    except:
        print("[x] Error occured generating kml file")


    