from openpyxl import load_workbook
from collections import OrderedDict

FILE_PATH = "test2.xlsx"
OUTPUT_HTML = "ep_matrix.html"

# =========================================================
# STEP 1: Read conditions from Excel
# =========================================================
def read_conditions(path):
    wb = load_workbook(path, data_only=True, keep_vba=True)
    ws = wb.active

    conditions = OrderedDict()
    last_condition = None

    for row in ws.iter_rows(min_row=2):
        cond = row[0].value
        v_desc = row[1].value
        v_tag = row[2].value
        x_desc = row[3].value
        x_tag = row[4].value

        if cond:
            last_condition = str(cond).strip()

        if not last_condition:
            continue

        if last_condition not in conditions:
            conditions[last_condition] = {
                "valid": OrderedDict(),
                "invalid": OrderedDict()
            }

        if isinstance(v_tag, str):
            conditions[last_condition]["valid"][v_tag] = v_desc

        if isinstance(x_tag, str):
            conditions[last_condition]["invalid"][x_tag] = x_desc

    return conditions


# =========================================================
# STEP 2: Generate EP Testcases
# =========================================================
def generate_ep_testcases(conditions):
    conds = list(conditions.keys())

    valid_sets = [list(conditions[c]["valid"].keys()) for c in conds]
    invalid_sets = [list(conditions[c]["invalid"].keys()) for c in conds]

    tcs = []

    # --- all valid ---
    for i in range(max(len(v) for v in valid_sets)):
        tc = [v[i % len(v)] for v in valid_sets]
        tcs.append(tc)

    # --- single invalid ---
    base_idx = 0
    for ci, invs in enumerate(invalid_sets):
        for x in invs:
            base = tcs[base_idx % len(tcs)].copy()
            base[ci] = x
            tcs.append(base)
            base_idx += 1

    return tcs


# =========================================================
# STEP 3: Print Testcase Detail (KEEP THIS)
# =========================================================
def print_testcases(tcs, conditions):
    conds = list(conditions.keys())

    for i, tc in enumerate(tcs, start=1):
        print(f"\nTC{i}")
        for idx, tag in enumerate(tc):
            cond = conds[idx]
            desc = (
                conditions[cond]["valid"].get(tag)
                or conditions[cond]["invalid"].get(tag)
            )
            print(f"  - {cond}: {tag} = {desc}")


# =========================================================
# STEP 4: Build EP Matrix (NO PRINT)
# =========================================================
def build_matrix(conditions, tcs):
    tags = []
    tag_to_cond = {}

    for cond, data in conditions.items():
        for t in list(data["valid"].keys()) + list(data["invalid"].keys()):
            tags.append(t)
            tag_to_cond[t] = cond

    matrix = OrderedDict((t, [""] * len(tcs)) for t in tags)

    for i, tc in enumerate(tcs):
        for tag in tc:
            matrix[tag][i] = "X"

    return matrix, tag_to_cond


# =========================================================
# STEP 5: Generate HTML Matrix
# =========================================================
def generate_html(matrix, tag_to_cond, tc_count):
    html = []
    html.append("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>EP Matrix</title>
<style>
body { font-family: Arial; }

table {
  border-collapse: collapse;
  table-layout: auto;
  width: max-content;
}

th, td {
  border: 1px solid #999;
  padding: 6px 12px;
  white-space: nowrap;
  text-align: center;
  font-size: 13px;
}

th {
  background: #f3f3f3;
  cursor: pointer;
}

.tag {
  text-align: left;
  font-weight: bold;
  min-width: 140px;
  position: sticky;
  left: 0;
  background: white;
  z-index: 2;
}

.valid {
  background: #c3e6cb !important;
  color: #155724;
}
.invalid {
  background: #f5c6cb !important;
  color: #721c24;
}

.sep-top td { border-top: 3px solid black; }

.highlight-col { background: #fff3cd !important; }
.highlight-row { background: #d1ecf1 !important; }
.highlight-x {
  background: #f6c23e !important;
  font-weight: bold;
}
.highlight-green {
  background: #28a745 !important;
  color: white;
  font-weight: bold;
}
.highlight-red {
  background: #dc3545 !important;
  color: white;
  font-weight: bold;
}
</style>

<script>
let activeCol = null;

function toggleColumn(col) {
  const table = document.getElementById("ep");

  if (activeCol === col) {
    clearAll();
    activeCol = null;
    return;
  }

  clearAll();
  activeCol = col;

  for (let r = 1; r < table.rows.length; r++) {
    const c = table.rows[r].cells[col];
    c.classList.add("highlight-col");

    if (c.innerText === "X") {
      // Check the tag in the first cell (index 0)
      const tagCell = table.rows[r].cells[0];
      const tagText = tagCell.innerText.trim().toLowerCase();
      
      if (tagText.startsWith("v")) {
             c.classList.add("highlight-green");
             tagCell.classList.add("highlight-green");
      } else if (tagText.startsWith("x")) {
             c.classList.add("highlight-red");
             tagCell.classList.add("highlight-red");
      } else {
             c.classList.add("highlight-x"); // fallback
             tagCell.classList.add("highlight-row");
      }
    }
  }

  table.rows[0].cells[col].classList.add("highlight-col");
}

function clearAll() {
  document.querySelectorAll(".highlight-col,.highlight-row,.highlight-x,.highlight-green,.highlight-red")
    .forEach(e => e.classList.remove("highlight-col","highlight-row","highlight-x","highlight-green","highlight-red"));
}
</script>
</head>
<body>

<h2>Equivalence Partitioning Matrix</h2>

<table id="ep">
<tr>
<th>EP Tag</th>
""")

    for i in range(tc_count):
        html.append(f'<th onclick="toggleColumn({i+1})">TC{i+1}</th>')
    html.append("</tr>")

    prev_cond = None
    for tag, row in matrix.items():
        cond = tag_to_cond[tag]
        cls = "valid" if tag.startswith("v") else "invalid"
        sep = "sep-top" if prev_cond and cond != prev_cond else ""

        html.append(f'<tr class="{sep}">')
        html.append(f'<td class="tag {cls}">{tag}</td>')
        for c in row:
            html.append(f"<td>{c}</td>")
        html.append("</tr>")
        prev_cond = cond

    html.append("</table></body></html>")
    return "\n".join(html)


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    conditions = read_conditions(FILE_PATH)
    tcs = generate_ep_testcases(conditions)

    # ✅ testcase detail ยัง print
    print_testcases(tcs, conditions)

    # ❌ matrix ไม่ print
    matrix, tag_to_cond = build_matrix(conditions, tcs)

    html = generate_html(matrix, tag_to_cond, len(tcs))
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n[OK] EP Matrix generated → {OUTPUT_HTML}")
