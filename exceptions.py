# exceptions.py

class DataIntegrityError(Exception):
    """Custom exception for errors related to missing or corrupted source data."""
    def __init__(self, message, project_id=None):
        self.message = message
        self.project_id = project_id
        super().__init__(self.message)

class ContractComplianceError(Exception):
    """Custom exception for a critical mismatch between log data and contract rules."""
    def __init__(self, message, log_id):
        self.message = message
        self.log_id = log_id
        super().__init__(self.message)