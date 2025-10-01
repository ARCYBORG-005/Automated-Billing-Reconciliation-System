# data_simulator.py

import pandas as pd

# The erroneous line has been removed. 
# Your code should now execute without a Line 2 import error.

def get_real_time_time_logs(cycle_count=0):
    """
    Simulates fetching the latest time logs from the Time Tracking System.
    Cycle_count=2 simulates a critical API failure (empty data).
    """
    if cycle_count == 2:
        print("-> ALERT: Data feed connection simulating loss for DataIntegrityError test.")
        return pd.DataFrame() 

    print("-> Fetching real-time time logs...")
    
    # Base Logs
    time_logs = pd.DataFrame({
        'Log_ID': [101, 102, 103, 104, 105, 106, 107],
        'Project_ID': ['P001', 'P001', 'P002', 'P002', 'P001', 'P003', 'P002'],
        'Employee_ID': ['E45', 'E45', 'E12', 'E12', 'E45', 'E90', 'E12'],
        'Hours': [8.0, 4.0, 7.5, 6.0, 2.0, 8.0, 3.0],
        'Activity_Type': ['Billable', 'Non-Billable', 'Billable', 'Billable', 'Billable', 'Billable', 'Billable'],
        'Invoicing_Status': ['Logged', 'Logged', 'Logged', 'Logged', 'Logged', 'Logged', 'Logged'],
        'Expense_Check': [False, False, False, False, True, False, False] 
    })
    
    # Edge Case: Log 110 has no Project_ID (simulating bad data entry)
    edge_log = pd.DataFrame({
        'Log_ID': [110],
        'Project_ID': [None],
        'Employee_ID': ['E50'],
        'Hours': [2.0],
        'Activity_Type': ['Billable'],
        'Invoicing_Status': ['Logged'],
        'Expense_Check': [False]
    })
    
    return pd.concat([time_logs, edge_log], ignore_index=True)

def get_master_contract_rules():
    """
    Simulates fetching standardized billing rules from the ERP/Contract Database.
    """
    print("-> Fetching master contract rules...")
    contract_rules = pd.DataFrame({
        'Project_ID': ['P001', 'P002', 'P003'],
        'Client_Name': ['TechSolutions Inc.', 'Global Commerce', 'Innovation Hub'],
        'Client_Rate_per_Hour': [150.00, 120.00, 180.00],
        'Billing_Model': ['T&M', 'T&M', 'Fixed-Price'], 
        'Reimbursable_Limit': [500.00, 1000.00, 0.00],
        'Max_FP_Hours': [None, None, 100]
    })
    return contract_rules

def get_new_log_entries(current_log_count):
    """
    Simulates new high-value logs entering the system after the initial cycle.
    """
    if current_log_count >= 8:
        new_logs = pd.DataFrame({
            'Log_ID': [108, 109],
            'Project_ID': ['P001', 'P002'],
            'Employee_ID': ['E45', 'E12'],
            'Hours': [5.0, 4.0],
            'Activity_Type': ['Billable', 'Billable'],
            'Invoicing_Status': ['Logged', 'Logged'],
            'Expense_Check': [False, False]
        })
        return new_logs
    return pd.DataFrame()