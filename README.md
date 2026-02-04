# EP Test Case Generator with AI Conversion

This tool automates the generation of [Equivalence Partitioning (EP)](https://en.wikipedia.org/wiki/Equivalence_partitioning) test cases from a set of conditions defined in an Excel file. It produces condition-based test cases and uses AI to convert them into fully executable test cases ready for QA execution.

## Features

- **Automated EP Generation**: Generates test cases covering valid and invalid partitions using a rotation strategy to ensure coverage while minimizing duplicates.
- **Interactive HTML Matrix**: Produces `ep_matrix.html` with:
  - Color-coded cells (Green for Valid, Red for Invalid).
  - Interactive column highlighting (clicking a column header highlights the relevant cells and EP tags).
  - A dynamic side panel showing detailed conditions for the selected test case.
- **AI-Powered Test Case Conversion**: Uses ChatGPT (GPT-4o) to convert condition-based test cases into executable test cases with:
  - Test Case Name
  - Test Objective
  - Test Data (JSON format)
  - Test Steps
  - Expected Results
- **Requirement Integration**: Optionally include business requirements as context for AI conversion.

## Project Structure

```
├── resource/                    # Input resources
│   ├── EP_table.xlsx           # EP conditions definition
│   └── requirement.md          # Optional: Business requirements
├── results/                     # Generated outputs
│   ├── testcase.txt            # Condition-based test cases
│   ├── ep_matrix.html          # Interactive visualization
│   └── testcase.xlsx           # AI-converted executable test cases
├── EP_generate.py              # EP test case generator
├── convert_condition_to_testcase.py  # AI conversion script
├── agend.md                    # AI conversion instructions
├── template.xlsx               # Excel template for EP_table
└── .env                        # OpenAI API key configuration
```

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

   # Install required packages
   pip install openpyxl openai pandas python-dotenv
   ```

4. **Configure OpenAI API Key**:
   Create a `.env` file in the project root and add your API key:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
   Get your API key from: https://platform.openai.com/api-keys

## How to Use

### Step 1: Prepare Your Input File

1. Create an Excel file in the `resource/` directory (e.g., `EP_table.xlsx`).
2. The file must follow this column structure (starting from Row 2):
   - **Column A**: Condition Name
   - **Column B**: Valid Description
   - **Column C**: Valid Tag (e.g., `v1`, `v2`...)
   - **Column D**: Invalid Description
   - **Column E**: Invalid Tag (e.g., `x1`, `x2`...)

You can use `template.xlsx` as a reference.

### Step 2: (Optional) Add Requirements

Create or edit `resource/requirement.md` to include:
- Business rules
- Constraints
- Specific requirements for test case generation

To skip requirements, set `REQUIREMENT_FILE = ""` in `convert_condition_to_testcase.py`.

### Step 3: Generate EP Test Cases

Run the EP generator:
```bash
python3 EP_generate.py
```

This creates:
- `results/testcase.txt` - Condition-based test cases
- `results/ep_matrix.html` - Interactive visualization

### Step 4: Convert to Executable Test Cases

Run the AI conversion script:
```bash
python3 convert_condition_to_testcase.py
```

This creates:
- `results/testcase.xlsx` - Executable test cases in Excel format

## Output Files

### 1. `results/ep_matrix.html`
An interactive HTML file for visualizing the test cases.
- **Columns**: Represent generated Test Cases (TC1, TC2, ...)
- **Rows**: Represent EP Tags (v1, x1, etc.)
- **Click**: Click on any "TC" header to highlight its column and view details in the side panel

<img width="904" height="359" alt="image" src="https://github.com/user-attachments/assets/fefd211b-f07f-4338-b2f0-7273f9e8b8cf" />

### 2. `results/testcase.txt`
A plain text file containing the breakdown of each condition-based test case.

**Example:**
```text
TC1
  - Email uniqueness: v1 = Email doesn't exist in system
  - First character of username: v2 = Start with uppercase
  - Username allowed characters: v5 = Uppercase alphabet (A–Z)
  ...
```

### 3. `results/testcase.xlsx`
Excel file with executable test cases containing:
- **TC ID**: Test case identifier
- **Test Case Name**: Short, business-readable name
- **Test Objective**: What the test verifies
- **Test Data**: JSON format with concrete values
- **Test Steps**: Numbered, executable steps
- **Expected Result**: Clear, observable outcome

## Configuration

### EP_generate.py
```python
FILE_PATH = "resource/EP_table.xlsx"  # Input Excel file
OUTPUT_HTML = "results/ep_matrix.html"  # HTML output
```

### convert_condition_to_testcase.py
```python
INPUT_FILE = "results/testcase.txt"  # Condition-based test cases
AGENDA_FILE = "agend.md"  # AI conversion instructions
REQUIREMENT_FILE = "resource/requirement.md"  # Optional requirements
OUTPUT_FILE = "results/testcase.xlsx"  # Executable test cases
MODEL_NAME = "gpt-4o"  # OpenAI model
```

## Logic Overview

### EP Generation Strategy
The generator uses a **Rotation Strategy**:
1. **Valid Test Cases**: Rotates through valid partitions of each condition to create "positive" test cases, ensuring every valid partition is covered at least once.
2. **Invalid Test Cases**: For every invalid partition, creates a new test case by taking a valid base case and injecting that single invalid value (to isolate the failure).

### AI Conversion Process
1. Reads conversion instructions from `agend.md`
2. Optionally loads business requirements from `resource/requirement.md`
3. Sends condition-based test cases to ChatGPT with context
4. Parses AI response (tab-separated format)
5. Generates Excel file with executable test cases

## Notes

> **Important**: 
> - The AI conversion uses GPT-4o which incurs API costs
> - Keep your `.env` file secure and never commit it to version control
> - The `agend.md` file contains strict instructions for AI - modify carefully
> - Temperature is set to 0.2 for deterministic output

---
Panuwat Rujirawanich (Nes)
