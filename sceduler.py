import schedule
import time
from datetime import datetime
import pytz  
from main import MqttClient
from const import data , imei_pass

IST = pytz.timezone("Asia/Kolkata")

def my_job():
    now_ist = datetime.now(IST)
    print(f"Job started at: {now_ist.strftime('%Y-%m-%d %H:%M:%S')}")
    mqttclinet = MqttClient(data , imei_pass)
    mqttclinet.bulk_publish()
    print(f"Job complieted at: {now_ist.strftime('%Y-%m-%d %H:%M:%S')}")

def conditional_job():
    now_ist = datetime.now(IST)
    if 8 <= now_ist.hour < 17:  
        my_job()
schedule.every(15).minutes.do(conditional_job)
print("Scheduler started. Press Ctrl+C to exit.")
while True:
    schedule.run_pending()
    time.sleep(1)

