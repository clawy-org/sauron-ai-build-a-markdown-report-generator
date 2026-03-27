#!/usr/bin/env python3
"""Tests for md_report.py — covers all element types, chaining, table alignment, and render output."""

import os
import tempfile
import unittest

from md_report import Report


class TestHeadings(unittest.TestCase):
    def test_h1(self):
        r = Report().h1("Title").render()
        self.assertIn("# Title", r)

    def test_h2(self):
        r = Report().h2("Section").render()
        self.assertIn("## Section", r)

    def test_h3(self):
        r = Report().h3("Subsection").render()
        self.assertIn("### Subsection", r)


class TestText(unittest.TestCase):
    def test_paragraph(self):
        r = Report().text("Hello world.").render()
        self.assertIn("Hello world.", r)

    def test_multiple_paragraphs(self):
        r = Report().text("First.").text("Second.").render()
        self.assertIn("First.", r)
        self.assertIn("Second.", r)
        # They should be separated by blank line
        self.assertIn("First.\n\nSecond.", r)


class TestBulletList(unittest.TestCase):
    def test_basic(self):
        r = Report().bullet(["a", "b", "c"]).render()
        self.assertIn("- a\n- b\n- c", r)

    def test_single_item(self):
        r = Report().bullet(["only"]).render()
        self.assertIn("- only", r)


class TestNumberedList(unittest.TestCase):
    def test_basic(self):
        r = Report().numbered(["x", "y", "z"]).render()
        self.assertIn("1. x\n2. y\n3. z", r)


class TestTable(unittest.TestCase):
    def test_basic_table(self):
        r = Report().table(["A", "B"], [["1", "2"], ["3", "4"]]).render()
        self.assertIn("| A", r)
        self.assertIn("| 1", r)
        self.assertIn("---", r)

    def test_left_alignment(self):
        r = Report().table(["H"], [["x"]], align=["left"]).render()
        # Left-aligned: no colons at start of separator (just dashes)
        lines = r.strip().split("\n")
        sep = lines[1]
        # Should contain only dashes (no leading colon)
        sep_content = sep.replace("|", "").strip()
        self.assertFalse(sep_content.startswith(":"))

    def test_center_alignment(self):
        r = Report().table(["H"], [["x"]], align=["center"]).render()
        lines = r.strip().split("\n")
        sep = lines[1]
        sep_content = sep.replace("|", "").strip()
        self.assertTrue(sep_content.startswith(":"))
        self.assertTrue(sep_content.endswith(":"))

    def test_right_alignment(self):
        r = Report().table(["H"], [["x"]], align=["right"]).render()
        lines = r.strip().split("\n")
        sep = lines[1]
        sep_content = sep.replace("|", "").strip()
        self.assertTrue(sep_content.endswith(":"))
        self.assertFalse(sep_content.startswith(":"))

    def test_empty_headers_no_crash(self):
        r = Report().table([], []).render()
        # Should produce empty report (no table)
        self.assertEqual(r.strip(), "")

    def test_missing_cells_padded(self):
        """Rows with fewer cells than headers should not crash."""
        r = Report().table(["A", "B", "C"], [["only_one"]]).render()
        self.assertIn("only_one", r)

    def test_mixed_alignment(self):
        r = Report().table(
            ["Left", "Center", "Right"],
            [["a", "b", "c"]],
            align=["left", "center", "right"],
        ).render()
        lines = r.strip().split("\n")
        sep = lines[1]
        parts = [p.strip() for p in sep.split("|") if p.strip()]
        # left: no colon prefix
        self.assertFalse(parts[0].startswith(":"))
        # center: colon on both sides
        self.assertTrue(parts[1].startswith(":") and parts[1].endswith(":"))
        # right: colon only on right
        self.assertTrue(parts[2].endswith(":"))
        self.assertFalse(parts[2].startswith(":"))


class TestCode(unittest.TestCase):
    def test_fenced_no_lang(self):
        r = Report().code("x = 1").render()
        self.assertIn("```\nx = 1\n```", r)

    def test_fenced_with_lang(self):
        r = Report().code("x = 1", lang="python").render()
        self.assertIn("```python\nx = 1\n```", r)


class TestQuote(unittest.TestCase):
    def test_single_line(self):
        r = Report().quote("Hello").render()
        self.assertIn("> Hello", r)

    def test_multi_line(self):
        r = Report().quote("Line1\nLine2").render()
        self.assertIn("> Line1\n> Line2", r)


class TestHorizontalRule(unittest.TestCase):
    def test_hr(self):
        r = Report().hr().render()
        self.assertIn("---", r)


class TestCollapsible(unittest.TestCase):
    def test_details_block(self):
        r = Report().collapsible("Click me", "Hidden content").render()
        self.assertIn("<details>", r)
        self.assertIn("<summary>Click me</summary>", r)
        self.assertIn("Hidden content", r)
        self.assertIn("</details>", r)


class TestChaining(unittest.TestCase):
    def test_full_chain(self):
        """All methods should be chainable and produce combined output."""
        r = (
            Report()
            .h1("T")
            .text("P")
            .bullet(["a"])
            .numbered(["b"])
            .table(["X"], [["1"]])
            .code("c")
            .quote("q")
            .hr()
            .collapsible("s", "d")
            .h2("S")
            .h3("SS")
        )
        rendered = r.render()
        self.assertIn("# T", rendered)
        self.assertIn("P", rendered)
        self.assertIn("- a", rendered)
        self.assertIn("1. b", rendered)
        self.assertIn("| X", rendered)
        self.assertIn("```\nc\n```", rendered)
        self.assertIn("> q", rendered)
        self.assertIn("---", rendered)
        self.assertIn("<details>", rendered)
        self.assertIn("## S", rendered)
        self.assertIn("### SS", rendered)


class TestRenderOutput(unittest.TestCase):
    def test_blocks_separated_by_blank_lines(self):
        r = Report().h1("A").h2("B").render()
        self.assertIn("# A\n\n## B", r)

    def test_ends_with_newline(self):
        r = Report().text("End").render()
        self.assertTrue(r.endswith("\n"))


class TestSave(unittest.TestCase):
    def test_save_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.md")
            Report().h1("Saved").save(path)
            self.assertTrue(os.path.exists(path))
            with open(path) as f:
                content = f.read()
            self.assertIn("# Saved", content)

    def test_save_creates_subdirectories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "sub", "dir", "report.md")
            Report().text("Deep").save(path)
            self.assertTrue(os.path.exists(path))

    def test_save_returns_self(self):
        """save() should be chainable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.md")
            r = Report().h1("X").save(path)
            self.assertIsInstance(r, Report)


class TestDemo(unittest.TestCase):
    def test_demo_runs(self):
        """The demo script should run without errors."""
        from md_report import _demo
        # Just ensure no exception
        _demo()


if __name__ == "__main__":
    unittest.main()
