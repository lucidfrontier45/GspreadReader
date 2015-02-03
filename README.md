# GspreadReader
CSV like Google Spreadsheet reader

# Usage 

```python

from gspread_reader import GspreadReader

gs = GspreadReader(<mail>, <passwd>, <sheet_name>, <sheet_id>)
header = gs.header
for line in gs:
    print gs
```
