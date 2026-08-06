from invoice_processor import process_records
from copy import deepcopy

RAW_RECORDS = [
    {"invoice_id": "INV-1001", "amount": "$1,200.00", "date": "2024-01-05", "vendor": "Acme Corp"},
    {"invoice_id": "INV-1002", "amount": "95O.5", "date": "01/06/2024", "vendor": "Beta LLC"},
    {"invoice_id": "INV-1003", "amount": "N/A", "date": "2024-01-07", "vendor": "Acme Corp"},
    {"invoice_id": "INV-1004", "amount": "2,340", "date": "Jan 8, 2024", "vendor": ""},
    {"invoice_id": "INV-1001", "amount": "$1,200.00", "date": "2024-01-05", "vendor": "Acme Corp"},
    {"invoice_id": "INV-1005", "amount": "-450.00", "date": "2024-13-40", "vendor": "Gamma Inc"},
    {"invoice_id": "INV-1006", "amount": " ", "date": "2024/01/09", "vendor": "Delta Co"},
    {"invoice_id": "INV-1007", "amount": "3200.00", "date": "2019-01-10", "vendor": "Acme Corp"},
]

def test_process_records_with_sample_data():
    clean_records, flagged_records = process_records(RAW_RECORDS)
    assert clean_records == [
        {"invoice_id": "INV-1001", "amount": 1200.0, "date": "2024-01-05", "vendor": "Acme Corp"},
        {"invoice_id": "INV-1002", "amount": 950.5, "date": "2024-01-06", "vendor": "Beta LLC"},
    ]
    assert flagged_records == [
        {"invoice_id": "INV-1003", "amount": "N/A", "date": "2024-01-07", "vendor": "Acme Corp", "reason": "Missing amount"},
        {"invoice_id": "INV-1004", "amount": 2340.0, "date": "2024-01-08", "vendor": "", "reason": "Missing vendor"},
        {"invoice_id": "INV-1001", "amount": 1200.0, "date": "2024-01-05", "vendor": "Acme Corp", "reason": "Duplicate invoice_id"},
        {"invoice_id": "INV-1005", "amount": -450.0, "date": "2024-13-40", "vendor": "Gamma Inc", "reason": "Amount must be greater than zero; Invalid date"},
        {"invoice_id": "INV-1006", "amount": " ", "date": "2024-01-09", "vendor": "Delta Co", "reason": "Missing amount"},
        {"invoice_id": "INV-1007", "amount": 3200.0, "date": "2019-01-10", "vendor": "Acme Corp", "reason": "Date is earlier than the expected range"},
    ]

def test_process_records_does_not_modify_input():
    original_records = deepcopy(RAW_RECORDS)
    process_records(RAW_RECORDS)
    assert RAW_RECORDS == original_records