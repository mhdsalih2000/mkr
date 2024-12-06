import schedule
import time
from datetime import datetime
import pytz
from main import MqttClient
from const import data, imei_pass
from db import establish_db_connection ,reset_column_values_to_zero

IST = pytz.timezone("Asia/Kolkata")

def my_job():
    now_ist = datetime.now(IST)
    print(f"Job started at: {now_ist.strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = time.time()
    mqttclinet = MqttClient(data, imei_pass)
    mqttclinet.bulk_publish()
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Job completed at: {now_ist.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time taken for the job: {duration:.2f} seconds")

def conditional_job():
    now_ist = datetime.now(IST)
    if 8 <= now_ist.hour < 17:  
        my_job()

def evening_job():
    enging ,session = establish_db_connection()
    reset_column_values_to_zero(session)




if __name__ == "__main__":
    schedule.every(5).seconds.do(conditional_job)
    schedule.every().day.at("18:00").do(evening_job)
    print("Scheduler started. Press Ctrl+C to exit.")


    while True:
        schedule.run_pending()
        time.sleep(1)
