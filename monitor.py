# monitor.py (MODIFIED to Display Rich Output)

import time
import pandas as pd
from datetime import datetime
import sys 
from data_simulator import get_real_time_time_logs, get_master_contract_rules, get_new_log_entries
from reconciliation_engine import run_billing_reconciliation, generate_alert_summary
from exceptions import DataIntegrityError, ContractComplianceError 
# NEW IMPORT
from rich.console import Console

# Initialize Rich Console for printing
console = Console()

# Set display options for professional table formatting
pd.set_option('display.float_format', lambda x: '%.2f' % x) 
pd.set_option('display.max_columns', None)

def run_real_time_monitor(interval_seconds=5, alert_threshold=1500.00):
    """
    Runs the ABR check every 'interval_seconds' to simulate a real-time system.
    """
    
    print(f"** ABR Real-Time Monitor Started ** (Checking every {interval_seconds} seconds)")
    
    # 1. Initialize Master Data and Initial Time Logs
    contract_data = get_master_contract_rules()
    
    # Load initial data
    current_time_logs = get_real_time_time_logs(cycle_count=0)
    
    log_counter = len(current_time_logs)
    cycle_count = 0
    
    while True:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n\n--- RECONCILIATION CYCLE START @ {timestamp} (Cycle: {cycle_count}) ---")
        
        try:
            # 2. Simulate New Data Ingestion (Dynamic Update)
            if cycle_count > 0:
                # Check for critical errors (Cycle 2 simulates a fail)
                new_logs_base = get_real_time_time_logs(cycle_count)
                
                if new_logs_base.empty and cycle_count == 2:
                    raise DataIntegrityError("Critical API failure: Empty response from time-tracking system.")

                # If no critical error, check for new hourly entries
                new_entries = get_new_log_entries(log_counter) 
                if not new_entries.empty:
                    current_time_logs = pd.concat([current_time_logs, new_entries], ignore_index=True)
                    log_counter += len(new_entries)
                    print(f"** New {len(new_entries)} log(s) added to system for reconciliation. **")


            # 3. Run Core Financial Audit Logic
            time_leakage_df, compliance_df = run_billing_reconciliation(current_time_logs, contract_data)
            
            # 4. Generate Alert (Runs only if ABR completes successfully)
            #  CHANGE: Function now returns a 4th argument: alert_table
            summary_df, alert_df, alert_msg, alert_table = generate_alert_summary(time_leakage_df, compliance_df, alert_threshold)
            
            # Print the text alert message (using rich markup for color/bolding)
            console.print(alert_msg)

            if not alert_df.empty:
                #  CHANGE: Use the console.print() method to render the professional table
                console.print(alert_table) 
                print("\n Action: Notification sent to Finance and PM for immediate invoicing.")

        # --- GRACEFUL ERROR HANDLING BLOCK ---
        except DataIntegrityError as e:
            # Use console.print for colored error message
            console.print(f"\n\n[bold white on red]=======================================================[/bold white on red]")
            console.print(f"[bold red] CRITICAL ERROR (HALT):[/bold red] [red]{e.message}[/red]")
            console.print(f"[bold white on red]=======================================================[/bold white on red]")
            sys.stdout.flush() 
            break 

        except ContractComplianceError as e:
            # Use console.print for colored warning
            console.print(f"\n\n[bold white on yellow]-------------------------------------------------------[/bold white on yellow]")
            console.print(f"[bold yellow]PROFITABILITY WARNING:[/bold yellow] [yellow]{e.message}[/yellow]")
            print("Action: Notification sent to Financial Controller for gross margin review.")
            console.print(f"[bold white on yellow]-------------------------------------------------------[/bold white on yellow]")

        except Exception as e:
            console.print(f" [bold red]UNEXPECTED SYSTEM ERROR:[/bold red] {str(e)}. The monitor will continue...")

        print(f"\n--- RECONCILIATION CYCLE END @ {timestamp} ---")
        
        cycle_count += 1
        time.sleep(interval_seconds)

if __name__ == "__main__":
    run_real_time_monitor(interval_seconds=5)