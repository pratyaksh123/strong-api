import csv

def read_csv(file_path):
    """Reads a CSV file and returns it as a list of dictionaries."""
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return None  # Return None if file is missing