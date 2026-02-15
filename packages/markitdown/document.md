Test Page

1.  Parentheses in file names or strings: Bash interprets parentheses as special

characters for grouping, so they must be escaped or quoted when used as

literal characters in file names or arguments.

-  Wrong: touch sample_file(data).txt

-  Correct (Escaping): touch sample_file\\(data\\).txt

-  Correct (Quoting): touch "sample_file(data).txt"

-  Correct (Single Quotes): touch 'sample_file(data).txt'

2.  Missing keywords: This error can occur if a control structure like if, for, or

while is missing necessary keywords such as then, do, fi, or done. The shell

might be trying to interpret the code in a way that leads it to an unexpected

parenthesis.

-  Debugging tip: Check the lines immediately preceding the error for

unclosed quotes or missing keywords.

3.  Hidden characters: Copying and pasting code from Windows or other sources

into a Linux environment can introduce hidden characters (like carriage

returns, \r) that cause syntax errors.

-  Solution: Use the dos2unix tool to convert the file to Unix line endings,

or use cat -A or hexdump -C to check for invisible characters.


