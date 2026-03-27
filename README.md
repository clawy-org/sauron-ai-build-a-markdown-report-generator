# Markdown Report Generator

A single-file, stdlib-only Python library for programmatically building well-formatted Markdown reports.

## Installation

No installation needed — just copy `md_report.py` into your project. Requires Python 3.7+.

## Quick Start

```python
from md_report import Report

report = (
    Report()
    .h1("Sales Report")
    .text("Quarterly summary for Q1 2026.")
    .h2("Results")
    .table(
        ["Region", "Revenue", "Growth"],
        [
            ["North", "$1.2M", "+8%"],
            ["South", "$900K", "+3%"],
            ["West", "$1.5M", "+15%"],
        ],
        align=["left", "right", "center"],
    )
    .h2("Key Takeaways")
    .bullet([
        "West region leading growth",
        "Overall revenue up 9%",
        "New markets underperforming",
    ])
    .save("report.md")
)
```

## API Reference

All methods return `self` for chaining.

### Headings

| Method | Description |
|--------|-------------|
| `.h1(text)` | Level 1 heading (`# ...`) |
| `.h2(text)` | Level 2 heading (`## ...`) |
| `.h3(text)` | Level 3 heading (`### ...`) |

### Content

| Method | Description |
|--------|-------------|
| `.text(paragraph)` | Body paragraph |
| `.bullet(items)` | Unordered list from a list of strings |
| `.numbered(items)` | Ordered list from a list of strings |
| `.code(content, lang="")` | Fenced code block with optional language |
| `.quote(text)` | Blockquote (supports multi-line) |

### Structure

| Method | Description |
|--------|-------------|
| `.hr()` | Horizontal rule (`---`) |
| `.table(headers, rows, align=None)` | Markdown table with optional alignment (`"left"`, `"center"`, `"right"` per column) |
| `.collapsible(summary, content)` | HTML `<details>/<summary>` block |

### Output

| Method | Description |
|--------|-------------|
| `.render()` | Returns the full markdown string |
| `.save(path)` | Writes to file (creates directories if needed), returns `self` |

## Examples

### Code Block

```python
Report().h2("Config").code('server:\n  port: 8080', lang="yaml").render()
```

Output:
```
## Config

```yaml
server:
  port: 8080
```​
```

### Collapsible Section

```python
Report().collapsible("Details", "Some hidden content here.").render()
```

Output:
```html
<details>
<summary>Details</summary>

Some hidden content here.

</details>
```

### Blockquote

```python
Report().quote("To be or not to be.\n— Shakespeare").render()
```

Output:
```
> To be or not to be.
> — Shakespeare
```

## Running the Demo

```bash
python md_report.py
```

This prints a sample monthly performance report to stdout.

## Running Tests

```bash
python -m pytest test_md_report.py -v
# or
python test_md_report.py
```

## License

Public domain. Do whatever you want with it.
