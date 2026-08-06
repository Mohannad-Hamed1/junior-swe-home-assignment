# Junior Software Engineer Home Assignment

This project processes raw invoice records produced by OCR and returns:

- a list of clean, normalized records
- a list of flagged records with a `reason` field

The solution normalizes amounts and dates, checks required fields, detects duplicate invoice IDs, and flags suspicious values.

## Project Files

- `invoice_processor.py` — main implementation
- `test_invoice_processor.py` — pytest tests using the provided sample data
- `thoughts.md` — assumptions, edge cases, validation, and AI usage
- `AI_Chat_History.md` — link to the AI conversation used during the assignment

## Requirements

- Python 3.9 or newer
- pytest

Install pytest:

```powershell
py -3.10 -m pip install pytest
```

## Run the Tests

From the project folder:

```powershell
py -3.10 -m pytest -v
```

Expected result:

```text
2 passed
```

The tests verify:

- the exact clean and flagged output for the provided sample data
- that the original input list is not modified

## Usage

```python
from invoice_processor import process_records

clean_records, flagged_records = process_records(raw_records)
```

`clean_records` contains valid normalized records.

`flagged_records` contains suspicious or invalid records with a `reason` field.
