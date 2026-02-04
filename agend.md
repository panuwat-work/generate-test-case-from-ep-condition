# Test Case Generation Agenda

This document defines the rules and structure for generating API test cases in a consistent, automation-friendly format.

---

## 1. Scope

* This agenda applies to **API test cases only**
* UI, Mobile, and E2E flows are **out of scope**
* Output format is Markdown (`.md`)
* Test cases are designed to be convertible to Excel / automation artifacts

---

## 2. Test Case Structure

Each test case MUST contain the following columns:

| Column Name     | Required | Description                                   |
| --------------- | -------- | --------------------------------------------- |
| TC ID           | ✅        | Unique test case identifier                   |
| Test Case Name  | ✅        | Clear, behavior-based name                    |
| Test Objective  | ✅        | Purpose of the test                           |
| Prepare Step    | ⭕        | Only when necessary (e.g. prerequisite setup) |
| Test Data       | ✅        | Explicit request data                         |
| Test Steps      | ✅        | API execution steps                           |
| Expected Result | ✅        | API response expectation                      |

---

## 3. TC ID Rules

* Format: `TC-XXX`
* Sequential numbering
* No reuse of IDs

Example:

* TC-001
* TC-002

---

## 4. Test Case Name Rules

Test Case Name MUST:

* Describe **what is being tested**
* Reflect valid or invalid behavior
* Be understandable without reading Test Steps

Good examples:

* Register user with valid email and password
* Login fails when password is incorrect

Bad examples:

* Test register
* API case 1

---

## 5. Test Objective Rules

Test Objective MUST:

* Explain **why** this test exists
* Focus on one behavior only
* Be concise and clear

Example:

* To verify that the system allows user registration with valid credentials
* To ensure login fails when an incorrect password is provided

---

## 6. Prepare Step Rules

* This column is **optional**
* Leave **blank** if no prerequisite is required
* Use ONLY when setup is mandatory

Examples of valid usage:

* Existing user must already be registered
* User account is locked after 5 failed attempts

Examples of invalid usage:

* Open browser
* Call API (belongs to Test Steps)

---

## 7. Test Data Rules

Test Data represents **request payload or parameters**.

### Format Rules

* Use key-value pairs
* Lowercase keys
* One space after colon
* Explicit values only (no placeholders)

Example:
email: [alice@test.com](mailto:alice@test.com) | password: Test1234

### Notes

* `|` is allowed as a field separator in AI output
* Multi-line or readable formatting MAY be handled by post-processing scripts
* Test Data must be deterministic and automation-ready

Rules:

* **Valid TC** → all fields valid
* **Invalid TC** → only the main field under test is invalid
* Other fields MUST remain valid

---

## 8. Test Steps Rules

Test Steps MUST:

* Be **API-based only**
* Be written as **numbered steps**
* Reference **actual values from Test Data**
* Include HTTP method and endpoint

### Format

1. Send `<METHOD>` request to `<endpoint>` with specified test data
2. Receive API response

Example:

1. Send POST request to /api/register with email=[alice@test.com](mailto:alice@test.com) and password=Test1234
2. Receive API response

### Notes

* Inline values or `|`-separated values are acceptable in AI output
* Final readability formatting MAY be applied by post-processing tools
* Do NOT use phrases like “with test data”

---

## 9. Expected Result Rules

Expected Result MUST:

* Describe API response behavior
* Include HTTP status code
* Include response message or error when applicable

Examples:

* API returns 201 Created and user is registered successfully
* API returns 400 Bad Request with validation error message

Avoid:

* Test passed
* System works correctly

---

## 10. Valid / Invalid Test Case Rules

### Valid Test Case

* All input fields are valid
* Expected Result indicates successful behavior

### Invalid Test Case

* Only ONE field is invalid per test case
* Invalid field MUST be clear from:

  * Test Case Name
  * Test Data
  * Expected Result

---

## 11. General Rules

* Do NOT repeat the same test data across multiple test cases unless required
* Avoid redundant test cases
* Keep language clear and unambiguous
* Output MUST be consistent and automation-friendly

---

## 12. Formatting Responsibility

* AI is responsible for **semantic correctness**
* Formatting normalization (e.g. multi-line conversion) MAY be handled by scripts
* Agenda prioritizes **stability and consistency over visual formatting**
