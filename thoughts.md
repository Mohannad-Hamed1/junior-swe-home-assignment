# Thoughts and Assumptions

## Assumptions

I consider an amount valid when it is greater than zero and no more than 1,000,000. Before conversion, I remove currency symbols, commas, and spaces and replace `O` or `o` with `0`. Missing, non-numeric, non-finite, negative, zero, and unusually large amounts are flagged. The upper limit is an assumption and should normally come from business requirements.

I accept the four date formats in the sample and normalize them to `YYYY-MM-DD`. I interpret `01/06/2024` as `MM/DD/YYYY`, making it January 6, consistent with the surrounding dates. Dates before `2020-01-01`, future dates, and impossible dates are flagged.

Vendor names and invoice IDs must not be empty. For duplicate invoice IDs, the first record is processed normally and later occurrences are flagged. Multiple problems are combined into one reason.

## Edge Cases and Validation

The main edge cases were `95O.5`, the ambiguous slash-separated date, the impossible date `2024-13-40`, and the valid but old 2019 date. I process copies so the original input remains unchanged. Parsed fields are normalized even if another field causes the record to be flagged.

I tested the exact sample with pytest. It produced two clean and six flagged records. A second test confirmed that the input was not modified. Both tests passed.

## AI Usage

I used ChatGPT to discuss requirements, review code, and prepare tests. Its first suggestion separated amount, date, vendor, and main processing logic. I shortened the code and extracted repeated missing-value handling into `clean_text`. I also questioned handling not required by the sample and reviewed the date logic line by line. ChatGPT noted that `float("NaN")` succeeds, so I added an `isfinite` check. Finally, I ran the pytest tests locally and confirmed both passed instead of accepting the proposed result without testing it.