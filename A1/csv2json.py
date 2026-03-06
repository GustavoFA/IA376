import os
import csv
import json
import argparse
from pathlib import Path


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Convert CSV exam files into a structured JSON dataset.")

    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory containing CSV files"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Output JSON file path (optional). If empty, saves as data.json in the input directory."
    )

    return parser.parse_args()


def get_csv_files(directory):
    """
    Scan the directory and return all CSV files.
    """
    csv_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    return csv_files


def process_csv_files(csv_files):
    """
    Read all CSV files and build the JSON structure grouped by patient.
    """
    data = {}

    for csv_file in csv_files:

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) < 6:
                    continue

                date, age, patient_id, sex, exam_name, exam_value = row

                # Create patient entry if it does not exist
                if patient_id not in data:
                    data[patient_id] = {
                        "date": date,
                        "sex": sex,
                        "age": int(age) if age else None,
                        "exams": {}
                    }

                # Clean the value (remove spaces and quotes)
                exam_value = exam_value.strip()

                # Handle empty or missing values
                if exam_value == "":
                     value = None
                else:
                     try:
                        value = float(exam_value.replace(",", "."))
                     except ValueError:
                         value = None

                # Store exam result
                data[patient_id]["exams"][exam_name] = value

    return data


def main():

    args = parse_args()

    input_dir = args.input_dir
    output_path = args.output

    if not os.path.isdir(input_dir):
        raise ValueError(f"Input directory does not exist: {input_dir}")

    # If output path is empty, save JSON in the input directory
    if output_path == "" or output_path is None:
        output_path = os.path.join(input_dir, "data.json")

    csv_files = get_csv_files(input_dir)

    if len(csv_files) == 0:
        raise ValueError("No CSV files found in the directory.")

    print(f"Found {len(csv_files)} CSV files.")

    dataset = process_csv_files(csv_files)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print(f"JSON saved to: {output_path}")


if __name__ == "__main__":
    main()