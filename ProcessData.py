from datetime import datetime
import pytz
from pvlib1 import calculate_ghi_with_weather_now
from utils import findlpm
from db import update_row , create_row, reset_column_values_to_zero, get_column_values_by_imei
from random import randint
from const import Statuses

def getTimeandDate():
    ist = pytz.timezone('Asia/Kolkata')  
    now = datetime.now(ist)  
    today = now.date()
    current_tm = now.time()
    shortyear = today.year % 100
    formatted_date = f"{shortyear}{today.month:02d}{today.day:02d}"
    formatted_time = f"{current_tm.hour:02d}{current_tm.minute:02d}{current_tm.second:02d}"
    formatedVd1date= f"{today.year}-{today.month:02d}-{today.day:02d}"
    formatedDateTime = f"{formatedVd1date} {current_tm.hour:02d}:{current_tm.minute:02d}:{current_tm.second:02d}"
    RTCTIME = f"{current_tm.hour:02d}:{current_tm.minute:02d}:{current_tm.second:02d}"
    Timedate = {
          "DATE":formatedVd1date ,
          "RTCDATE" : formatted_date, 
          "TIME": formatted_time ,
          "FORMATEDDATETIME" :formatedDateTime,
          "RTCTIME" :RTCTIME

          }
    return Timedate



def get_vd1_vd0( data ,imei , session ):
      motordatas = calculate_ghi_with_weather_now(data , imei )
      print(motordatas)
      motordata  = motordatas[0]
      hp = motordata["hp"]
      timeDate = getTimeandDate()
      outputPowerinKW = motordata["output Power"]/1000
      lpm = findlpm(motordata["input power"], data[0][hp]["RATED-PANEL-POWER"],data[0][hp]["MAX-FLOW"])
      if motordata['cloudy ghi'] < 200:
            runstatus = 1

      create_value = {
                    "daily_water_discharge": 0 ,
                    "cumulative_water_discharge": 0,
                    "day_run_hours": 0 ,
                    "cumulative_run_hours": 0,
                    "cumulative_energy_generated": 0 ,
                    "run_status":randint(1, 787)
                    }
      values = create_row(session , imei , create_value)
      if values["run_status"] == 787:
            reset_column_values_to_zero(session , ["run_status"], imei)

      runstatus = Statuses[values["run_status"]]
      if runstatus == 1:
            column_value = {
                    "daily_water_discharge": lpm * 15,
                    "cumulative_water_discharge": lpm * 15,
                    "day_run_hours": 0.25,
                    "cumulative_run_hours": 0.25,
                    "cumulative_energy_generated": outputPowerinKW ,
                    "run_status" : 1
                    }
            if session:
                  result = update_row(session, imei ,column_value)
            mqtt_payloadvd1 = {
                "VD": "1",
                "TIMESTAMP": f"{timeDate['FORMATEDDATETIME']}",  
                "DATE": f"{timeDate['RTCDATE']}",   
                "IMEI":f"{imei}", 
                "PDKWH1": f"{round(outputPowerinKW,3)}", 
                "PTOTKWH1": f"{round(result['cumulative_energy_generated'],3)}",
                "POPDWD1":f"{round(result['daily_water_discharge'],3)}",  
                "POPTOTWD1": f"{round(result['cumulative_water_discharge'],3)}",
                "PDHR1": f"{round(result['day_run_hours'],3)}", 
                "PTOTHR1": f"{round(result['cumulative_run_hours'],3)}",
                "POPKW1":f"{round(outputPowerinKW,3)}",                          
                "MAXINDEX": "0",
                "INDEX": "0",
                "LOAD": "0",
                "STINTERVAL": "15",
                "POTP": "542154",
                "COTP": "123456",
                "PMAXFREQ1":f"{data[0][hp]['MOTOR-FREQ']}",    
                "PFREQLSP1": "50",
                "PFREQHSP1": "110",
                "PCNTRMODE1": "0",
                "PRUNST1": "1",
                "POPFREQ1": f"{motordata['motorFreq']}",    
                "POPI1":f"{motordata['Input current']}",      
                "POPV1": f"{motordata['motorVoltage']}",      
                "PDC1V1": f"{motordata['Panel Voltage']}",      
                "PDC1I1": f"{motordata['Input current']}",     
                "PDCVOC1": f"{motordata['Panel Voltage']}",  
                "POPFLW1": f"{lpm}"    
              }  

            mqtt_payloadvd0={
                "VD": "0",
                "TIMESTAMP": f"{timeDate['FORMATEDDATETIME']}",     
                "DATE":f"{timeDate['RTCDATE']}",                       
                "IMEI": f"{imei}",             
                "RTCDATE": f"{ timeDate['RTCDATE']}",  
                "RTCTIME": f"{timeDate['RTCTIME']}", 
                "LAT": motordata["latitude"],  
                "LONG": motordata["longitude"], 
                "RSSI": "19",         
                "STINTERVAL": "15",
                "POTP": "0",
                "COTP": "0",
                "GSM": "1",
                "SIM": "1",
                "NET": "1",
                "GPRS": "1",
                "SD": "0",
                "ONLINE": "1",
                "GPS": "1",
                "GPSLOC": "1",
                "RF": "1",
                "TEMP": "25.10",
                "SIMSLOT": "1",
                "SIMCHNGCNT": "0",
                "FLASH": "1",
                "BATTST": "1",
                "VBATT": 3.32,   
                "PST": 1  
              }
      else: 
            update_row(session, imei ,{"run_status" : 1})
            mqtt_payloadvd1 = {
                "VD": "1",
                "TIMESTAMP": f"{timeDate['FORMATEDDATETIME']}",  
                "DATE": f"{timeDate['RTCDATE']}",   
                "IMEI":f"{imei}", 
                "PDKWH1": "0", 
                "PTOTKWH1": "0",
                "POPDWD1":"0",  
                "POPTOTWD1": "0",
                "PDHR1": "0", 
                "PTOTHR1": "0",
                "POPKW1":"0",                          
                "MAXINDEX": "0",
                "INDEX": "0",
                "LOAD": "0",
                "STINTERVAL": "15",
                "POTP": "542154",
                "COTP": "123456",
                "PMAXFREQ1":"0",    
                "PFREQLSP1": "50",
                "PFREQHSP1": "110",
                "PCNTRMODE1": "0",
                "PRUNST1": runstatus,
                "POPFREQ1": "0",    
                "POPI1":"0",      
                "POPV1": f"{motordata['motorVoltage']}",      
                "PDC1V1": f"{motordata['Panel Voltage']}",      
                "PDC1I1": "0",     
                "PDCVOC1": f"{motordata['Panel Voltage']}",  
                "POPFLW1": "0"
            }     
            mqtt_payloadvd0={
                  "VD": "0",
                "TIMESTAMP": f"{timeDate['FORMATEDDATETIME']}",     
                "DATE":f"{timeDate['RTCDATE']}",                       
                "IMEI": f"{imei}",             
                "RTCDATE": f"{ timeDate['RTCDATE']}",  
                "RTCTIME": f"{timeDate['RTCTIME']}", 
                "LAT": motordata["latitude"],  
                "LONG": motordata["longitude"], 
                "RSSI": "19",         
                "STINTERVAL": "15",
                "POTP": "0",
                "COTP": "0",
                "GSM": "1",
                "SIM": "1",
                "NET": "1",
                "GPRS": "1",
                "SD": "0",
                "ONLINE": "1",
                "GPS": "1",
                "GPSLOC": "1",
                "RF": "1",
                "TEMP": "25.10",
                "SIMSLOT": "1",
                "SIMCHNGCNT": "0",
                "FLASH": "1",
                "BATTST": "1",
                "VBATT": 3.32,   
                "PST": 1  
                }
      return mqtt_payloadvd0 , mqtt_payloadvd1

