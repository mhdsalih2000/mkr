import pvlib
import pandas as pd
import numpy as np
import pytz
from datetime import datetime
from const import MotorSpec ,data
from utils import calculate_pdc, find_current, find_motor_volatage, find_motorFreq, outputPower, findOutputV
from openwether import get_weather_by_coordinates

def calculate_ghi_with_weather_now(data, imei,model='ineichen', npanel=0.11):
    try:

        if imei not in MotorSpec:
            raise ValueError(f"Invalid IMEI: {imei} - No motor specifications found.")
        
        motor_spec = MotorSpec[imei]
        hp = int(motor_spec["hp"])
        latitude =  float(motor_spec["latitude"])
        longitude = float(motor_spec["longitude"])

        wether_data = get_weather_by_coordinates(latitude , longitude)
        temperature = wether_data["temperature"]
        cloudPercentage = wether_data["clouds"]
        print("cloud" ,cloudPercentage)
        print("temperature" ,temperature)

        if hp == 2:
            datas = data[0]["2hp"]
        elif hp == 3:
            datas = data[0]["3hp"]
        elif hp == 5:
            datas = data[0]['5hp']
        elif hp == 75:
            datas = data[0]['75hp']
        elif hp == 10:
            datas = data[0]['10hp']
        else:
            raise ValueError(f"Unsupported horsepower: {hp}")


        utc_now = datetime.now(pytz.utc)
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
        solar_position = pvlib.solarposition.get_solarposition(ist_now, latitude, longitude)
        solar_azimuth = solar_position['apparent_zenith'].apply(lambda x: x - 180 if x > 90 else x)
        print("Solar azimuth:", solar_azimuth)

        if model == 'ineichen':
            ghi_clearsky = pvlib.clearsky.ineichen(solar_azimuth, latitude, linke_turbidity=1)
        elif model == 'reindl':
            ghi_clearsky = pvlib.clearsky.reindl(solar_position['apparent_zenith'], latitude, linke_turbidity=2)
        elif model == 'hottel':
            ghi_clearsky = pvlib.clearsky.hottel(solar_position['apparent_zenith'], latitude, linke_turbidity=2)
        else:
            raise ValueError("Invalid model name. Choose 'ineichen', 'reindl', or 'hottel'.")

        clearSky_ghi = float(ghi_clearsky["ghi"].iloc[0])
        print(clearSky_ghi)
        temperature_effect = 1 - 0.01 * (temperature - 20)
        cloudCoverFactor = 1 - (cloudPercentage / 100)
        
        cloudySky_ghi  = clearSky_ghi*  temperature_effect
        print("cloudy ghi ",cloudySky_ghi )
        print("Temperature effect:", temperature_effect)
        print("cloud cover factor",cloudCoverFactor)

        if cloudySky_ghi == 0 :
            res = [
                {
                "date": ist_now,
                "latitude":str(latitude) ,
                "longitude":str(longitude) ,
                "hp" :f"{motor_spec['hp']}hp",
                "input power": 0 ,
                "Panel Voltage": 0,
                "clearSky ghi": clearSky_ghi,
                "cloudy ghi": cloudySky_ghi ,
                "motorVoltage": 0 ,
                "motorFreq": 0 ,
                "Input current": 0 ,
                "output Power": 0,
                "output Voltage": 0,
                "motorVoltage":0
            }]
            return res
        
        ghi_clearsky_array = np.array(ghi_clearsky)
        if ghi_clearsky_array is not None:
            ghi = ghi_clearsky_array[0][0]  
            cloudy_ghi = cloudySky_ghi
            
        else:
            ghi = None
            cloudy_ghi = None

        if cloudy_ghi:
            pdc = calculate_pdc((700 - cloudy_ghi), npanel, RatedPanelPower=datas["RATED-PANEL-POWER"])

        if cloudy_ghi:
            motorVolatge = find_motor_volatage(nominalvoltage=datas["PANEL-VOLTAGE"], ghi=(700 - cloudy_ghi))
            motorFrq = find_motorFreq(pdc, ratedPanelPower=datas["RATED-PANEL-POWER"], max_freq=datas["MOTOR-FREQ"])

        if pdc:
            current = find_current(pdc, ratedPanelPower=datas["RATED-PANEL-POWER"], motorVolatge=motorVolatge)
            output_power = outputPower(pdc)

        if output_power:
            outputV = findOutputV(pdc, datas["RATED-PANEL-POWER"], datas["DRIVE-OUTPUT-V"])
        else:
            outputV = None

        if outputV and outputV > motorVolatge:
            motorVolatge = outputV        
        res = [{
                "date": ist_now,
                "latitude":str(latitude) ,
                "longitude":str(longitude) ,
                "hp": f"{motor_spec['hp']}hp",
                "input power": round(pdc, 3) if pdc is not None else None,
                "clearSky ghi": round(ghi, 3) if ghi is not None else None,
                "cloudy ghi": round(cloudy_ghi, 3) if cloudy_ghi is not None else None,
                "Panel Voltage": round(motorVolatge, 3) if motorVolatge is not None else None,
                "motorFreq": round(motorFrq, 3) if motorFrq is not None else None,
                "Input current": round(current, 3) if current is not None else None,
                "output Power": round(output_power, 3) if output_power is not None else None,
                "motorVoltage": round(outputV, 3) if outputV is not None else None,
                
            }]
        return res

    except KeyError as e:
        print(f"KeyError: Missing required data for IMEI {imei}: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except TypeError as e:
        print(f"TypeError: Incompatible data type encountered: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


