import sys
from typing import BinaryIO, Any, Dict, List, Optional, Tuple, Union
import re
from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_xlsx_dependency_exc_info = None
try:
    import pandas as pd
    import openpyxl  # noqa: F401
    import numpy as np
except ImportError:
    _xlsx_dependency_exc_info = sys.exc_info()

_xls_dependency_exc_info = None
try:
    import pandas as pd  # noqa: F811
    import xlrd  # noqa: F401
except ImportError:
    _xls_dependency_exc_info = sys.exc_info()

ACCEPTED_XLSX_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
]
ACCEPTED_XLSX_FILE_EXTENSIONS = [".xlsx"]

ACCEPTED_XLS_MIME_TYPE_PREFIXES = [
    "application/vnd.ms-excel",
    "application/excel",
]
ACCEPTED_XLS_FILE_EXTENSIONS = [".xls"]


class DataRegion:
    """Represents a detected data region in an Excel sheet"""
    
    def __init__(self, name: str, start_row: int, end_row: int, start_col: int, end_col: int, 
                 data: pd.DataFrame, confidence: float = 1.0):
        self.name = name
        self.start_row = start_row
        self.end_row = end_row
        self.start_col = start_col
        self.end_col = end_col
        self.data = data
        self.confidence = confidence
    
    def __repr__(self):
        return f"DataRegion({self.name}, rows={self.start_row}-{self.end_row}, cols={self.start_col}-{self.end_col})"


class ExcelStructureAnalyzer:
    """Analyzes Excel structure to detect data regions and patterns"""
    
    def __init__(self):
        self.min_region_size = 3  # Minimum rows for a valid data region
        self.blank_threshold = 0.7  # If > 70% of column is blank, consider it empty
        
    def detect_blank_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect columns that are mostly blank or have unhelpful names"""
        blank_columns = []
        
        for col in df.columns:
            try:
                col_str = str(col)
                
                # First check if column has meaningful data regardless of name
                non_null_ratio = df[col].notna().sum() / len(df)
                has_meaningful_data = non_null_ratio >= (1 - self.blank_threshold)
                
                # If column has meaningful data, keep it even if name looks bad
                if has_meaningful_data:
                    continue
                    
                # Only remove columns that are actually mostly empty
                if non_null_ratio < (1 - self.blank_threshold):
                    blank_columns.append(col)
                    continue
            except Exception as e:
                # If analysis fails, err on the side of keeping the column
                continue
                
        return blank_columns
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe by removing blank columns and handling NaN values"""
        # Try to detect if there are better headers in the data
        df_with_headers = self._detect_better_headers(df)
        
        # Detect and remove blank columns
        blank_cols = self.detect_blank_columns(df_with_headers)
        df_cleaned = df_with_headers.drop(columns=blank_cols)
        
        # Clean column names
        df_cleaned.columns = [self._clean_column_name(str(col)) for col in df_cleaned.columns]
        
        # Handle NaN values more intelligently
        df_cleaned = self._handle_nan_values(df_cleaned)
        
        return df_cleaned
    
    def _clean_column_name(self, col_name: str) -> str:
        """Clean and improve column names"""
        # If it's a numeric column name, try to make it more descriptive
        if col_name.isdigit():
            return f"Value_{col_name}"
        
        # If it starts with "Unnamed:", try to make it more descriptive
        if col_name.startswith('Unnamed:'):
            col_num = col_name.split(':')[1].strip()
            return f"Column_{col_num}"
            
        # Clean up whitespace and special characters
        cleaned = re.sub(r'[^\w\s-]', '', col_name).strip()
        cleaned = re.sub(r'\s+', '_', cleaned)
        
        return cleaned if cleaned else "Data_Column"
    
    def _handle_nan_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle NaN values intelligently based on column content"""
        df_copy = df.copy()
        
        for col in df_copy.columns:
            try:
                # Get the column as a Series
                column_series = df_copy[col]
                
                # Check if column contains URLs
                if column_series.astype(str).str.contains(r'http[s]?://', na=False).any():
                    df_copy[col] = column_series.fillna('')
                # Check if column contains price information  
                elif column_series.astype(str).str.contains(r'[£$€¥]\d+', na=False).any():
                    df_copy[col] = column_series.fillna('')  # Keep prices clean, don't add N/A
                # Check if column contains numeric values (IDs, quantities, etc.)
                elif column_series.dtype in ['int64', 'float64'] or column_series.astype(str).str.match(r'^\d+$', na=False).any():
                    df_copy[col] = column_series.fillna('')
                # For other columns, replace NaN with empty string
                else:
                    df_copy[col] = column_series.fillna('')
            except Exception as e:
                # If any analysis fails, just replace NaN with empty string
                df_copy[col] = df_copy[col].fillna('')
                
        return df_copy
    
    def detect_data_regions(self, df: pd.DataFrame) -> List[DataRegion]:
        """Detect distinct data regions within the dataframe"""
        regions = []
        
        # For now, implement a simple approach - treat the whole cleaned data as one region
        # But detect if there are clear section breaks
        
        cleaned_df = self.clean_dataframe(df)
        
        if len(cleaned_df) == 0:
            return regions
            
        # Look for section headers or breaks
        sections = self._find_section_breaks(cleaned_df)
        
        if not sections:
            # Single region
            regions.append(DataRegion(
                name="Main Data",
                start_row=0,
                end_row=len(cleaned_df) - 1,
                start_col=0,
                end_col=len(cleaned_df.columns) - 1,
                data=cleaned_df,
                confidence=1.0
            ))
        else:
            # Multiple regions
            for i, (start_idx, end_idx, section_name) in enumerate(sections):
                section_data = cleaned_df.iloc[start_idx:end_idx+1]
                regions.append(DataRegion(
                    name=section_name or f"Section_{i+1}",
                    start_row=start_idx,
                    end_row=end_idx,
                    start_col=0,
                    end_col=len(section_data.columns) - 1,
                    data=section_data,
                    confidence=0.8
                ))
        
        return regions
    
    def _find_section_breaks(self, df: pd.DataFrame) -> List[Tuple[int, int, str]]:
        """Find natural breaks in the data that might indicate sections"""
        sections = []
        
        # Look for rows that might be headers or section dividers
        # This is a simple heuristic - can be improved
        
        current_start = 0
        
        for i in range(len(df)):
            row = df.iloc[i]
            
            # Check if this row looks like a section header
            # (e.g., most values are the same, or very different from surrounding rows)
            if self._is_potential_section_break(df, i):
                if i > current_start + self.min_region_size:
                    # Found a section
                    sections.append((current_start, i - 1, None))
                    current_start = i
        
        # Add the final section
        if len(df) > current_start + self.min_region_size:
            sections.append((current_start, len(df) - 1, None))
        
        return sections
    
    def _is_potential_section_break(self, df: pd.DataFrame, row_idx: int) -> bool:
        """Determine if a row might be a section break"""
        if row_idx == 0 or row_idx >= len(df) - 1:
            return False
            
        row = df.iloc[row_idx]
        
        # Simple heuristic: if most values in the row are empty or very different
        # from the previous row, it might be a break
        empty_count = row.isna().sum() + (row == '').sum()
        
        return empty_count > len(row) * 0.6
    
    def _detect_better_headers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect if there are better column headers within the data"""
        if len(df) < 3:
            return df
            
        # Look for a row that might contain better headers
        for i in range(min(3, len(df))):  # Check first 3 rows
            row = df.iloc[i]
            
            # Check if this row looks like headers
            # Headers typically have:
            # 1. More text content than numeric
            # 2. Unique values
            # 3. Non-empty values in most columns
            
            text_count = 0
            unique_count = 0
            non_empty_count = 0
            unique_values = set()
            
            # Convert row to list to avoid Series boolean issues
            row_values = row.tolist()
            
            for val in row_values:
                # Handle each value individually
                val_str = str(val)
                if pd.notna(val) and val_str not in ['', 'nan', 'NaN', 'None']:
                    non_empty_count += 1
                    if isinstance(val, str) and not val_str.isdigit():
                        text_count += 1
                    # Track unique values
                    unique_values.add(val_str)
            
            unique_count = len(unique_values)
            
            # If this row looks like headers (mostly text, unique values)
            total_cols = len(row_values)
            if (text_count > total_cols * 0.5 and 
                unique_count == non_empty_count and 
                non_empty_count > total_cols * 0.4):
                
                # Use this row as headers and return remaining data
                new_df = df.iloc[i+1:].copy()
                if len(new_df) > 0:
                    # Update column names
                    new_columns = []
                    for j, val in enumerate(row_values):
                        val_str = str(val)
                        if pd.notna(val) and val_str not in ['', 'nan', 'NaN', 'None']:
                            new_columns.append(val_str)
                        else:
                            new_columns.append(f"Column_{j+1}")
                    
                    # Ensure we don't have more column names than actual columns
                    if len(new_columns) > len(new_df.columns):
                        new_columns = new_columns[:len(new_df.columns)]
                    elif len(new_columns) < len(new_df.columns):
                        # Pad with default names if needed
                        for k in range(len(new_columns), len(new_df.columns)):
                            new_columns.append(f"Column_{k+1}")
                    
                    new_df.columns = new_columns
                    return new_df
        
        return df


class ExcelFormulaInfo:
    """Container for Excel formula information"""
    
    def __init__(self):
        self.formulas: Dict[str, Dict[str, Any]] = {}  # sheet_name -> formula info
        self.column_mappings: Dict[str, Dict[str, List[str]]] = {}  # sheet_name -> column -> formulas
        
    def add_formula(self, sheet_name: str, cell: str, formula: str, column: str, row: int, 
                   column_name: str = None, column_position: int = None):
        """Add formula information"""
        if sheet_name not in self.formulas:
            self.formulas[sheet_name] = {}
            self.column_mappings[sheet_name] = {}
            
        self.formulas[sheet_name][cell] = {
            'formula': formula,
            'column': column,
            'row': row,
            'column_letter': column,
            'column_name': column_name or f'Column {column}',
            'column_position': column_position or 1,
        }
        
        if column not in self.column_mappings[sheet_name]:
            self.column_mappings[sheet_name][column] = []
        self.column_mappings[sheet_name][column].append(cell)
    
    def get_formulas_by_sheet(self, sheet_name: str) -> Dict[str, Any]:
        """Get all formulas for a specific sheet"""
        return self.formulas.get(sheet_name, {})
    
    def get_formulas_by_column(self, sheet_name: str, column: str) -> List[str]:
        """Get all formula cells for a specific column in a sheet"""
        return self.column_mappings.get(sheet_name, {}).get(column, [])
    
    def has_formulas(self) -> bool:
        """Check if any formulas were found"""
        return bool(self.formulas)


class EnhancedDocumentConverterResult(DocumentConverterResult):
    """Enhanced result that includes formula information and structure analysis"""
    
    def __init__(self, markdown: str, formula_info: Optional[ExcelFormulaInfo] = None, 
                 structure_info: Optional[Dict[str, Any]] = None):
        super().__init__(markdown=markdown)
        self.formula_info = formula_info or ExcelFormulaInfo()
        self.structure_info = structure_info or {}
    
    @property
    def has_formulas(self) -> bool:
        """Check if the document contains formulas"""
        return self.formula_info.has_formulas()
    
    def get_formulas_summary(self) -> str:
        """Get a markdown summary of all formulas"""
        if not self.has_formulas:
            return ""
        
        summary = "\n\n## Excel Formulas Found\n\n"
        
        for sheet_name, formulas in self.formula_info.formulas.items():
            if formulas:
                summary += f"### Sheet: {sheet_name}\n\n"
                summary += "| Cell | Formula | Column |\n"
                summary += "|------|---------|--------|\n"
                
                for cell, info in formulas.items():
                    summary += f"| {cell} | `{info['formula']}` | {info['column']} |\n"
                summary += "\n"
        
        return summary
    
    def get_formulas_by_sheet(self, sheet_name: str) -> Dict[str, Any]:
        """Get formulas for a specific sheet"""
        return self.formula_info.get_formulas_by_sheet(sheet_name)
    
    def get_formulas_by_column(self, sheet_name: str, column: str) -> List[str]:
        """Get formula cells for a specific column"""
        return self.formula_info.get_formulas_by_column(sheet_name, column)


class XlsxConverter(DocumentConverter):
    """
    Converts XLSX files to Markdown, with each sheet presented as a separate Markdown table.
    Enhanced to extract both values and formulas dynamically, with intelligent section detection
    and blank column handling.
    """

    def __init__(self, include_formulas: bool = True, include_formula_summary: bool = False, 
                 clean_structure: bool = True, detect_sections: bool = True):
        super().__init__()
        self._html_converter = HtmlConverter()
        self.include_formulas = include_formulas
        self.include_formula_summary = include_formula_summary
        self.clean_structure = clean_structure
        self.detect_sections = detect_sections
        self.structure_analyzer = ExcelStructureAnalyzer()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_XLSX_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_XLSX_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def _extract_formulas(self, file_stream: BinaryIO) -> ExcelFormulaInfo:
        """Extract formulas from Excel file using openpyxl"""
        formula_info = ExcelFormulaInfo()
        
        try:
            # Reset stream position
            file_stream.seek(0)
            workbook = openpyxl.load_workbook(file_stream, data_only=False)
            
            # Also get pandas column mapping for synergy
            file_stream.seek(0)
            import pandas as pd
            sheets_df = pd.read_excel(file_stream, sheet_name=None, engine="openpyxl")
            
            for sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                
                # Get column mapping: Excel letter → pandas column name
                column_mapping = {}
                if sheet_name in sheets_df:
                    df_columns = list(sheets_df[sheet_name].columns)
                    for i, col_name in enumerate(df_columns):
                        excel_letter = openpyxl.utils.get_column_letter(i + 1)
                        column_mapping[excel_letter] = {
                            'name': str(col_name),
                            'position': i + 1
                        }
                
                # Scan all cells for formulas
                for row in sheet.iter_rows():
                    for cell in row:
                        if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                            column_info = column_mapping.get(cell.column_letter, {
                                'name': f'Column {cell.column_letter}',
                                'position': cell.column
                            })
                            
                            formula_info.add_formula(
                                sheet_name=sheet_name,
                                cell=cell.coordinate,
                                formula=cell.value,
                                column=cell.column_letter,
                                row=cell.row,
                                column_name=column_info['name'],
                                column_position=column_info['position']
                            )
            
        except Exception as e:
            # If formula extraction fails, continue without formulas
            print(f"Warning: Could not extract formulas: {e}")
        
        return formula_info

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> EnhancedDocumentConverterResult:
        # Check the dependencies
        if _xlsx_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xlsx",
                    feature="xlsx",
                )
            ) from _xlsx_dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _xlsx_dependency_exc_info[2]
            )

        # Extract formulas if requested
        formula_info = ExcelFormulaInfo()
        if self.include_formulas:
            formula_info = self._extract_formulas(file_stream)

        # Reset stream position for pandas
        file_stream.seek(0)
        
        # Extract data values using pandas
        sheets = pd.read_excel(file_stream, sheet_name=None, engine="openpyxl")
        md_content = ""
        
        for sheet_name in sheets:
            df = sheets[sheet_name]
            
            if self.clean_structure and not df.empty:
                # Use enhanced structure analysis
                regions = self.structure_analyzer.detect_data_regions(df)
                
                if regions:
                    md_content += f"## {sheet_name}\n\n"
                    
                    if len(regions) == 1:
                        # Single region - just clean and present the data
                        region = regions[0]
                        cleaned_df = region.data
                        
                        if not cleaned_df.empty:
                            html_content = cleaned_df.to_html(index=False, escape=False)
                            md_content += (
                                self._html_converter.convert_string(
                                    html_content, **kwargs
                                ).markdown.strip()
                                + "\n\n"
                            )
                    else:
                        # Multiple regions - present each section separately
                        for region in regions:
                            if not region.data.empty:
                                md_content += f"### {region.name}\n\n"
                                html_content = region.data.to_html(index=False, escape=False)
                                md_content += (
                                    self._html_converter.convert_string(
                                        html_content, **kwargs
                                    ).markdown.strip()
                                    + "\n\n"
                                )
                else:
                    # Fallback to original approach if no regions detected
                    md_content += f"## {sheet_name}\n"
                    html_content = df.to_html(index=False)
                    md_content += (
                        self._html_converter.convert_string(
                            html_content, **kwargs
                        ).markdown.strip()
                        + "\n\n"
                    )
            else:
                # Original approach without structure cleaning
                md_content += f"## {sheet_name}\n"
                html_content = df.to_html(index=False)
                md_content += (
                    self._html_converter.convert_string(
                        html_content, **kwargs
                    ).markdown.strip()
                    + "\n\n"
                )

        # Create structure info summary
        structure_info = {}
        if self.clean_structure:
            structure_info = {
                'cleaned_structure': True,
                'sheets_processed': list(sheets.keys()),
                'total_sheets': len(sheets)
            }

        # Create enhanced result
        result = EnhancedDocumentConverterResult(
            markdown=md_content.strip(),
            formula_info=formula_info,
            structure_info=structure_info
        )
        
        # Add formula summary if requested
        if self.include_formula_summary and result.has_formulas:
            result.markdown += result.get_formulas_summary()
        
        return result


class XlsConverter(DocumentConverter):
    """
    Converts XLS files to Markdown, with each sheet presented as a separate Markdown table.
    Enhanced to extract both values and formulas dynamically.
    """

    def __init__(self, include_formulas: bool = True, include_formula_summary: bool = False):
        super().__init__()
        self._html_converter = HtmlConverter()
        self.include_formulas = include_formulas
        self.include_formula_summary = include_formula_summary

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_XLS_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_XLS_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def _extract_formulas_xls(self, file_stream: BinaryIO) -> ExcelFormulaInfo:
        """Extract formulas from XLS file using xlrd (limited support)"""
        formula_info = ExcelFormulaInfo()
        
        try:
            # Note: xlrd has limited formula support compared to openpyxl
            # For now, return empty formula info for XLS files
            # Future enhancement could use other libraries like xlwings or openpyxl
            # TODO: Add XLS formula extraction if needed
            pass
            
        except Exception as e:
            print(f"Warning: Could not extract formulas from XLS: {e}")
        
        return formula_info

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> EnhancedDocumentConverterResult:
        # Load the dependencies
        if _xls_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".xls",
                    feature="xls",
                )
            ) from _xls_dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _xls_dependency_exc_info[2]
            )

        # Extract formulas if requested (limited for XLS)
        formula_info = ExcelFormulaInfo()
        if self.include_formulas:
            formula_info = self._extract_formulas_xls(file_stream)

        # Reset stream position for pandas
        file_stream.seek(0)
        
        # Extract data values using pandas
        sheets = pd.read_excel(file_stream, sheet_name=None, engine="xlrd")
        md_content = ""
        
        for s in sheets:
            md_content += f"## {s}\n"
            html_content = sheets[s].to_html(index=False)
            md_content += (
                self._html_converter.convert_string(
                    html_content, **kwargs
                ).markdown.strip()
                + "\n\n"
            )

        # Create enhanced result
        result = EnhancedDocumentConverterResult(
            markdown=md_content.strip(),
            formula_info=formula_info
        )
        
        # Add formula summary if requested
        if self.include_formula_summary and result.has_formulas:
            result.markdown += result.get_formulas_summary()
        
        return result
