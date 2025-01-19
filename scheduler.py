import schedule
import time
from app import dump_data_in_chunks  # import the function from app.py

# define the job that calls dump_data_in_chunks
def job():
    print("Refreshing data...")
    dump_data_in_chunks()

# schedule the job to run at midnight every day
schedule.every().day.at("00:00").do(job)

# keep the script running to maintain the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
