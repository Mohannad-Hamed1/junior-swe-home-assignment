from datetime import date, datetime
from math import isfinite

MISSING_VALUES = {"", "N/A"}
MIN_DATE = date(2020, 1, 1)
DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y", "%Y/%m/%d")

def clean_text(value):
    if value is None:
        return None
    text = str(value).strip()
    if text.upper() in MISSING_VALUES:
        return None
    return text

def normalize_amount(value):
    text = clean_text(value)
    if text is None:
        return None, "Missing amount"
    text = text.replace("O", "0").replace("o", "0")
    text = text.replace("$", "").replace(",", "").replace(" ", "")
    try:
        amount = float(text)
    except ValueError:
        return None, "Invalid amount"
    if not isfinite(amount):
        return None, "Invalid amount"
    if amount <= 0:
        return amount, "Amount must be greater than zero"
    if amount > 1_000_000:
        return amount, "Amount exceeds the expected range"
    return amount, None

def normalize_date(value):
    text = clean_text(value)
    if text is None:
        return None, "Missing date"
    parsed_date = None
    for date_format in DATE_FORMATS:
        try:
            parsed_date = datetime.strptime(text, date_format).date()
            break
        except ValueError:
            continue
    if parsed_date is None:
        return None, "Invalid date"
    normalized_date = parsed_date.isoformat()
    if parsed_date < MIN_DATE:
        return normalized_date, "Date is earlier than the expected range"
    if parsed_date > date.today():
        return normalized_date, "Date cannot be in the future"
    return normalized_date, None

def process_records(raw_records: list[dict]) -> tuple[list[dict], list[dict]]:
    clean_records = []
    flagged_records = []
    seen_invoice_ids = set()
    for record in raw_records:
        processed_record = record.copy()
        reasons = []
        # Check invoice ID and duplication
        invoice_id = clean_text(record.get("invoice_id"))
        if invoice_id is None:
            reasons.append("Missing invoice_id")
        else:
            processed_record["invoice_id"] = invoice_id
            if invoice_id in seen_invoice_ids:
                reasons.append("Duplicate invoice_id")
            else:
                seen_invoice_ids.add(invoice_id)
        # Normalize amount
        amount, amount_reason = normalize_amount(record.get("amount"))
        if amount is not None:
            processed_record["amount"] = amount
        if amount_reason is not None:
            reasons.append(amount_reason)
        # Normalize date
        normalized_date, date_reason = normalize_date(record.get("date"))
        if normalized_date is not None:
            processed_record["date"] = normalized_date
        if date_reason is not None:
            reasons.append(date_reason)
        # Check vendor
        vendor = clean_text(record.get("vendor"))
        if vendor is None:
            reasons.append("Missing vendor")
        else:
            processed_record["vendor"] = vendor
        # Add the record to the appropriate output
        if reasons:
            processed_record["reason"] = "; ".join(reasons)
            flagged_records.append(processed_record)
        else:
            clean_records.append(processed_record)
    return clean_records, flagged_records