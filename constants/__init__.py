import os

# Get the directory of the current file (constants/__init__.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMPLOYEE_DATA_PATH = os.path.join(BASE_DIR, r'..\models\employee.json')