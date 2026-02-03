from openpyxl import load_workbook
from collections import OrderedDict
import json

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
# STEP 2: Generate EP Testcases (DO NOT TOUCH)
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
# STEP 5: Generate HTML Matrix + TC Detail Panel (JS expects JSON)
# =========================================================
def generate_html(matrix, tag_to_cond, tc_count, tcs, conditions):
    conds = list(conditions.keys())

    # ---- prepare TC detail for JS as JSON ----
    tc_detail = OrderedDict()
    for i, tc in enumerate(tcs, start=1):
        rows = []
        for idx, tag in enumerate(tc):
            cond = conds[idx]
            desc = (
                conditions[cond]["valid"].get(tag)
                or conditions[cond]["invalid"].get(tag)
            )
            # ensure strings (avoid None)
            desc_text = "" if desc is None else str(desc)
            rows.append({
                "condition": cond,
                "tag": tag,
                "desc": desc_text
            })
        tc_detail[f"TC{i}"] = rows

    tc_detail_json = json.dumps(tc_detail, ensure_ascii=False)

    html_parts = []

    html_parts.append(f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>EP Matrix</title>

<style>
body {{
  font-family: Arial;
  display: flex;
  gap: 24px;
  padding: 16px;
}}

table {{
  border-collapse: collapse;
  table-layout: auto;
  width: max-content;
  max-width: 80vw;
}}

th, td {{
  border: 1px solid #999;
  padding: 6px 12px;
  white-space: nowrap;
  text-align: center;
  font-size: 13px;
}}

th {{
  background: #f3f3f3;
  cursor: pointer;
}}

.tag {{
  text-align: left;
  font-weight: bold;
  min-width: 160px;
  position: sticky;
  left: 0;
  background: white;
  z-index: 2;
}}

.valid {{ background: #c3e6cb; color: #155724; }}
.invalid {{ background: #f5c6cb; color: #721c24; }}

.sep-top td {{ border-top: 3px solid black; }}

.highlight-col {{ background: #fff3cd !important; }}
.highlight-green {{ background: #28a745 !important; color: white; font-weight: bold; }}
.highlight-red {{ background: #dc3545 !important; color: white; font-weight: bold; }}

#tc-detail {{
  min-width: 460px;
  border: 1px solid #ccc;
  padding: 16px;
  background: #fafafa;
  max-height: 80vh;
  overflow: auto;
}}

#tc-detail h3 {{
  margin-top: 0;
  margin-bottom: 8px;
}}
</style>

<script>
const TC_DETAIL = {tc_detail_json};

let activeCol = null;

function toggleColumn(col) {{
  const table = document.getElementById("ep");

  // column index in table rows: 0 = EP Tag, 1 = TC1, 2 = TC2, ...
  const colIndex = col; // we pass col as 1..N, which matches table cell index

  if (activeCol === colIndex) {{
    clearAll();
    document.getElementById("tc-detail").innerHTML = "";
    activeCol = null;
    return;
  }}

  clearAll();
  activeCol = colIndex;

  // loop rows starting from 1 (skip header)
  for (let r = 1; r < table.rows.length; r++) {{
    const cell = table.rows[r].cells[colIndex];
    if (!cell) continue;
    cell.classList.add("highlight-col");

    if (cell.innerText.trim() === "X") {{
      const tagCell = table.rows[r].cells[0];
      const tag = tagCell.innerText.trim().toLowerCase();

      if (tag.startsWith("v")) {{
        cell.classList.add("highlight-green");
        tagCell.classList.add("highlight-green");
      }} else {{
        cell.classList.add("highlight-red");
        tagCell.classList.add("highlight-red");
      }}
    }}
  }}

  // highlight header cell
  if (table.rows[0] && table.rows[0].cells[colIndex]) {{
    table.rows[0].cells[colIndex].classList.add("highlight-col");
  }}

  renderTC(colIndex);
}}

function renderTC(colIndex) {{
  const key = "TC" + colIndex;
  const data = TC_DETAIL[key];
  if (!data) return;

  let html = `<h3>${{key}}</h3>`;
  data.forEach(i => {{
    // escape html for safety
    const cond = escapeHtml(i.condition);
    const tag = escapeHtml(i.tag);
    const desc = escapeHtml(i.desc);

    html += `
      <div style="margin-bottom:8px;">
        - <b>${{cond}}</b>: <b>${{tag}}</b> = ${{desc}}
      </div>
    `;
  }});
  document.getElementById("tc-detail").innerHTML = html;
}}

/* clear highlights */
function clearAll() {{
  document.querySelectorAll(
    ".highlight-col,.highlight-green,.highlight-red"
  ).forEach(e => e.classList.remove("highlight-col","highlight-green","highlight-red"));
}}

/* simple HTML escape */
function escapeHtml(text) {{
  if (!text && text !== 0) return "";
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}}
</script>
</head>

<body>
<div>
<h2>Equivalence Partitioning Matrix</h2>
<table id="ep">
<tr>
<th>EP Tag</th>
""")

    # header: TC1..TCn (note: header cell indices match JS colIndex)
    for i in range(tc_count):
        # we pass i+1 because table cell index 0=EP Tag, 1=TC1...
        html_parts.append(f'<th onclick="toggleColumn({i+1})">TC{i+1}</th>')
    html_parts.append("</tr>")

    prev_cond = None
    for tag, row in matrix.items():
        cond = tag_to_cond[tag]
        cls = "valid" if tag.startswith("v") else "invalid"
        sep = "sep-top" if prev_cond and cond != prev_cond else ""

        html_parts.append(f'<tr class="{sep}">')
        html_parts.append(f'<td class="tag {cls}">{tag}</td>')
        for c in row:
            html_parts.append(f"<td>{c}</td>")
        html_parts.append("</tr>")
        prev_cond = cond

    html_parts.append("""
</table>
</div>

<div id="tc-detail"></div>

</body>
</html>
""")

    return "\n".join(html_parts)


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    conditions = read_conditions(FILE_PATH)
    tcs = generate_ep_testcases(conditions)

    # terminal output stays as before
    print_testcases(tcs, conditions)

    # build matrix and write HTML
    matrix, tag_to_cond = build_matrix(conditions, tcs)
    html = generate_html(matrix, tag_to_cond, len(tcs), tcs, conditions)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n[OK] EP Matrix generated → {OUTPUT_HTML}")
