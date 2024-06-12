import os
import subprocess
import sys

def test_pipeline_execution():
    data_dir = r"D:\Summer 2024\Methods of Advanced Data Engineering (MADE)\Exercise_main\MADE_SS2024\data"
    input_files = [
        os.path.join(data_dir, 'greenhouse_gas_inventory_data_data.csv'),
        os.path.join(data_dir, 'seaice.csv')
    ]

    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"Test failed: Input file {input_file} does not exist.")
            sys.exit(1)
    print("Test passed: All input files exist.")

    result = subprocess.run([sys.executable, 'pipeline.py'], capture_output=True, text=True)

    assert result.returncode == 0, f"Test failed: Pipeline execution failed: {result.stderr}"
    print("Test passed: Pipeline executed successfully.")

    sqlite_db_path = os.path.join(data_dir, 'climate_data.db')
    assert os.path.exists(sqlite_db_path), f"Test failed: SQLite database {sqlite_db_path} does not exist"
    print(f"Test passed: SQLite database {sqlite_db_path} exists.")

    print("All tests passed.")

if __name__ == "__main__":
    test_pipeline_execution()
