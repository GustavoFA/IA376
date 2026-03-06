import os
import argparse
import pandas as pd


def find_csv_files(directory):
    """
    Recursively search for all CSV files inside a directory.
    Returns a list with the full path of each CSV file found.
    """
    csv_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    return csv_files


def main():

    parser = argparse.ArgumentParser(
        description="Merge all CSV files from a directory into a single CSV file"
    )

    parser.add_argument(
        "input_dir",
        help="Directory containing CSV files"
    )

    parser.add_argument(
        "output_csv",
        nargs="?",  # Makes this argument optional
        default=None,
        help="Optional path for the merged CSV file"
    )

    args = parser.parse_args()

    input_dir = args.input_dir
    output_csv = args.output_csv

    # Check if the input directory exists
    if not os.path.isdir(input_dir):
        raise ValueError(f"Input directory does not exist: {input_dir}")

    # If no output path is provided, save inside input directory
    if output_csv is None:
        output_csv = os.path.join(input_dir, "full_data.csv")

    # Find all CSV files
    csv_files = find_csv_files(input_dir)

    if not csv_files:
        raise RuntimeError("No CSV files found in the provided directory.")

    print(f"Found {len(csv_files)} CSV files")

    dfs = []

    # Load each CSV file
    for file in csv_files:

        print(f"Reading: {file}")

        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except Exception as e:
            print(f"Skipping {file} due to error: {e}")

    if not dfs:
        raise RuntimeError("No CSV files could be loaded.")

    # Concatenate all DataFrames
    df_final = pd.concat(dfs, ignore_index=True)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_csv)

    if output_dir != "":
        os.makedirs(output_dir, exist_ok=True)

    # Save the merged CSV
    df_final.to_csv(output_csv, index=False)

    print(f"\nMerged CSV saved at: {output_csv}")


if __name__ == "__main__":
    main()