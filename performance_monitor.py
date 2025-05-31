import pyodbc
import psutil
import time
from datetime import datetime

# Database connection using Windows Authentication
conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=Praveen\SQLEXPRESS;'  # Change if necessary
                      'DATABASE=System_Information;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

# Function to collect system performance data and insert into MSSQL
def insert_performance_data():
    while True:
        current_time = datetime.now()
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        cpu_interrupts = psutil.cpu_stats().interrupts
        cpu_calls = psutil.cpu_stats().syscalls
        memory_used = psutil.virtual_memory().used
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_received = net_io.bytes_recv
        disk_usage = psutil.disk_usage('/').percent

        # SQL query to insert performance data
        query = """INSERT INTO dbo.performance 
                   (Time, cpu_usage, memory_usage, cpu_interrupts, cpu_calls, memory_used, bytes_sent, bytes_received, disk_usage)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        values = (current_time, cpu_usage, memory_usage, cpu_interrupts, cpu_calls, memory_used, bytes_sent, bytes_received, disk_usage)

        # Execute the query and commit changes
        cursor.execute(query, values)
        conn.commit()

        print(f"Inserted: Time={current_time}, CPU={cpu_usage}%, Memory={memory_usage}%, Disk={disk_usage}%, Sent={bytes_sent}B, Received={bytes_received}B")

        time.sleep(1)  # Collect data every 5 seconds

# Start the monitoring function
insert_performance_data()
