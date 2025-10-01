
# Automated Billing Reconciliation (ABR) System
 

This project is a **low-latency, event-driven monitoring service** designed to automatically detect and flag **revenue leakage** (unbilled hours) against Time & Materials (T\&M) client contracts.

The system's core value is its ability to immediately identify unbilled revenue that exceeds a critical financial threshold (default: **$1500.00**) and present an **actionable, color-coded alert** directly in the console, drastically improving cash flow and financial compliance.

-----

##  Key Features & Value Proposition

| Feature | Business Value |
| :--- | :--- |
| **Real-Time Monitoring** | Runs continuously, checking for leakage every **5 seconds**—enabling same-day invoicing. |
| **Graceful Failure** | Uses custom exceptions to log a **CRITICAL ERROR (HALT)** and shut down cleanly if the data source fails, protecting financial data integrity. |
| **Rich Terminal Output** | Utilizes the `rich` library to present highly legible, color-coded tables of leakage, making the output instantly understandable by Finance/Operations teams. |
| **Data Integrity** | Includes a **`⚠ QUARANTINE`** check to isolate invalid logs (e.g., missing Project IDs) without failing the audit process. |

-----

## How to Run the Project (Quick Start)

1. **Activate Environment:** Ensure your virtual environment is active.
    ```bash
    (venv) PS D:\revenue leakage> .\venv\Scripts\Activate.ps1
    ```
2. **Install Dependencies:** Install the required external libraries.
    ```bash
    (venv) PS D:\revenue leakage> pip install pandas rich
    ```
3. **Execute the Monitor:** Run the main orchestrator file.
    ```bash
    (venv) PS D:\revenue leakage> python main.py
    ```

The monitor will begin its continuous audit cycle every 5 seconds.

-----

##  System Architecture (Module Breakdown)

The project follows the principle of **Separation of Concerns**, making it scalable and highly maintainable.

| File | Primary Role | Function Summary |
| :--- | :--- | :--- |
| **`main.py`** |

 **Entry Point** |
  Initiates the monitoring service. |
| **`monitor.py`** | **Service Orchestrator** | Manages the continuous 5-second execution loop (`while True`) and the high-level system error handling. |

| **`reconciliation_engine.py`** |

 **Financial Audit Logic** | **The Brain.** Calculates potential revenue, applies all contract rules, checks the $1500 threshold, and generates the professional `rich` alert table. |

| **`data_simulator.py`**
 | **Data Access Layer** |
  Simulates fetching live **Time Logs** and **Contract Rules** (simulating API calls). |

| **`exceptions.py`** | 
**Error Handling** |
 Defines custom exceptions (`DataIntegrityError`, `ContractComplianceError`) for robust, application-specific error reporting. |
