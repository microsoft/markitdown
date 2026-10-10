"""PDF conversion, table extraction, numbering, and page cleanup."""

import os
import re
from unittest.mock import patch

import pytest

from markitdown import MarkItDown
from markitdown.converters._pdf_converter import (
    PARTIAL_NUMBERING_PATTERN,
    _merge_partial_numbering_lines,
)


# Table extraction

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
            # A separator needs dashes in every cell; retain blank data rows.
            if re.match(r"^\|(?:\s*-+\s*\|)+$", line):
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
        """Each SKU reference appears once, without missing or duplicated content."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # SKU-8847 appears once in each of two tables and once in the analysis.
        sku_count = text_content.count("SKU-8847")
        assert sku_count == 3, f"Expected 3 SKU-8847 references, found {sku_count}"

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

    def test_movie_theater_booking_pdf_extraction(self, markitdown):
        """Test extraction of movie theater booking PDF with complex tables.

        Expected output: Pipe-separated format with booking details, agency info,
        customer details, and show schedules in structured tables.
        """
        pdf_path = os.path.join(TEST_FILES_DIR, "movie-theater-booking-2024.pdf")

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Validate pipe-separated table format
        assert "|" in text_content, "Booking order should contain pipe separators"

        # Validate key booking information
        expected_strings = [
            "BOOKING ORDER",
            "2024-12-5678",  # Order number
            "Holiday Movie Marathon Package",  # Product description
            "12/20/2024 - 12/31/2024",  # Booking dates
            "SC-WINTER-2024",  # Alt order number
            "STARLIGHT CINEMAS",  # Cinema brand
        ]
        validate_strings(result, expected_strings)

        # Validate agency information
        agency_strings = [
            "Premier Entertainment Group",  # Agency name
            "Michael Chen",  # Contact
            "Sarah Johnson",  # Primary contact
            "Downtown Multiplex",  # Cinema name
        ]
        validate_strings(result, agency_strings)

        # Validate customer information
        customer_strings = [
            "Universal Studios Distribution",  # Customer name
            "Film Distributor",  # Category
            "CUST-98765",  # Customer ID
        ]
        validate_strings(result, customer_strings)

        # Validate booking summary totals
        booking_strings = [
            "$12,500.00",  # Gross amount
            "$11,250.00",  # Net amount
            "December 2024",  # Month
            "48",  # Number of shows
        ]
        validate_strings(result, booking_strings)

        # Validate show schedule details
        show_strings = [
            "Holiday Spectacular",  # Movie title
            "Winter Wonderland",  # Movie title
            "New Year Mystery",  # Movie title
            "IMAX 3D",  # Format
            "$250",  # Rate
            "$300",  # Rate
            "$3,000",  # Revenue
            "$3,600",  # Revenue
        ]
        validate_strings(result, show_strings)


class TestPdfFullOutputComparison:
    """Test that PDF extraction produces expected complete outputs."""

    @pytest.fixture
    def markitdown(self):
        """Create MarkItDown instance."""
        return MarkItDown()

    def test_movie_theater_full_output(self, markitdown):
        """Test complete output for movie theater booking PDF."""
        pdf_path = os.path.join(TEST_FILES_DIR, "movie-theater-booking-2024.pdf")
        expected_path = os.path.join(
            TEST_FILES_DIR, "expected_outputs", "movie-theater-booking-2024.md"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        if not os.path.exists(expected_path):
            pytest.skip(f"Expected output not found: {expected_path}")

        result = markitdown.convert(pdf_path)
        actual_output = result.text_content

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_output = f.read()

        assert actual_output == expected_output

    def test_sparse_borderless_table_full_output(self, markitdown):
        """Test complete output for SPARSE borderless table PDF."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf"
        )
        expected_path = os.path.join(
            TEST_FILES_DIR,
            "expected_outputs",
            "SPARSE-2024-INV-1234_borderless_table.md",
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        if not os.path.exists(expected_path):
            pytest.skip(f"Expected output not found: {expected_path}")

        result = markitdown.convert(pdf_path)
        actual_output = result.text_content

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_output = f.read()

        assert actual_output == expected_output

    def test_repair_multipage_full_output(self, markitdown):
        """Test complete output for REPAIR multipage invoice PDF."""
        pdf_path = os.path.join(TEST_FILES_DIR, "REPAIR-2022-INV-001_multipage.pdf")
        expected_path = os.path.join(
            TEST_FILES_DIR, "expected_outputs", "REPAIR-2022-INV-001_multipage.md"
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        if not os.path.exists(expected_path):
            pytest.skip(f"Expected output not found: {expected_path}")

        result = markitdown.convert(pdf_path)
        actual_output = result.text_content

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_output = f.read()

        assert actual_output == expected_output

    def test_receipt_full_output(self, markitdown):
        """Test complete output for RECEIPT retail purchase PDF."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "RECEIPT-2024-TXN-98765_retail_purchase.pdf"
        )
        expected_path = os.path.join(
            TEST_FILES_DIR,
            "expected_outputs",
            "RECEIPT-2024-TXN-98765_retail_purchase.md",
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        if not os.path.exists(expected_path):
            pytest.skip(f"Expected output not found: {expected_path}")

        result = markitdown.convert(pdf_path)
        actual_output = result.text_content

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_output = f.read()

        assert actual_output == expected_output

    def test_academic_paper_full_output(self, markitdown):
        """Test complete output for academic paper PDF."""
        pdf_path = os.path.join(TEST_FILES_DIR, "test.pdf")
        expected_path = os.path.join(TEST_FILES_DIR, "expected_outputs", "test.md")

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        if not os.path.exists(expected_path):
            pytest.skip(f"Expected output not found: {expected_path}")

        result = markitdown.convert(pdf_path)
        actual_output = result.text_content

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_output = f.read()

        assert actual_output == expected_output

    def test_medical_scan_full_output(self, markitdown):
        """A scanned PDF without OCR produces empty output and no Markdown tables."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "MEDRPT-2024-PAT-3847_medical_report_scan.pdf"
        )
        expected_path = os.path.join(
            TEST_FILES_DIR,
            "expected_outputs",
            "MEDRPT-2024-PAT-3847_medical_report_scan.md",
        )

        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        if not os.path.exists(expected_path):
            pytest.skip(f"Expected output not found: {expected_path}")

        result = markitdown.convert(pdf_path)
        actual_output = result.text_content

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_output = f.read()

        # Both should be empty (scanned PDF with no text layer)
        assert actual_output.strip() == "", "Scanned PDF should produce empty output"
        assert (
            expected_output.strip() == ""
        ), "Expected output should be empty for scanned PDF"
        assert (
            extract_markdown_tables(actual_output) == []
        ), "Scanned PDF should have no extracted tables"


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

    @pytest.mark.parametrize(
        "pdf_file, expected_table_count",
        [
            ("SPARSE-2024-INV-1234_borderless_table.pdf", 2),
            ("REPAIR-2022-INV-001_multipage.pdf", 6),
            ("RECEIPT-2024-TXN-98765_retail_purchase.pdf", 0),
            ("test.pdf", 0),
        ],
    )
    def test_all_pdfs_table_rows_consistent(
        self, markitdown, pdf_file, expected_table_count
    ):
        """Test that all PDF tables have rows with pipe-separated content.

        Note: With gap-based column detection, rows may have different column counts
        depending on how content is spaced in the PDF. What's important is that each
        row has pipe separators and the content is readable.
        """
        pdf_path = os.path.join(TEST_FILES_DIR, pdf_file)
        result = markitdown.convert(pdf_path)
        assert result.text_content.strip(), f"{pdf_file}: No text extracted"

        tables = extract_markdown_tables(result.text_content)
        assert (
            len(tables) == expected_table_count
        ), f"{pdf_file}: Expected {expected_table_count} tables, found {len(tables)}"

        for table_idx, table in enumerate(tables):
            for row_idx, row in enumerate(table):
                assert any(
                    cell.strip() for cell in row
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


# MasterFormat numbering


class TestMasterFormatPartialNumbering:
    """Test handling of MasterFormat-style partial numbering (.1, .2, etc.)."""

    def test_partial_numbering_pattern_regex(self):
        """Test that the partial numbering regex pattern correctly matches."""

        # Should match partial numbering patterns
        assert PARTIAL_NUMBERING_PATTERN.match(".1") is not None
        assert PARTIAL_NUMBERING_PATTERN.match(".2") is not None
        assert PARTIAL_NUMBERING_PATTERN.match(".10") is not None
        assert PARTIAL_NUMBERING_PATTERN.match(".99") is not None

        # Should NOT match other patterns
        assert PARTIAL_NUMBERING_PATTERN.match("1.") is None
        assert PARTIAL_NUMBERING_PATTERN.match("1.2") is None
        assert PARTIAL_NUMBERING_PATTERN.match(".1.2") is None
        assert PARTIAL_NUMBERING_PATTERN.match("text") is None
        assert PARTIAL_NUMBERING_PATTERN.match(".a") is None
        assert PARTIAL_NUMBERING_PATTERN.match("") is None

    def test_masterformat_partial_numbering_not_split(self):
        """Test that MasterFormat partial numbering stays with associated text.

        MasterFormat documents use partial numbering like:
            .1  The intent of this Request for Proposal...
            .2  Available information relative to...

        These should NOT be split into separate table columns, but kept
        as coherent text lines with the number followed by its description.
        """
        pdf_path = os.path.join(TEST_FILES_DIR, "masterformat_partial_numbering.pdf")

        markitdown = MarkItDown()
        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Partial numberings should NOT appear isolated on their own lines
        # If they're isolated, it means the parser incorrectly split them from their text
        lines = text_content.split("\n")
        isolated_numberings = []
        for line in lines:
            stripped = line.strip()
            # Check if line contains ONLY a partial numbering (with possible whitespace/pipes)
            cleaned = stripped.replace("|", "").strip()
            if cleaned in [".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", ".10"]:
                isolated_numberings.append(stripped)

        assert len(isolated_numberings) == 0, (
            f"Partial numberings should not be isolated from their text. "
            f"Found isolated: {isolated_numberings}"
        )

        # Verify that partial numberings appear WITH following text on the same line
        # Look for patterns like ".1 The intent" or ".1  Some text"
        partial_with_text = re.findall(r"\.\d+\s+\w+", text_content)
        assert (
            len(partial_with_text) > 0
        ), "Expected to find partial numberings followed by text on the same line"

    def test_masterformat_content_preserved(self):
        """Test that MasterFormat document content is fully preserved."""
        pdf_path = os.path.join(TEST_FILES_DIR, "masterformat_partial_numbering.pdf")

        markitdown = MarkItDown()
        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Verify key content from the MasterFormat document is preserved
        expected_content = [
            "RFP for Construction Management Services",
            "Section 00 00 43",
            "Instructions to Respondents",
            "Ken Sargent House",
            "INTENT",
            "Request for Proposal",
            "KEN SARGENT HOUSE",
            "GRANDE PRAIRIE, ALBERTA",
            "Section 00 00 45",
        ]

        for content in expected_content:
            assert (
                content in text_content
            ), f"Expected content '{content}' not found in extracted text"

        # Verify partial numbering is followed by text on the same line
        # .1 should be followed by "The intent" on the same line
        assert re.search(
            r"\.1\s+The intent", text_content
        ), "Partial numbering .1 should be followed by 'The intent' text"

        # .2 should be followed by "Available information" on the same line
        assert re.search(
            r"\.2\s+Available information", text_content
        ), "Partial numbering .2 should be followed by 'Available information' text"

        # Ensure text content is not empty and has reasonable length
        assert (
            len(text_content.strip()) > 100
        ), "MasterFormat document should have substantial text content"

    @pytest.mark.parametrize(
        "blank_lines",
        ["", "\n\n", " \n\t"],
        ids=["one-blank-line", "multiple-blank-lines", "whitespace-only-lines"],
    )
    def test_merge_partial_numbering_with_empty_lines_between(self, blank_lines):
        """Merge across blank lines while preserving surrounding text and paragraphs."""
        text = (
            "Heading\n\n"
            f".1\n{blank_lines}\nThe intent of this Request...\n"
            "Continuation.\n\n"
            f".10\n{blank_lines}\nAvailable information."
        )
        expected = (
            "Heading\n\n"
            ".1 The intent of this Request...\n"
            "Continuation.\n\n"
            ".10 Available information."
        )

        assert _merge_partial_numbering_lines(text) == expected

    def test_multiple_partial_numberings_all_merged(self):
        """Test that all partial numberings in a document are properly merged."""
        pdf_path = os.path.join(TEST_FILES_DIR, "masterformat_partial_numbering.pdf")

        markitdown = MarkItDown()
        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Count occurrences of merged partial numberings (number followed by text)
        merged_count = len(re.findall(r"\.\d+\s+[A-Za-z]", text_content))

        # Count isolated partial numberings (number alone on a line)
        isolated_count = 0
        for line in text_content.split("\n"):
            stripped = line.strip()
            if re.match(r"^\.\d+$", stripped):
                isolated_count += 1

        assert (
            merged_count >= 2
        ), f"Expected at least 2 merged partial numberings, found {merged_count}"
        assert (
            isolated_count == 0
        ), f"Found {isolated_count} isolated partial numberings that weren't merged"

    def test_merge_partial_numbering_consecutive_standalone(self):
        """Test that two consecutive partial numberings are not merged together into a single token."""
        text = (
            ".1\n"
            ".2\n"
            "Contractor shall furnish all materials.\n"
            ".3\n"
            "Work shall comply with local codes."
        )
        expected = (
            ".1\n"
            ".2 Contractor shall furnish all materials.\n"
            ".3 Work shall comply with local codes."
        )
        assert _merge_partial_numbering_lines(text) == expected

    def test_merge_partial_numbering_multiple_consecutive_and_trailing(self):
        """Test three or more consecutive partial numberings and trailing standalone numbers."""
        three_consecutive = (
            ".1\n"
            ".2\n"
            ".3\n"
            "Final requirements and specification details."
        )
        expected_three = (
            ".1\n"
            ".2\n"
            ".3 Final requirements and specification details."
        )
        assert _merge_partial_numbering_lines(three_consecutive) == expected_three

        trailing_numbers = ".1\n.2\n.3"
        expected_trailing = ".1\n.2\n.3"
        assert _merge_partial_numbering_lines(trailing_numbers) == expected_trailing

    @pytest.mark.parametrize(
        "separator",
        ["\n", "\n\n", "\n  \n\t\n"],
        ids=["single-blank-line", "multiple-blank-lines", "whitespace-lines"],
    )
    def test_merge_partial_numbering_consecutive_with_blank_lines(self, separator):
        """Test consecutive partial numbers separated by blank lines preserve their structure."""
        text = (
            f".1{separator}"
            ".2\n"
            "Contractor shall furnish all materials."
        )
        expected = (
            f".1{separator}"
            ".2 Contractor shall furnish all materials."
        )
        assert _merge_partial_numbering_lines(text) == expected

    def test_merge_partial_numbering_preceding_inline_numbered_line(self):
        """Test standalone partial number does not merge into a line already prefixed with a partial number."""
        text = (
            ".1\n"
            ".2 Contractor shall furnish all materials.\n"
            ".3 Work shall comply with local codes."
        )
        expected = (
            ".1\n"
            ".2 Contractor shall furnish all materials.\n"
            ".3 Work shall comply with local codes."
        )
        assert _merge_partial_numbering_lines(text) == expected

    @pytest.mark.parametrize(
        "first_num,second_num",
        [
            (".1", ".2"),
            (".9", ".10"),
            (".10", ".11"),
            (".99", ".100"),
            (".1", ".100"),
        ],
    )
    def test_merge_partial_numbering_varying_digit_lengths(self, first_num, second_num):
        """Test consecutive partial numbering protection across varying digit lengths."""
        text = (
            f"{first_num}\n"
            f"{second_num}\n"
            "Technical specification content."
        )
        expected = (
            f"{first_num}\n"
            f"{second_num} Technical specification content."
        )
        assert _merge_partial_numbering_lines(text) == expected

    def test_merge_partial_numbering_preserves_multiple_blank_lines_between_sections(self):
        """Test multiple blank lines between sections with consecutive numbers are preserved."""
        text = (
            "Section 01 00 00\n\n\n"
            ".1\n\n"
            "Preliminary note.\n\n\n"
            ".2\n\n"
            ".3\n\n"
            "Execution requirements.\n\n\n"
            ".4\n\n"
            "Quality assurance."
        )
        expected = (
            "Section 01 00 00\n\n\n"
            ".1 Preliminary note.\n\n\n"
            ".2\n\n"
            ".3 Execution requirements.\n\n\n"
            ".4 Quality assurance."
        )
        assert _merge_partial_numbering_lines(text) == expected

    def test_end_to_end_pdf_conversion_with_consecutive_partial_numbering(self):
        """Test full MarkItDown PDF conversion pipeline preserves consecutive partial numbering."""
        pdf_path = os.path.join(TEST_FILES_DIR, "test.pdf")
        simulated_pdfminer_text = (
            ".1\n"
            ".2\n"
            "Contractor shall furnish all materials.\n"
            ".3\n"
            "Work shall comply with local codes."
        )
        with patch("pdfminer.high_level.extract_text", return_value=simulated_pdfminer_text):
            result = MarkItDown().convert(pdf_path)

        assert ".1 .2" not in result.text_content
        assert ".1\n.2 Contractor shall furnish all materials." in result.text_content
        assert ".3 Work shall comply with local codes." in result.text_content

    @pytest.mark.parametrize(
        "non_partial_pattern",
        [
            ".5 mg",
            "1.2",
            ".a",
            "..1",
            "section .1",
            "... ellipsis",
        ],
        ids=["unit-suffix", "standard-decimal", "letter-suffix", "double-dot", "text-prefix", "ellipsis"],
    )
    def test_merge_partial_numbering_boundary_conditions(self, non_partial_pattern):
        """Test boundary conditions ensure non-partial numbering lines are unaffected."""
        text = (
            f"{non_partial_pattern}\n"
            "Following line of text."
        )
        expected = (
            f"{non_partial_pattern}\n"
            "Following line of text."
        )
        assert _merge_partial_numbering_lines(text) == expected


# Page cleanup and extraction fallback

# Tests for PDF converter memory optimization.
#
# Verifies that:
# - page.close() is called after processing each page (frees cached data)
# - Plain-text PDFs fall back to pdfminer when no form pages are found
# - Mixed PDFs use form extraction only on form-style pages


@pytest.fixture
def pdf_activity(monkeypatch):
    """Record parser activity while executing every real library operation."""
    import pdfplumber
    from markitdown.converters import _pdf_converter

    events = []
    original_open = pdfplumber.open
    original_page_close = pdfplumber.page.Page.close
    original_extract_text = _pdf_converter.pdfminer.high_level.extract_text
    original_form_extraction = _pdf_converter._extract_form_content_from_words

    def open_pdf(*args, **kwargs):
        events.append(("open", None))
        return original_open(*args, **kwargs)

    def close_page(page):
        events.append(("close", page.page_number))
        return original_page_close(page)

    def extract_text(*args, **kwargs):
        events.append(("pdfminer", None))
        return original_extract_text(*args, **kwargs)

    def extract_form(page):
        result = original_form_extraction(page)
        events.append(("form" if result is not None else "plain", page.page_number))
        return result

    monkeypatch.setattr(pdfplumber, "open", open_pdf)
    monkeypatch.setattr(pdfplumber.page.Page, "close", close_page)
    monkeypatch.setattr(
        _pdf_converter.pdfminer.high_level, "extract_text", extract_text
    )
    monkeypatch.setattr(
        _pdf_converter, "_extract_form_content_from_words", extract_form
    )
    return events


def _convert_cleanup_fixture(kind):
    return (
        MarkItDown()
        .convert(os.path.join(TEST_FILES_DIR, f"pdf_cleanup_{kind}.pdf"))
        .markdown
    )


class TestPdfMemoryOptimization:
    """Exercise page cleanup and fallback using copied, real PDF packages."""

    def test_page_close_called_on_every_page(self, pdf_activity):
        markdown = _convert_cleanup_fixture("form")
        assert markdown.count("ZAVA AUTO REPAIR") == 3
        for page in (1, 2, 3):
            extracted = pdf_activity.index(("form", page))
            closed = pdf_activity.index(("close", page))
            assert extracted < closed
            if page < 3:
                assert closed < pdf_activity.index(("form", page + 1))

    def test_plain_text_pdf_falls_back_to_pdfminer(self, pdf_activity):
        markdown = _convert_cleanup_fixture("plain")
        assert pdf_activity.count(("pdfminer", None)) == 1
        assert [(kind, page) for kind, page in pdf_activity if kind == "plain"] == [
            ("plain", 1),
            ("plain", 2),
            ("plain", 3),
        ]
        assert markdown.count("While there is contemporaneous exploration") == 3

    def test_plain_text_pdf_still_closes_all_pages(self, pdf_activity):
        _convert_cleanup_fixture("plain")
        fallback = pdf_activity.index(("pdfminer", None))
        for page in (1, 2, 3):
            extracted = pdf_activity.index(("plain", page))
            closed = pdf_activity.index(("close", page))
            assert extracted < closed < fallback
            if page < 3:
                assert closed < pdf_activity.index(("plain", page + 1))

    def test_mixed_pdf_uses_form_extraction_per_page(self, pdf_activity):
        markdown = _convert_cleanup_fixture("mixed")
        assert [
            (kind, page) for kind, page in pdf_activity if kind in ("form", "plain")
        ] == [("form", 1), ("plain", 2), ("form", 3)]
        assert ("pdfminer", None) not in pdf_activity
        assert markdown.count("ZAVA AUTO REPAIR") == 2
        assert "While there is contemporaneous exploration" in markdown
        assert "|" in markdown

    def test_only_one_pdfplumber_open_call(self, pdf_activity):
        _convert_cleanup_fixture("form")
        assert pdf_activity.count(("open", None)) == 1

    @pytest.mark.skipif(
        not os.path.exists(
            os.path.join(TEST_FILES_DIR, "REPAIR-2022-INV-001_multipage.pdf")
        ),
        reason="Multipage invoice PDF not available",
    )
    def test_real_pdf_page_cleanup(self):
        """Close each real page before the next page or document cleanup begins."""
        import pdfplumber

        events = []
        page_numbers = []
        original_extract_words = pdfplumber.page.Page.extract_words
        original_page_close = pdfplumber.page.Page.close
        original_pdf_close = pdfplumber.PDF.close

        def tracking_extract_words(page, *args, **kwargs):
            events.append(("extract", page.page_number))
            return original_extract_words(page, *args, **kwargs)

        def tracking_page_close(page):
            events.append(("close", page.page_number))
            return original_page_close(page)

        def tracking_pdf_close(pdf):
            page_numbers.extend(page.page_number for page in pdf.pages)
            events.append(("document_close", None))
            return original_pdf_close(pdf)

        with patch.object(
            pdfplumber.page.Page, "extract_words", tracking_extract_words
        ), patch.object(
            pdfplumber.page.Page, "close", tracking_page_close
        ), patch.object(
            pdfplumber.PDF, "close", tracking_pdf_close
        ):
            pdf_path = os.path.join(TEST_FILES_DIR, "REPAIR-2022-INV-001_multipage.pdf")
            MarkItDown().convert(pdf_path)

        # Assert outside the spies: conversion catches pdfplumber exceptions and
        # falls back to pdfminer, which could otherwise hide assertion failures.
        assert len(page_numbers) > 1, "The fixture must exercise multiple pages"
        document_close = events.index(("document_close", None))
        for index, page_number in enumerate(page_numbers):
            extracted = events.index(("extract", page_number))
            closed = events.index(("close", page_number))
            next_extraction = (
                events.index(("extract", page_numbers[index + 1]))
                if index + 1 < len(page_numbers)
                else document_close
            )
            assert extracted < closed < next_extraction, (
                f"Page {page_number} must be closed after extraction and before "
                f"the next page or document cleanup: {events}"
            )


# Conversion regressions

skip_remote = (
    True if os.environ.get("GITHUB_ACTIONS") else False
)  # Don't run these tests in CI

PDF_TEST_URL = "https://arxiv.org/pdf/2308.08155v2.pdf"

PDF_TEST_STRINGS = [
    "While there is contemporaneous exploration of multi-agent approaches"
]


@pytest.mark.skipif(
    skip_remote,
    reason="do not run tests that query external urls",
)
def test_markitdown_remote() -> None:
    markitdown = MarkItDown()

    # By URL
    result = markitdown.convert(PDF_TEST_URL)
    for test_string in PDF_TEST_STRINGS:
        assert test_string in result.text_content


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
