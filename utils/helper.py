from constants import EMPLOYEE_DATA_PATH
import json

def read_emp_data():
    with open(EMPLOYEE_DATA_PATH, 'r') as f:
        emp_data = json.load(f)
    return emp_data