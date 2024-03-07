import schedule
import time

def main():
    # Define the time of the day when you want the process to run
    scheduled_time = "11:18"  # Adjust this according to your requirement
    
    # Schedule the process to run daily at the specified time
    schedule.every().day.at(scheduled_time).do(run_process)
    
    # Infinite loop to keep the program running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check for scheduled tasks every 60 seconds

def run_process():
    # Call your main function here or the function that starts your process
    print("Hello")

if __name__ == '__main__':
    main()
