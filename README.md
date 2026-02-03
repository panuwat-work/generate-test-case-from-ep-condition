# EP Test Case Generator

This tool automates the generation of [Equivalence Partitioning (EP)](https://en.wikipedia.org/wiki/Equivalence_partitioning) test cases from a set of conditions defined in an Excel file. It produces a detailed text-based list of test cases and an interactive HTML matrix for visualization.

## Features

- **Automated EP Generation**: Generates test cases covering valid and invalid partitions using a rotation strategy to ensure coverage while minimizing duplicates.
- **Interactive HTML Matrix**: Produces `ep_matrix.html` with:
  - Color-coded cells (Green for Valid, Red for Invalid).
  - Interactive column highlighting (clicking a column header highlights the relevant cells and EP tags).
  - A dynamic side panel showing detailed conditions for the selected test case.
- **Detailed Text Output**: Exports all generated test cases to `testcase.txt` for easy documentation or manual execution.

## Installation

1. **Prerequisites**: Ensure you have Python 3 installed.

2. **Clone/Download** this project folder.

3. **Install Dependencies**:
   It is recommended to use a virtual environment.
   ```bash
   # Create a virtual environment
   python3 -m venv .venv
   
   # Activate the virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate

   # Install openpyxl
   pip install openpyxl
   ```

## How to Use

1. **Prepare your Input File**:
   - Create an Excel file (e.g., `test2.xlsx` or `Testpythonep.xlsx`).
   - The file must follow a specific column structure (starting from Row 2):
     - **Column A**: Condition Name
     - **Column B**: Valid Description
     - **Column C**: Valid Tag (e.g., `v1`, `v2`...)
     - **Column D**: Invalid Description
     - **Column E**: Invalid Tag (e.g., `x1`, `x2`...)

2. **Configure the Script**:
   Open `EP_generate.py` and set the `FILE_PATH` variable to your Excel filename:
   ```python
   FILE_PATH = "YourExcelFile.xlsx"
   ```

3. **Run the Script**:
   ```bash
   python3 EP_generate.py
   ```

## Output

The script generates two files in the same directory:

### 1. `ep_matrix.html`
An interactive HTML file for visualizing the test cases.
- **Columns**: Represent generated Test Cases (TC1, TC2, ...).
- **Rows**: Represent EP Tags (v1, x1, etc.).
- **Click**: Click on any "TC" header to highlight its column and view details in the side panel.

### 2. `testcase.txt`
A plain text file containing the breakdown of each test case.

**Example Output:**
```text
TC1
  - token: v1 = token ถูกต้อง และ login แล้ว
  - text: v2 = text ตรงกับ product บางส่วน (contain) และมีสินค้า
  - id (product id): v4 = id มีอยู่ใน database

TC2
  - token: v1 = token ถูกต้อง และ login แล้ว
  - text: v3 = text ตรงกับ product บางส่วน แต่ไม่มีสินค้า
  - id (product id): v5 = id ไม่มีอยู่ใน database

...
```

## Logic Overview

The generator uses a **Rotation Strategy**:
1. **Valid Test Cases**: It rotates through the valid partitions of each condition to create a set of "positive" test cases. It ensures every valid partition is covered at least once.
2. **Invalid Test Cases**: For every invalid partition found, it creates a new test case by taking a valid base case and injecting that single invalid value (to isolate the failure).

---
Panuwat Rujirawanich (Nes)
