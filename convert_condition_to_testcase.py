import os
import sys
import pandas as pd
import io
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
INPUT_FILE = "results/testcase.txt"
AGENDA_FILE = "agend.md"
REQUIREMENT_FILE = "resource/requirement.md"
OUTPUT_FILE = "results/testcase.xlsx"
MODEL_NAME = "gpt-4o"

def clean_ai_output(text):
    """
    Removes markdown code blocks (```) if present in the AI response.
    """
    lines = text.strip().split('\n')
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()

def main():
    # 1. Check for API Key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please export it: export OPENAI_API_KEY='sk-...'")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # 2. Read Input Files
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        sys.exit(1)
    
    if not os.path.exists(AGENDA_FILE):
        print(f"Error: Agenda file '{AGENDA_FILE}' not found.")
        sys.exit(1)

    print(f"Reading {INPUT_FILE}, {AGENDA_FILE}, and {REQUIREMENT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        testcase_content = f.read()

    with open(AGENDA_FILE, "r", encoding="utf-8") as f:
        agenda_content = f.read()
    
    # Read requirement file (optional - skip if REQUIREMENT_FILE is empty or file doesn't exist)
    requirement_content = ""
    if REQUIREMENT_FILE and os.path.exists(REQUIREMENT_FILE):
        with open(REQUIREMENT_FILE, "r", encoding="utf-8") as f:
            requirement_content = f.read()
            if requirement_content.strip():
                print(f"  ✓ Loaded requirements from {REQUIREMENT_FILE}")
    
    # Build system prompt with agenda and requirements
    system_content = agenda_content
    if requirement_content.strip():
        system_content += "\n\n---\n\n# Additional Context: Requirements\n\n" + requirement_content
    
    # User content is the test cases to convert
    user_content = testcase_content

    # 3. Call OpenAI API
    print(f"Sending request to OpenAI ({MODEL_NAME})...")
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2  # Low temperature for deterministic output
        )
        ai_output = response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

    # 4. Process Output
    print("Processing AI response...")
    cleaned_output = clean_ai_output(ai_output)
    
    # 5. Save to Excel
    try:
        # Expecting tab-separated values as per agend.md instructions
        df = pd.read_csv(io.StringIO(cleaned_output), sep="\t")
        
        # Verify columns if needed, but we trust the AI correctly followed the strict agenda for now
        # Writing to Excel
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"Success! Converted test cases saved to '{OUTPUT_FILE}'.")
        
    except Exception as e:
        print("Error parsing AI output or saving to Excel:")
        print(e)
        print("--- Raw AI Output ---")
        print(cleaned_output)
        sys.exit(1)

if __name__ == "__main__":
    main()
