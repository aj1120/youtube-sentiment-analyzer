import subprocess
import time
import os
import threading

def run_script(script_name):
    subprocess.run(["python", script_name])

# Run each component in a separate thread or process
threads = []

# Start producer
t1 = threading.Thread(target=run_script, args=("producer.py",))
threads.append(t1)

# Start consumer
t2 = threading.Thread(target=run_script, args=("consumer.py",))
threads.append(t2)

# Start real-time sentiment analysis
t3 = threading.Thread(target=run_script, args=("sentiment_analysis.py",))
threads.append(t3)

# Start all threads
for t in threads:
    t.start()

# Wait a bit for everything to boot
time.sleep(10)

# Open Power BI dashboard
dashboard_path = r"C:\Users\AJIT\Documents\ajit_project1.pbix"
os.system(f'start "" "{dashboard_path}"')

# Wait for all threads to finish (optional)
for t in threads:
    t.join()
