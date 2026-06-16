import pandas as pd

class XlsxConverter:
    def convert(self, file_path):
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        # Drop empty rows and columns
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

        # Replace 'Unnamed:' headers with empty strings
        df.columns = ['' if col.startswith('Unnamed:') else col for col in df.columns]

        # Convert NaN values to empty strings
        df = df.fillna('')

        # Convert the DataFrame to HTML
        html = df.to_html(na_rep='')

        return html