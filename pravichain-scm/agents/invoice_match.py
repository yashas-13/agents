"""Invoice Reconciliation Agent."""

import os
import pandas as pd
import pdfminer.high_level
import pytesseract
import sqlite3
import sys


def extract_text(pdf_path):
    if pdf_path.endswith('.pdf'):
        return pdfminer.high_level.extract_text(pdf_path)
    return pytesseract.image_to_string(pdf_path)


def match_invoices(text, conn):
    query = "SELECT id, vendor, amount FROM invoices;"
    invoices = pd.read_sql(query, conn)
    matches = invoices[invoices['vendor'].str.contains('ACME')]  # placeholder
    return matches


def run(pdf_path):
    if not os.path.isfile(pdf_path):
        print(f"File not found: {pdf_path}", file=sys.stderr)
        return

    if not os.path.isfile('db/scm.sqlite'):
        print("Database db/scm.sqlite not found. Run scripts/populate_sample_db.py first.", file=sys.stderr)
        return

    conn = sqlite3.connect('db/scm.sqlite')
    text = extract_text(pdf_path)
    matches = match_invoices(text, conn)
    print('Matches found:', matches)


def main():
    """Entry point for CLI usage."""
    import sys
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print('Usage: pravichain-invoice <pdf_path>')


if __name__ == '__main__':
    main()
