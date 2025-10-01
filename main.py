# main.py

from monitor import run_real_time_monitor

if __name__ == "__main__":
    # Start the real-time monitoring system
    # Interval set to 5 seconds for immediate demonstration. 
    # In a real environment, this would be 300 (5 minutes) or more.
    run_real_time_monitor(interval_seconds=5)