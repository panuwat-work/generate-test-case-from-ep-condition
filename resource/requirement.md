# Condition-based Test Case → Executable Test Case (Requirement-driven, Sheet-safe)

## 0. Mandatory Requirement Reference (CRITICAL)

⚠️ **BEFORE generating any test case, AI MUST:**

1. Read and understand **`resource/requirement.md`**
2. Treat `requirement.md` as the **single source of truth** for:

   * System type (UI / API / Database)
   * Available endpoints
   * Business rules
   * Validation rules
3. Use `requirement.md` to:

   * Determine **test type**
   * Decide **Prepare Step**
   * Decide **Test Steps**
   * Decide **Expected Result**

❌ AI is NOT allowed to infer UI behavior
if `requirement.md` defines the feature as **API or Database only**

If `requirement.md` conflicts with assumptions →
**`requirement.md` ALWAYS wins**

---

## 1. Objective

This agenda defines **strict instructions for AI** to convert **condition-based test cases**
(v / x conditions) into **fully executable test cases** that are:

* Requirement-aligned
* Non-duplicated
* **Safe for Google Sheets / Excel**
* Ready for **QA execution, review, and reporting**

Supported test types:

* API
* Database
* Integration / End-to-End
* UI (ONLY if explicitly defined in requirement.md)

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
* If multiple `x*` appear → AI must **reject or split**
* Conditions describe **business rules**, not steps

---

## 3. Conversion Principles (Must Follow)

### 3.1 One-to-One Mapping

* Each condition-based TC → exactly **one executable test case**
* No merging
* No extra test cases

---

### 3.2 Requirement-first Test Type Resolution

AI MUST determine test type using this priority order:

1. **Explicit definition in `requirement.md`**

   * API endpoint → API test
   * Table / persistence rule → Database test
   * Both → Integration test
2. ONLY if requirement.md is silent → infer cautiously
3. UI test is allowed **ONLY** when UI behavior is explicitly stated

❌ If requirement defines API →
AI MUST NOT generate UI-style steps (no page, no form, no click)

---

### 3.3 Data Construction Rules

* Generate **explicit, realistic values**
* Must comply with validation rules in `requirement.md`
* Valid TC → all values valid
* Invalid TC → only the **main invalid condition** is invalid

---

### 3.4 Error Handling Rules (Invalid Case)

* Expected Result must describe:

  * Exact error defined in requirement.md
  * HTTP status / rejection behavior (for API)
  * Constraint failure (for DB)
* No cascading failures
* No UI error if requirement is API

---

## 4. Mandatory Output Format (Sheet-safe)

⚠️ **CRITICAL STRUCTURE RULE**

> **One test case = ONE physical row**
> **Newline is NOT allowed inside any cell**

### Column Order (DO NOT CHANGE)

```
TC ID	Test Case Name	Test Objective	Prepare Step	Test Data	Test Steps	Expected Result
```

Rules:

* Use **TAB** as column separator
* Use **newline** ONLY between test cases
* Use `|` to separate multiple items inside a cell
* No markdown tables
* No explanation text outside the table

---

## 5. Column Writing Rules

### 5.1 TC ID

* Use original TC ID with **3-digit numeric format**

  * TC1 → TC001
  * TC10 → TC010
* Do NOT create new IDs

---

### 5.2 Test Case Name

* Short
* Business-readable
* Reflect **business rule from requirement.md**

---

### 5.3 Test Objective

* One sentence
* Must start with **"To verify that..."**
* Reference system behavior defined in requirement.md

---

### 5.4 Prepare Step

Purpose:

* Ensure system state required by requirement.md

Rules:

* **Single-line only**
* Steps separated by `|`
* No UI action unless requirement defines UI
* If not required → `N/A`

Examples:

API:

```
Ensure authentication token is valid | Ensure target resource does not exist
```

Database:

```
Ensure no existing record matches the test data
```

Integration:

```
Ensure required master data exists | Ensure dependent services are running
```

---

### 5.5 Test Data

* **Single-line key-value format**
* Fields separated by `|`
* Values must comply with requirement.md

Example:

```
email: john.doe01@gmail.com | username: JohnDoe | password: Abc@12345
```

---

### 5.6 Test Steps

* **Single-line only**
* Steps separated by `|`
* MUST match test type resolved from requirement.md
* No UI wording for API tests

---

#### 5.6.1 API Test Steps (DEFAULT for API requirement)

```
1. Send POST request to create user using test data | 2. Receive API response
```

---

#### 5.6.2 Database Test Steps

```
1. Attempt to persist data using test data | 2. Verify database behavior
```

---

#### 5.6.3 Integration Test Steps

```
1. Call API using test data | 2. Verify data persistence in database
```

---

#### 5.6.4 UI Test Steps (ONLY if requirement defines UI)

```
1. Open specified screen | 2. Perform action using test data | 3. Submit request
```

---

### 5.7 Expected Result

* **Single-line**
* Must match outcome defined in requirement.md

API example:

```
API returns HTTP 201 and user is created successfully
```

Invalid API:

```
API returns HTTP 400 with validation error for email field
```

---

## 6. Valid Case Deduplication Rule

* Generate minimal valid test cases
* Do NOT create permutations not required by requirement.md

---

## 7. Output Quality Checklist (AI Self-Check)

* [ ] requirement.md was read first
* [ ] Test type matches requirement.md
* [ ] No UI step in API/DB test
* [ ] One test case = one row
* [ ] No newline inside any cell
* [ ] TC ID uses 3-digit format
* [ ] Output is Sheet-safe

---

## 8. Final Instruction to AI

1. Read `resource/requirement.md`
2. Resolve test type and behavior from requirements
3. Convert condition-based test cases strictly following this agenda
4. Output **ONLY** the tab-separated test case table
