import os
import sys
import io
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

# ---------------------------
# Configuration
# ---------------------------
INPUT_FILE = "results/testcase.txt"
AGENDA_FILE = "agend.md"
REQUIREMENT_FILE = "resource/requirement.md"
OUTPUT_FILE = "results/testcase.xlsx"
MODEL_NAME = "gpt-4.1"

EXPECTED_COLUMNS = [
    "TC ID",
    "Test Case Name",
    "Test Objective",
    "Prepare Step",
    "Test Data",
    "Test Steps",
    "Expected Result"
]

# ---------------------------
# Utility Functions
# ---------------------------

def clean_ai_output(text: str) -> str:
    """Remove markdown code fences from AI output."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    return text.strip()


def normalize_multiline_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize Test Data & Test Steps:
    - ONLY split on ' | ' (pipe with spaces)
    - Preserve '|' inside real data
    - Remove leading spaces per line
    """
    target_columns = ["Test Data", "Test Steps"]

    for col in target_columns:
        if col not in df.columns:
            continue

        def normalize_cell(value: str) -> str:
            if not isinstance(value, str):
                return value

            # Split ONLY on ' | '
            parts = value.split(" | ")
            if len(parts) == 1:
                return value.strip()

            # Join as multiline and trim each line
            return "\n".join(p.strip() for p in parts)

        df[col] = df[col].apply(normalize_cell)

    return df


def validate_output(df: pd.DataFrame):
    """Validate AI output to ensure it is Sheet-safe and requirement-aligned."""
    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            f"Column mismatch.\nExpected: {EXPECTED_COLUMNS}\nActual: {list(df.columns)}"
        )

    ui_keywords = ["page", "screen", "click", "form", "button", "navigate"]
    for idx, row in df.iterrows():
        steps = str(row["Test Steps"]).lower()
        if any(word in steps for word in ui_keywords):
            raise ValueError(
                f"UI wording detected in Test Steps at row {idx + 1}: {row['Test Steps']}"
            )


def post_process_excel(file_path: str):
    """Enable wrap text so multiline cells render immediately."""
    wb = load_workbook(file_path)
    ws = wb.active

    wrap_alignment = Alignment(wrap_text=True, vertical="top")

    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and "\n" in cell.value:
                cell.alignment = wrap_alignment

    for row in ws.iter_rows():
        ws.row_dimensions[row[0].row].height = None

    wb.save(file_path)

# ---------------------------
# Main Process
# ---------------------------

def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    for file_path in [INPUT_FILE, AGENDA_FILE]:
        if not os.path.exists(file_path):
            print(f"❌ Required file not found: {file_path}")
            sys.exit(1)

    print("📖 Reading input files...")

    testcase_content = open(INPUT_FILE, encoding="utf-8").read()
    agenda_content = open(AGENDA_FILE, encoding="utf-8").read()

    requirement_content = ""
    if REQUIREMENT_FILE and os.path.exists(REQUIREMENT_FILE):
        requirement_content = open(REQUIREMENT_FILE, encoding="utf-8").read().strip()
        if requirement_content:
            print(f"  ✓ Loaded requirements from {REQUIREMENT_FILE}")

    system_content = f"""
CRITICAL RULES (NON-NEGOTIABLE):

1. You MUST read and follow resource/requirement.md first.
2. requirement.md is the single source of truth.
3. API / DB tests MUST NOT contain UI wording.
4. Column order MUST match agenda exactly.
"""

    system_content += "\n\n---\n\n# AGENDA\n\n" + agenda_content

    if requirement_content:
        system_content += "\n\n---\n\n# REQUIREMENTS\n\n" + requirement_content

    print(f"🤖 Sending request to OpenAI ({MODEL_NAME})...")
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": testcase_content}
        ],
        temperature=0.1
    )

    cleaned_output = clean_ai_output(response.choices[0].message.content)

    try:
        lines = cleaned_output.splitlines()
        first_row = lines[0].split("\t")

        if first_row == EXPECTED_COLUMNS:
            df = pd.read_csv(io.StringIO(cleaned_output), sep="\t")
        else:
            df = pd.read_csv(
                io.StringIO(cleaned_output),
                sep="\t",
                header=None,
                names=EXPECTED_COLUMNS
            )

        df = normalize_multiline_columns(df)
        validate_output(df)

    except Exception as e:
        print("❌ Validation failed:")
        print(e)
        print("\n--- RAW AI OUTPUT ---\n")
        print(cleaned_output)
        sys.exit(1)

    df.to_excel(OUTPUT_FILE, index=False)
    post_process_excel(OUTPUT_FILE)

    print(f"✅ Success! Test cases saved to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
