# agenda.md

# Condition-based Test Case → Executable Test Case (Sheet-ready)

## 1. Objective

This agenda defines **strict instructions for AI** to convert **condition-based test cases**
(v / x conditions) into **fully executable test cases** that are:

* Requirement-aligned
* Non-duplicated
* Ready to **copy & paste into Google Sheets**
* Suitable for **QA execution, review, and reporting**

This agenda is **generic** and can be reused across features, modules, and projects.

---

## 2. Input Format (Condition-based Test Case)

AI will receive test cases in the following format:

```
TC1
- Field A: v1 = valid condition description
- Field B: v2 = valid condition description
- Field C: x3 = invalid condition description
```

### Rules

* `v*` = valid condition
* `x*` = invalid condition
* **Valid TC** → contains only `v*`
* **Invalid TC** → contains exactly **one main `x*`**
* If multiple `x*` appear → AI must **reject or split** the test case
* Conditions are **logical definitions**, not test steps

---

## 3. Conversion Principles (Must Follow)

### 3.1 One-to-One Mapping

* Each TC condition → exactly **one executable test case**
* No merging of different TCs
* No creation of extra test cases

---

### 3.2 Data Construction Rules

When converting conditions → test data:

* Generate **explicit, realistic values**
* Data must:

  * Match condition intent
  * Be consistent across fields
  * Avoid placeholders like `test@test.com` unless specified
* Valid TC → all data must be valid
* Invalid TC → only the **main invalid condition** is invalid
  All other fields must be valid

---

### 3.3 Error Handling Rules (Invalid Case)

For invalid TCs:

* Expected Result must include:

  * Exact validation behavior (error message / UI state)
  * Field-level impact only
* Do NOT introduce cascading failures
* Do NOT validate unrelated fields

---

## 4. Mandatory Output Format (Google Sheet Ready)

⚠️ **AI MUST output in plain text, tab-separated format**

### Column Order (DO NOT CHANGE)

```
TC ID	Test Case Name	Test Objective	Test Data	Test Steps	Expected Result
```

* Use **TAB** as column separator
* Use **newline** as row separator
* No markdown tables
* No bullet points
* No explanations outside the table

---

## 5. Column Writing Rules

### 5.1 TC ID

* Use original TC ID (e.g. TC1, TC2)
* Do not rename or reorder

---

### 5.2 Test Case Name

* Short
* Business-readable
* Reflect **main condition**
* Example:

  * `Create account with valid email and username`
  * `Reject registration when email already exists`

---

### 5.3 Test Objective

* One sentence
* Start with **"To verify that..."**
* Focus on system behavior, not steps

---

### 5.4 Test Data

* Use **JSON format**
* Include only relevant fields
* Values must be concrete and realistic

Example:

```
{"email":"john.doe01@gmail.com","username":"JohnDoe","password":"Abc@12345"}
```

---

### 5.5 Test Steps

* Numbered steps in a single cell
* High-level but executable
* No UI locator details
* Example:

```
1. Open registration page
2. Enter valid registration data
3. Submit the form
```

---

### 5.6 Expected Result

* Clear, observable outcome
* Valid TC:

  * Success message
  * Navigation
  * Data persistence
* Invalid TC:

  * Exact validation message
  * Field highlight / blocking behavior

---

## 6. Valid Case Deduplication Rule

For **valid cases**:

* AI must generate **ONLY the minimal set of TCs**
* Each TC must cover **unique valid condition combinations**
* Do NOT generate permutations that do not add coverage
* If input already defines selected valid coverage → **do not expand**

---

## 7. Output Quality Checklist (AI Self-Check)

Before responding, AI must ensure:

* [ ] No duplicate valid coverage
* [ ] Only one invalid condition per invalid TC
* [ ] All columns filled
* [ ] Google Sheets paste works without reformatting
* [ ] No markdown / explanation text in output

---

## 8. Final Instruction to AI

> Convert the given condition-based test cases strictly following this agenda.
> Output **ONLY** the Google Sheet–ready test case table.
