import io
from markitdown.converters._csv_converter import CsvConverter
from markitdown._stream_info import StreamInfo

# Test CSV with pipe characters
csv_content = b"""name,description
John|Doe,Developer|Engineer
Alice,Manager|Lead"""

converter = CsvConverter()
stream_info = StreamInfo(extension=".csv", charset="utf-8")

result = converter.convert(
    io.BytesIO(csv_content),
    stream_info
)

print(result.markdown)
# Output should have escaped pipes:
# | name | description |
# | --- | --- |
# | John\|Doe | Developer\|Engineer |
# | Alice | Manager\|Lead |
