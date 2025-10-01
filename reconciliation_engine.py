# reconciliation_engine.py (MODIFIED for Rich Output)

import pandas as pd
from datetime import date
from exceptions import DataIntegrityError, ContractComplianceError
# NEW IMPORTS for rich formatting
from rich.console import Console
from rich.table import Table

# Initialize Rich Console (used for printing tables and styling)
console = Console()

def run_billing_reconciliation(time_logs_df, contract_rules_df):
    """
    Performs the Automated Billing Reconciliation (ABR) audit with robust edge case handling.
    """
    print("\n-> Running ABR Engine: Robust Audit in Progress...")
    
    # --- EDGE CASE 1: Handle Null or Missing Data ---
    if time_logs_df.empty or contract_rules_df.empty:
        raise DataIntegrityError("One or both source data feeds were empty. Cannot reconcile.")

    # 1. MERGE: Combine operational data with financial rules
    df_merged = pd.merge(time_logs_df, contract_rules_df, on='Project_ID', how='left', indicator=True)
    
    # --- EDGE CASE 2: Handle Logs with Unknown Project ID (Missing Contract) ---
    unknown_projects = df_merged[df_merged['_merge'] == 'left_only']
    if not unknown_projects.empty:
        # Quarantine the bad data for manual follow-up, but continue processing valid data
        print(f" QUARANTINE: Found {len(unknown_projects)} log(s) with no matching contract (Missing Project ID).")
        df_merged = df_merged[df_merged['_merge'] == 'both']

    # 2. CALCULATION: Determine potential revenue
    df_merged['Potential_Revenue'] = df_merged.apply(
        lambda row: row['Hours'] * row['Client_Rate_per_Hour']
        if row['Activity_Type'] == 'Billable' and row['Billing_Model'] == 'T&M'
        else 0, axis=1
    )
    
    # 3. LEAKAGE FILTER 1: Time Leakage (Standard T&M)
    time_leakage_condition = (
        (df_merged['Activity_Type'] == 'Billable') & 
        (df_merged['Billing_Model'] == 'T&M') & 
        (df_merged['Invoicing_Status'] == 'Logged')
    )
    time_leakage_report = df_merged[time_leakage_condition]

    # --- EDGE CASE 3: Fixed-Price (FP) Project Overrun (High-Impact Nuance) ---
    fp_projects = df_merged[df_merged['Billing_Model'] == 'Fixed-Price'].dropna(subset=['Max_FP_Hours'])
    fp_project_total = fp_projects.groupby(['Project_ID', 'Max_FP_Hours']).agg(
        Total_Logged_Hours=('Hours', 'sum')
    ).reset_index()
    
    fp_overrun_alerts = fp_project_total[fp_project_total['Total_Logged_Hours'] > fp_project_total['Max_FP_Hours']]

    if not fp_overrun_alerts.empty:
        for index, row in fp_overrun_alerts.iterrows():
            raise ContractComplianceError(
                f"Fixed-Price Overrun: Project {row['Project_ID']} logged {row['Total_Logged_Hours']:.2f} hrs, exceeding the contracted {row['Max_FP_Hours']} hr limit.", 
                log_id="FP-CHECK"
            )
            
    # 4. LEAKAGE FILTER 2: Compliance Leakage (Non-Billable time on T&M)
    compliance_leakage_condition = (
        (df_merged['Activity_Type'] == 'Non-Billable') & 
        (df_merged['Billing_Model'] == 'T&M')
    )
    compliance_report = df_merged[compliance_leakage_condition]
    
    return time_leakage_report, compliance_report

def generate_alert_summary(leakage_df, compliance_df, threshold=1500.00):
    """
    Creates the high-level dashboard summary and returns the RICH Table object if an alert is triggered.
    """
    # 1. Summarize Time Leakage
    summary = leakage_df.groupby(['Project_ID', 'Client_Name']).agg(
        Total_Unbilled_Hours=('Hours', 'sum'),
        Total_Potential_Leakage=('Potential_Revenue', 'sum')
    ).reset_index()

    # 2. Check for Critical Alert
    alerts = summary[summary['Total_Potential_Leakage'] > threshold]

    if not alerts.empty:
        # --- RICH TABLE GENERATION (Professional Output) ---
        alert_message = (
            f"\n [bold red]CRITICAL REAL-TIME LEAKAGE ALERT ({date.today()})[/bold red] 🚨\n"
            "Action Required: Projects below have unbilled T&M revenue exceeding the $"
            f"{threshold:.2f} threshold. [b yellow]Invoice immediately[/b yellow]."
        )
        
        # Configure a professional, color-coded table
        alert_table = Table(
            title="[bold underline]Immediate Action Required Leakage Report[/bold underline]", 
            title_style="bold red", 
            show_header=True, 
            header_style="bold white on blue",
            min_width=80
        )
        
        # Define columns with styles
        alert_table.add_column("Project ID", style="cyan", justify="left")
        alert_table.add_column("Client Name", style="white", justify="left")
        alert_table.add_column("Unbilled Hours", style="magenta", justify="right")
        alert_table.add_column("Leakage (USD)", style="bold yellow on red", justify="right")
        
        # Add rows from the critical alerts DataFrame
        # Sort by leakage amount descending for impact
        sorted_alerts = alerts.sort_values(by='Total_Potential_Leakage', ascending=False)
        for index, row in sorted_alerts.iterrows():
            alert_table.add_row(
                row['Project_ID'],
                row['Client_Name'],
                f"{row['Total_Unbilled_Hours']:.2f}",
                f"${row['Total_Potential_Leakage']:.2f}"
            )
            
        return summary, alerts, alert_message, alert_table # Return the new table object
        
    else:
        alert_message = "\n System Check: No critical revenue leakage detected above the threshold."
        return summary, alerts, alert_message, None
   