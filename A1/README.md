# A1 - Building a Model for the Synthesis of Tabular Healthcare Data


## Jupyter notebook

This notebook presents a synthetic data generation approach for medical exam results based on the normal distribution. The goal is to create realistic artificial blood test data while preserving the statistical properties of the original dataset.

First, the statistical characteristics of the real dataset are analyzed, including measures such as mean and standard deviation for each laboratory exam. These parameters are then used to generate synthetic samples drawn from normal distributions that approximate the original data.

To evaluate whether the generated data is realistic, several statistical comparison methods are applied between the real and synthetic datasets. These include histogram comparison, Kernel Density Estimation (KDE) for distribution visualization, Cumulative Distribution Functions (CDF), and the Kolmogorov–Smirnov (KS) statistical test, which measures the similarity between the two distributions.

Using this approach, the notebook generates a synthetic dataset containing 1000 fictitious blood exam records. The analysis shows that the generated samples closely follow the statistical behavior of the original data, making them suitable for experimentation, testing, or machine learning tasks without exposing real patient information.

## CSV to JSON converter

### Objective

This script converts multiple CSV files containing medical exam records into a structured JSON dataset grouped by patient ID. The tool scans a directory for CSV files, reads the exam data, and produces a single JSON file where each patient has their demographic information and exam results organized in a structured format.

### Expected CSV format

Each CSV row must contain six columns in the following order:

date, age, patient_id, sex, exam_name, exam_value

Example:
```
2024-01-10,45,12345,M,Glucose,92
2024-01-10,45,12345,M,Cholesterol,180
2024-02-02,52,67890,F,Glucose,105
```

### Output JSON structure

The output JSON groups exams by patient ID.

Example output:

```
{
  "12345": {
    "date": "2024-01-10",
    "sex": "M",
    "age": 45,
    "exams": {
      "Glucose": 92.0,
      "Cholesterol": 180.0
    }
  }
}
```

Notes

* Exam values are converted to floating-point numbers.

* Empty values are stored as null.

* If multiple CSV files contain exams for the same patient, they are merged.

### How to use

Run the script from the command line:

``` python convert_csv_to_json.py <input_directory> ```

Example:

``` python convert_csv_to_json.py ./exam_csvs ```

This will generate:

exam_csvs/data.json

Or you can specify a custom output file:

``` python convert_csv_to_json.py ./exam_csvs --output dataset.json ```

Example:

``` python convert_csv_to_json.py ./data --output ./output/patient_dataset.json ```