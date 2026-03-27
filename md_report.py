#!/usr/bin/env python3
"""
md_report.py — A programmatic markdown report builder.

Provides a fluent/chainable API for generating well-formatted Markdown reports.
Stdlib only. No external dependencies.
"""

from __future__ import annotations

import os
from typing import List, Optional, Sequence


class Report:
    """Fluent markdown report builder.

    Usage:
        report = (
            Report()
            .h1("My Report")
            .text("An introduction paragraph.")
            .h2("Data")
            .table(["Name", "Score"], [["Alice", "95"], ["Bob", "87"]])
            .render()
        )
    """

    def __init__(self) -> None:
        self._blocks: List[str] = []

    # ── Headings ──────────────────────────────────────────────

    def h1(self, text: str) -> Report:
        """Add a level-1 heading."""
        self._blocks.append(f"# {text}")
        return self

    def h2(self, text: str) -> Report:
        """Add a level-2 heading."""
        self._blocks.append(f"## {text}")
        return self

    def h3(self, text: str) -> Report:
        """Add a level-3 heading."""
        self._blocks.append(f"### {text}")
        return self

    # ── Body ──────────────────────────────────────────────────

    def text(self, paragraph: str) -> Report:
        """Add a body paragraph."""
        self._blocks.append(paragraph)
        return self

    # ── Lists ─────────────────────────────────────────────────

    def bullet(self, items: Sequence[str]) -> Report:
        """Add an unordered (bullet) list."""
        lines = [f"- {item}" for item in items]
        self._blocks.append("\n".join(lines))
        return self

    def numbered(self, items: Sequence[str]) -> Report:
        """Add an ordered (numbered) list."""
        lines = [f"{i}. {item}" for i, item in enumerate(items, 1)]
        self._blocks.append("\n".join(lines))
        return self

    # ── Table ─────────────────────────────────────────────────

    def table(
        self,
        headers: Sequence[str],
        rows: Sequence[Sequence[str]],
        align: Optional[Sequence[str]] = None,
    ) -> Report:
        """Add a markdown table.

        Args:
            headers: Column header strings.
            rows: List of rows, each a list of cell strings.
            align: Optional per-column alignment: 'left', 'center', or 'right'.
                   Defaults to left-aligned for all columns.
        """
        if not headers:
            return self

        ncols = len(headers)

        # Compute column widths (minimum 3 for separator dashes)
        widths = [max(3, len(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row[:ncols]):
                widths[i] = max(widths[i], len(str(cell)))

        def _pad(val: str, width: int) -> str:
            return val.ljust(width)

        # Header row
        header_line = "| " + " | ".join(_pad(h, widths[i]) for i, h in enumerate(headers)) + " |"

        # Separator row with alignment
        separators = []
        for i in range(ncols):
            a = (align[i] if align and i < len(align) else "left").lower()
            w = widths[i]
            if a == "center":
                separators.append(":" + "-" * (w - 2) + ":" if w >= 3 else ":-:")
            elif a == "right":
                separators.append("-" * (w - 1) + ":")
            else:  # left (default)
                separators.append("-" * w)
        sep_line = "| " + " | ".join(separators) + " |"

        # Data rows
        data_lines = []
        for row in rows:
            cells = []
            for i in range(ncols):
                val = str(row[i]) if i < len(row) else ""
                cells.append(_pad(val, widths[i]))
            data_lines.append("| " + " | ".join(cells) + " |")

        self._blocks.append("\n".join([header_line, sep_line] + data_lines))
        return self

    # ── Code ──────────────────────────────────────────────────

    def code(self, content: str, lang: str = "") -> Report:
        """Add a fenced code block."""
        self._blocks.append(f"```{lang}\n{content}\n```")
        return self

    # ── Blockquote ────────────────────────────────────────────

    def quote(self, text: str) -> Report:
        """Add a blockquote."""
        lines = text.split("\n")
        quoted = "\n".join(f"> {line}" for line in lines)
        self._blocks.append(quoted)
        return self

    # ── Horizontal Rule ───────────────────────────────────────

    def hr(self) -> Report:
        """Add a horizontal rule."""
        self._blocks.append("---")
        return self

    # ── Collapsible ───────────────────────────────────────────

    def collapsible(self, summary: str, content: str) -> Report:
        """Add a collapsible details/summary HTML block."""
        block = f"<details>\n<summary>{summary}</summary>\n\n{content}\n\n</details>"
        self._blocks.append(block)
        return self

    # ── Output ────────────────────────────────────────────────

    def render(self) -> str:
        """Render the full markdown string."""
        return "\n\n".join(self._blocks) + "\n"

    def save(self, path: str) -> Report:
        """Write the rendered markdown to a file."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render())
        return self


# ── Demo ──────────────────────────────────────────────────────

def _demo() -> None:
    """Run a demo that produces valid markdown output."""
    report = (
        Report()
        .h1("Monthly Performance Report")
        .text("This report summarises key metrics for **March 2026**.")
        .hr()
        .h2("Highlights")
        .bullet([
            "Revenue up 12% month-over-month",
            "3 new enterprise clients onboarded",
            "System uptime: 99.97%",
        ])
        .h2("Team Scores")
        .table(
            ["Team", "Score", "Delta"],
            [
                ["Engineering", "94", "+3"],
                ["Design", "91", "+1"],
                ["Sales", "88", "-2"],
            ],
            align=["left", "center", "right"],
        )
        .h2("Deployment Stats")
        .code(
            "deployments: 47\nrollbacks:    2\nhotfixes:     5",
            lang="yaml",
        )
        .h3("Notes")
        .quote("Ship fast, but never ship broken.\n— The Team")
        .collapsible(
            "Raw data (click to expand)",
            "```json\n{\"deploys\": 47, \"rollbacks\": 2}\n```",
        )
        .h2("Next Steps")
        .numbered([
            "Finalise Q2 roadmap",
            "Hire two senior engineers",
            "Launch v2.1 beta",
        ])
    )

    print(report.render())


if __name__ == "__main__":
    _demo()
