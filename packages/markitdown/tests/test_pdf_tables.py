#!/usr/bin/env python3 -m pytest
"""Tests for PDF table extraction functionality."""
import os
import re
import pytest

from markitdown import MarkItDown

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


# --- Helper Functions ---
def validate_strings(result, expected_strings, exclude_strings=None):
    """Validate presence or absence of specific strings."""
    text_content = result.text_content.replace("\\", "")
    for string in expected_strings:
        assert string in text_content, f"Expected string not found: {string}"
    if exclude_strings:
        for string in exclude_strings:
            assert string not in text_content, f"Excluded string found: {string}"


def validate_markdown_table(result, expected_headers, expected_data_samples):
    """Validate that a markdown table exists with expected headers and data."""
    text_content = result.text_content

    # Check for markdown table structure (| header | header |)
    assert "|" in text_content, "No markdown table markers found"

    # Check headers are present
    for header in expected_headers:
        assert header in text_content, f"Expected table header not found: {header}"

    # Check some data values are present
    for data in expected_data_samples:
        assert data in text_content, f"Expected table data not found: {data}"


def extract_markdown_tables(text_content):
    """
    Extract all markdown tables from text content.
    Returns a list of tables, where each table is a list of rows,
    and each row is a list of cell values.
    """
    tables = []
    lines = text_content.split("\n")
    current_table = []
    in_table = False

    for line in lines:
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            # Skip separator rows (contain only dashes and pipes)
            if re.match(r"^\|[\s\-|]+\|$", line):
                continue
            # Parse cells from the row
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            current_table.append(cells)
            in_table = True
        else:
            if in_table and current_table:
                tables.append(current_table)
                current_table = []
            in_table = False

    # Don't forget the last table
    if current_table:
        tables.append(current_table)

    return tables


def validate_table_structure(table):
    """
    Validate that a table has consistent structure:
    - All rows have the same number of columns
    - Has at least a header row and one data row
    """
    if not table:
        return False, "Table is empty"

    if len(table) < 2:
        return False, "Table should have at least header and one data row"

    num_cols = len(table[0])
    if num_cols < 2:
        return False, f"Table should have at least 2 columns, found {num_cols}"

    for i, row in enumerate(table):
        if len(row) != num_cols:
            return False, f"Row {i} has {len(row)} columns, expected {num_cols}"

    return True, "Table structure is valid"


class TestPdfTableExtraction:
    """Test PDF table extraction with various PDF types."""

    @pytest.fixture
    def markitdown(self):
        """Create MarkItDown instance."""
        return MarkItDown()

    def test_borderless_table_extraction(self, markitdown):
        """Test extraction of borderless tables from SPARSE inventory PDF.

        Expected output structure:
        - Header: INVENTORY RECONCILIATION REPORT with Report ID, Warehouse, Date, Prepared By
        - Pipe-separated rows with inventory data
        - Text section: Variance Analysis with Summary Statistics
        - More pipe-separated rows with extended inventory review
        - Footer: Recommendations section
        """
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Validate document header content
        expected_strings = [
            "INVENTORY RECONCILIATION REPORT",
            "Report ID: SPARSE-2024-INV-1234",
            "Warehouse: Distribution Center East",
            "Report Date: 2024-11-15",
            "Prepared By: Sarah Martinez",
        ]
        validate_strings(result, expected_strings)

        # Validate pipe-separated format is used
        assert "|" in text_content, "Should have pipe separators for form-style data"

        # --- Validate First Table Data (Inventory Variance) ---
        # Validate table headers are present
        first_table_headers = [
            "Product Code",
            "Location",
            "Expected",
            "Actual",
            "Variance",
            "Status",
        ]
        for header in first_table_headers:
            assert header in text_content, f"Should contain header '{header}'"

        # Validate first table has all expected SKUs
        first_table_skus = ["SKU-8847", "SKU-9201", "SKU-4563", "SKU-7728"]
        for sku in first_table_skus:
            assert sku in text_content, f"Should contain {sku}"

        # Validate first table has correct status values
        expected_statuses = ["OK", "CRITICAL"]
        for status in expected_statuses:
            assert status in text_content, f"Should contain status '{status}'"

        # Validate first table has location codes
        expected_locations = ["A-12", "B-07", "C-15", "D-22", "A-08"]
        for loc in expected_locations:
            assert loc in text_content, f"Should contain location '{loc}'"

        # --- Validate Second Table Data (Extended Inventory Review) ---
        # Validate second table headers
        second_table_headers = [
            "Category",
            "Unit Cost",
            "Total Value",
            "Last Audit",
            "Notes",
        ]
        for header in second_table_headers:
            assert header in text_content, f"Should contain header '{header}'"

        # Validate second table has all expected SKUs (10 products)
        second_table_skus = [
            "SKU-8847",
            "SKU-9201",
            "SKU-4563",
            "SKU-7728",
            "SKU-3345",
            "SKU-5512",
            "SKU-6678",
            "SKU-7789",
            "SKU-2234",
            "SKU-1123",
        ]
        for sku in second_table_skus:
            assert sku in text_content, f"Should contain {sku}"

        # Validate second table has categories
        expected_categories = ["Electronics", "Hardware", "Software", "Accessories"]
        for category in expected_categories:
            assert category in text_content, f"Should contain category '{category}'"

        # Validate second table has cost values (spot check)
        expected_costs = ["$45.00", "$32.50", "$120.00", "$15.75"]
        for cost in expected_costs:
            assert cost in text_content, f"Should contain cost '{cost}'"

        # Validate second table has note values
        expected_notes = ["Verified", "Critical", "Pending"]
        for note in expected_notes:
            assert note in text_content, f"Should contain note '{note}'"

        # --- Validate Analysis Text Section ---
        analysis_strings = [
            "Variance Analysis:",
            "Summary Statistics:",
            "Total Variance Cost: $4,287.50",
            "Critical Items: 1",
            "Overall Accuracy: 97.2%",
            "Recommendations:",
        ]
        validate_strings(result, analysis_strings)

        # --- Validate Document Structure Order ---
        # Verify sections appear in correct order
        # Note: Using flexible patterns since column merging may occur based on gap detection
        import re

        header_pos = text_content.find("INVENTORY RECONCILIATION REPORT")
        # Look for Product Code header - may be in same column as Location or separate
        first_table_match = re.search(r"\|\s*Product Code", text_content)
        variance_pos = text_content.find("Variance Analysis:")
        extended_review_pos = text_content.find("Extended Inventory Review:")
        # Second table - look for SKU entries after extended review section
        # The table may not have pipes on every row due to paragraph detection
        second_table_pos = -1
        if extended_review_pos != -1:
            # Look for either "| Product Code" or "Product Code" as table header
            second_table_match = re.search(
                r"Product Code.*Category", text_content[extended_review_pos:]
            )
            if second_table_match:
                # Adjust position to be relative to full text
                second_table_pos = extended_review_pos + second_table_match.start()
        recommendations_pos = text_content.find("Recommendations:")

        positions = {
            "header": header_pos,
            "first_table": first_table_match.start() if first_table_match else -1,
            "variance_analysis": variance_pos,
            "extended_review": extended_review_pos,
            "second_table": second_table_pos,
            "recommendations": recommendations_pos,
        }

        # All sections should be found
        for name, pos in positions.items():
            assert pos != -1, f"Section '{name}' not found in output"

        # Verify correct order
        assert (
            positions["header"] < positions["first_table"]
        ), "Header should come before first table"
        assert (
            positions["first_table"] < positions["variance_analysis"]
        ), "First table should come before Variance Analysis"
        assert (
            positions["variance_analysis"] < positions["extended_review"]
        ), "Variance Analysis should come before Extended Review"
        assert (
            positions["extended_review"] < positions["second_table"]
        ), "Extended Review should come before second table"
        assert (
            positions["second_table"] < positions["recommendations"]
        ), "Second table should come before Recommendations"

    def test_borderless_table_no_duplication(self, markitdown):
        """Test that borderless table content is not duplicated excessively."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Count occurrences of unique table data - should not be excessively duplicated
        # SKU-8847 appears in both tables, plus possibly once in summary text
        sku_count = text_content.count("SKU-8847")
        # Should appear at most 4 times (2 tables + minor text references), not more
        assert (
            sku_count <= 4
        ), f"SKU-8847 appears too many times ({sku_count}), suggests duplication issue"

    def test_borderless_table_correct_position(self, markitdown):
        """Test that tables appear in correct positions relative to text."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Verify content order - header should come before table content, which should come before analysis
        header_pos = text_content.find("Prepared By: Sarah Martinez")
        # Look for Product Code in any pipe-separated format
        product_code_pos = text_content.find("Product Code")
        variance_pos = text_content.find("Variance Analysis:")

        assert header_pos != -1, "Header should be found"
        assert product_code_pos != -1, "Product Code should be found"
        assert variance_pos != -1, "Variance Analysis should be found"

        assert (
            header_pos < product_code_pos < variance_pos
        ), "Product data should appear between header and Variance Analysis"

        # Second table content should appear after "Extended Inventory Review"
        extended_review_pos = text_content.find("Extended Inventory Review:")
        # Look for Category header which is in second table
        category_pos = text_content.find("Category")
        recommendations_pos = text_content.find("Recommendations:")

        if (
            extended_review_pos != -1
            and category_pos != -1
            and recommendations_pos != -1
        ):
            # Find Category position after Extended Inventory Review
            category_after_review = text_content.find("Category", extended_review_pos)
            if category_after_review != -1:
                assert (
                    extended_review_pos < category_after_review < recommendations_pos
                ), "Extended review table should appear between Extended Inventory Review and Recommendations"

    def test_receipt_pdf_extraction(self, markitdown):
        """Test extraction of receipt PDF (no tables, formatted text).

        Expected output structure:
        - Store header: TECHMART ELECTRONICS with address
        - Transaction info: Store #, date, TXN, Cashier, Register
        - Line items: 6 products with prices and member discounts
        - Totals: Subtotal, Member Discount, Sales Tax, Rewards, TOTAL
        - Payment info: Visa Card, Auth, Ref
        - Rewards member info: Name, ID, Points
        - Return policy and footer
        """
        pdf_path = os.path.join(
            TEST_FILES_DIR, "RECEIPT-2024-TXN-98765_retail_purchase.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # --- Validate Store Header ---
        store_header = [
            "TECHMART ELECTRONICS",
            "4567 Innovation Blvd",
            "San Francisco, CA 94103",
            "(415) 555-0199",
        ]
        validate_strings(result, store_header)

        # --- Validate Transaction Info ---
        transaction_info = [
            "Store #0342 - Downtown SF",
            "11/23/2024",
            "TXN: TXN-98765-2024",
            "Cashier: Emily Rodriguez",
            "Register: POS-07",
        ]
        validate_strings(result, transaction_info)

        # --- Validate Line Items (6 products) ---
        line_items = [
            # Product 1: Headphones
            "Wireless Noise-Cancelling",
            "Headphones - Premium Black",
            "AUDIO-5521",
            "$349.99",
            "$299.99",
            # Product 2: USB-C Hub
            "USB-C Hub 7-in-1 Adapter",
            "ACC-8834",
            "$79.99",
            "$159.98",
            # Product 3: Portable SSD
            "Portable SSD 2TB",
            "STOR-2241",
            "$289.00",
            "$260.00",
            # Product 4: Wireless Mouse
            "Ergonomic Wireless Mouse",
            "ACC-9012",
            "$59.99",
            # Product 5: Screen Cleaning Kit
            "Screen Cleaning Kit",
            "CARE-1156",
            "$12.99",
            "$38.97",
            # Product 6: HDMI Cable
            "HDMI 2.1 Cable 6ft",
            "CABLE-7789",
            "$24.99",
            "$44.98",
        ]
        validate_strings(result, line_items)

        # --- Validate Totals ---
        totals = [
            "SUBTOTAL",
            "$863.91",
            "Member Discount",
            "Sales Tax (8.5%)",
            "$66.23",
            "Rewards Applied",
            "-$25.00",
            "TOTAL",
            "$821.14",
        ]
        validate_strings(result, totals)

        # --- Validate Payment Info ---
        payment_info = [
            "PAYMENT METHOD",
            "Visa Card ending in 4782",
            "Auth: 847392",
            "REF-20241123-98765",
        ]
        validate_strings(result, payment_info)

        # --- Validate Rewards Member Info ---
        rewards_info = [
            "REWARDS MEMBER",
            "Sarah Mitchell",
            "ID: TM-447821",
            "Points Earned: 821",
            "Total Points: 3,247",
        ]
        validate_strings(result, rewards_info)

        # --- Validate Return Policy & Footer ---
        footer_info = [
            "RETURN POLICY",
            "Returns within 30 days",
            "Receipt required",
            "Thank you for shopping!",
            "www.techmart.example.com",
        ]
        validate_strings(result, footer_info)

        # --- Validate Document Structure Order ---
        positions = {
            "store_header": text_content.find("TECHMART ELECTRONICS"),
            "transaction": text_content.find("TXN: TXN-98765-2024"),
            "first_item": text_content.find("Wireless Noise-Cancelling"),
            "subtotal": text_content.find("SUBTOTAL"),
            "total": text_content.find("TOTAL"),
            "payment": text_content.find("PAYMENT METHOD"),
            "rewards": text_content.find("REWARDS MEMBER"),
            "return_policy": text_content.find("RETURN POLICY"),
        }

        # All sections should be found
        for name, pos in positions.items():
            assert pos != -1, f"Section '{name}' not found in output"

        # Verify correct order
        assert (
            positions["store_header"] < positions["transaction"]
        ), "Store header should come before transaction"
        assert (
            positions["transaction"] < positions["first_item"]
        ), "Transaction should come before items"
        assert (
            positions["first_item"] < positions["subtotal"]
        ), "Items should come before subtotal"
        assert (
            positions["subtotal"] < positions["total"]
        ), "Subtotal should come before total"
        assert (
            positions["total"] < positions["payment"]
        ), "Total should come before payment"
        assert (
            positions["payment"] < positions["rewards"]
        ), "Payment should come before rewards"
        assert (
            positions["rewards"] < positions["return_policy"]
        ), "Rewards should come before return policy"

    def test_multipage_invoice_extraction(self, markitdown):
        """Test extraction of multipage invoice PDF with form-style layout.

        Expected output: Pipe-separated format with clear cell boundaries.
        Form data should be extracted with pipes indicating column separations.
        """
        pdf_path = os.path.join(TEST_FILES_DIR, "REPAIR-2022-INV-001_multipage.pdf")

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Validate basic content is extracted
        expected_strings = [
            "ZAVA AUTO REPAIR",
            "Collision Repair",
            "Redmond, WA",
            "Gabriel Diaz",
            "Jeep",
            "Grand Cherokee",
            "Parts",
            "Body Labor",
            "Paint Labor",
            "GRAND TOTAL",
            # Second page content
            "Bruce Wayne",
            "Batmobile",
        ]
        validate_strings(result, expected_strings)

        # Validate pipe-separated table format
        # Form-style documents should use pipes to separate cells
        assert "|" in text_content, "Form-style PDF should contain pipe separators"

        # Validate key form fields are properly separated
        # These patterns check that label and value are in separate cells
        # Note: cells may have padding spaces for column alignment
        import re

        assert re.search(
            r"\| Insured name\s*\|", text_content
        ), "Insured name should be in its own cell"
        assert re.search(
            r"\| Gabriel Diaz\s*\|", text_content
        ), "Gabriel Diaz should be in its own cell"
        assert re.search(
            r"\| Year\s*\|", text_content
        ), "Year label should be in its own cell"
        assert re.search(
            r"\| 2022\s*\|", text_content
        ), "Year value should be in its own cell"

        # Validate table structure for estimate totals
        assert (
            re.search(r"\| Hours\s*\|", text_content) or "Hours |" in text_content
        ), "Hours column header should be present"
        assert (
            re.search(r"\| Rate\s*\|", text_content) or "Rate |" in text_content
        ), "Rate column header should be present"
        assert (
            re.search(r"\| Cost\s*\|", text_content) or "Cost |" in text_content
        ), "Cost column header should be present"

        # Validate numeric values are extracted
        assert "2,100" in text_content, "Parts cost should be extracted"
        assert "300" in text_content, "Body labor cost should be extracted"
        assert "225" in text_content, "Paint labor cost should be extracted"
        assert "5,738" in text_content, "Grand total should be extracted"

        # Validate second page content (Bruce Wayne invoice)
        assert "Bruce Wayne" in text_content, "Second page customer name"
        assert "Batmobile" in text_content, "Second page vehicle model"
        assert "211,522" in text_content, "Second page grand total"

        # Validate disclaimer text is NOT in table format (long paragraph)
        # The disclaimer should be extracted as plain text, not pipe-separated
        assert (
            "preliminary estimate" in text_content.lower()
        ), "Disclaimer text should be present"

    def test_academic_pdf_extraction(self, markitdown):
        """Test extraction of academic paper PDF (scientific document).

        Expected output: Plain text without tables or pipe characters.
        Scientific documents should be extracted as flowing text with proper spacing,
        not misinterpreted as tables.
        """
        pdf_path = os.path.join(TEST_FILES_DIR, "test.pdf")

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Validate academic paper content with proper spacing
        expected_strings = [
            "Introduction",
            "Large language models",  # Should have proper spacing, not "Largelanguagemodels"
            "agents",
            "multi-agent",  # Should be properly hyphenated
        ]
        validate_strings(result, expected_strings)

        # Validate proper text formatting (words separated by spaces)
        assert "LLMs" in text_content, "Should contain 'LLMs' acronym"
        assert "reasoning" in text_content, "Should contain 'reasoning'"
        assert "observations" in text_content, "Should contain 'observations'"

        # Ensure content is not empty and has proper length
        assert len(text_content) > 1000, "Academic PDF should have substantial content"

        # Scientific documents should NOT have tables or pipe characters
        assert (
            "|" not in text_content
        ), "Scientific document should not contain pipe characters (no tables)"

        # Verify no markdown tables were extracted
        tables = extract_markdown_tables(text_content)
        assert (
            len(tables) == 0
        ), f"Scientific document should have no tables, found {len(tables)}"

        # Verify text is properly formatted with spaces between words
        # Check that common phrases are NOT joined together (which would indicate bad extraction)
        assert (
            "Largelanguagemodels" not in text_content
        ), "Text should have proper spacing, not joined words"
        assert (
            "multiagentconversations" not in text_content.lower()
        ), "Text should have proper spacing between words"

    def test_scanned_pdf_handling(self, markitdown):
        """Test handling of scanned/image-based PDF (no text layer).

        Expected output: Empty - scanned PDFs without OCR have no text layer.
        """
        pdf_path = os.path.join(
            TEST_FILES_DIR, "MEDRPT-2024-PAT-3847_medical_report_scan.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)

        # Scanned PDFs without OCR have no text layer, so extraction should be empty
        assert (
            result is not None
        ), "Converter should return a result even for scanned PDFs"
        assert result.text_content is not None, "text_content should not be None"

        # Verify extraction is empty (no text layer in scanned PDF)
        assert (
            result.text_content.strip() == ""
        ), f"Scanned PDF should have empty extraction, got: '{result.text_content[:100]}...'"


class TestPdfTableMarkdownFormat:
    """Test that extracted tables have proper markdown formatting."""

    @pytest.fixture
    def markitdown(self):
        """Create MarkItDown instance."""
        return MarkItDown()

    def test_markdown_table_has_pipe_format(self, markitdown):
        """Test that form-style PDFs have pipe-separated format."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Find rows with pipes
        lines = text_content.split("\n")
        pipe_rows = [
            line for line in lines if line.startswith("|") and line.endswith("|")
        ]

        assert len(pipe_rows) > 0, "Should have pipe-separated rows"

        # Check that Product Code appears in a pipe-separated row
        product_code_found = any("Product Code" in row for row in pipe_rows)
        assert product_code_found, "Product Code should be in pipe-separated format"

    def test_markdown_table_columns_have_pipes(self, markitdown):
        """Test that form-style PDF columns are separated with pipes."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Find table rows and verify column structure
        lines = text_content.split("\n")
        table_rows = [
            line for line in lines if line.startswith("|") and line.endswith("|")
        ]

        assert len(table_rows) > 0, "Should have markdown table rows"

        # Check that at least some rows have multiple columns (pipes)
        multi_col_rows = [row for row in table_rows if row.count("|") >= 3]
        assert (
            len(multi_col_rows) > 5
        ), f"Should have rows with multiple columns, found {len(multi_col_rows)}"


class TestPdfTableStructureConsistency:
    """Test that extracted tables have consistent structure across all PDF types."""

    @pytest.fixture
    def markitdown(self):
        """Create MarkItDown instance."""
        return MarkItDown()

    def test_borderless_table_structure(self, markitdown):
        """Test that borderless table PDF has pipe-separated structure."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Should have pipe-separated content
        assert "|" in text_content, "Borderless table PDF should have pipe separators"

        # Check that key content is present
        assert "Product Code" in text_content, "Should contain Product Code"
        assert "SKU-8847" in text_content, "Should contain first SKU"
        assert "SKU-9201" in text_content, "Should contain second SKU"

    def test_multipage_invoice_table_structure(self, markitdown):
        """Test that multipage invoice PDF has pipe-separated format."""
        pdf_path = os.path.join(TEST_FILES_DIR, "REPAIR-2022-INV-001_multipage.pdf")

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Should have pipe-separated content
        assert "|" in text_content, "Invoice PDF should have pipe separators"

        # Find rows with pipes
        lines = text_content.split("\n")
        pipe_rows = [
            line for line in lines if line.startswith("|") and line.endswith("|")
        ]

        assert (
            len(pipe_rows) > 10
        ), f"Should have multiple pipe-separated rows, found {len(pipe_rows)}"

        # Check that some rows have multiple columns
        multi_col_rows = [row for row in pipe_rows if row.count("|") >= 4]
        assert len(multi_col_rows) > 5, "Should have rows with 3+ columns"

    def test_receipt_has_no_tables(self, markitdown):
        """Test that receipt PDF doesn't incorrectly extract tables from formatted text."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "RECEIPT-2024-TXN-98765_retail_purchase.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        tables = extract_markdown_tables(result.text_content)

        # Receipt should not have markdown tables extracted
        # (it's formatted text, not tabular data)
        # If tables are extracted, they should be minimal/empty
        total_table_rows = sum(len(t) for t in tables)
        assert (
            total_table_rows < 5
        ), f"Receipt should not have significant tables, found {total_table_rows} rows"

    def test_scanned_pdf_no_tables(self, markitdown):
        """Test that scanned PDF has empty extraction and no tables."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "MEDRPT-2024-PAT-3847_medical_report_scan.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)

        # Scanned PDF with no text layer should have empty extraction
        assert (
            result.text_content.strip() == ""
        ), "Scanned PDF should have empty extraction"

        tables = extract_markdown_tables(result.text_content)

        # Scanned PDF with no text layer should have no tables
        assert len(tables) == 0, "Scanned PDF should have no extracted tables"

    def test_all_pdfs_table_rows_consistent(self, markitdown):
        """Test that all PDF tables have rows with pipe-separated content.

        Note: With gap-based column detection, rows may have different column counts
        depending on how content is spaced in the PDF. What's important is that each
        row has pipe separators and the content is readable.
        """
        pdf_files = [
            "SPARSE-2024-INV-1234_borderless_table.pdf",
            "REPAIR-2022-INV-001_multipage.pdf",
            "RECEIPT-2024-TXN-98765_retail_purchase.pdf",
            "test.pdf",
        ]

        for pdf_file in pdf_files:
            pdf_path = os.path.join(TEST_FILES_DIR, pdf_file)
            if not os.path.exists(pdf_path):
                continue

            result = markitdown.convert(pdf_path)
            tables = extract_markdown_tables(result.text_content)

            for table_idx, table in enumerate(tables):
                if not table:
                    continue

                # Verify each row has at least one column (pipe-separated content)
                for row_idx, row in enumerate(table):
                    assert (
                        len(row) >= 1
                    ), f"{pdf_file}: Table {table_idx}, row {row_idx} has no columns"

                    # Verify the row has non-empty content
                    row_content = " ".join(cell.strip() for cell in row)
                    assert (
                        len(row_content.strip()) > 0
                    ), f"{pdf_file}: Table {table_idx}, row {row_idx} is empty"

    def test_borderless_table_data_integrity(self, markitdown):
        """Test that borderless table extraction preserves data integrity."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        tables = extract_markdown_tables(result.text_content)

        assert len(tables) >= 2, "Should have at least 2 tables"

        # Check first table has expected SKU data
        first_table = tables[0]
        table_text = str(first_table)
        assert "SKU-8847" in table_text, "First table should contain SKU-8847"
        assert "SKU-9201" in table_text, "First table should contain SKU-9201"

        # Check second table has expected category data
        second_table = tables[1]
        table_text = str(second_table)
        assert "Electronics" in table_text, "Second table should contain Electronics"
        assert "Hardware" in table_text, "Second table should contain Hardware"
