import json
from j2on import data
def extract_imei_and_password(data):
    result = {}
    for item in data:
        result[item["imeiNo"]] = item["password"]

    file_name = "IMEI_Password.json"
    with open(file_name, "w") as json_file:
        json.dump(result, json_file, indent=2) 

    print(f"JSON file created: {file_name}")

extract_imei_and_password(data)

import json



def create_motor_spec(data):
    motor_spec = {}
    for item in data:
        # Normalize HP values: 7.5 to 75, and 5.0 to 5
        if item["motorhp"] == 7.5:
            hp_value = 75
        elif item["motorhp"] == 5.0:
            hp_value = 5
        elif item["motorhp"] == 3.0:
            hp_value = 3
        elif item["motorhp"] == 2.0:
            hp_value = 2
        else:
            hp_value = item["motorhp"]
        
        motor_spec[item["imeiNo"]] = {
            "latitude": item["lat"],
            "longitude": item["long"],
            "hp": hp_value,# Static or default value
            "password": item["password"]
        }

    
    file_name = "MotorSpec.json"
    with open(file_name, "w") as json_file:
        json.dump(motor_spec, json_file, indent=2)  # Pretty print JSON

    print(f"JSON file created: {file_name}")


create_motor_spec(data)