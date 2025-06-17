"""Invoice Reconciliation Agent."""

import os
import pandas as pd
import pdfminer.high_level
import pytesseract
import psycopg2


def extract_text(pdf_path):
    if pdf_path.endswith('.pdf'):
        return pdfminer.high_level.extract_text(pdf_path)
    return pytesseract.image_to_string(pdf_path)


def match_invoices(text, conn):
    query = "SELECT id, vendor, amount FROM invoices;"
    invoices = pd.read_sql(query, conn)
    matches = invoices[invoices['vendor'].str.contains('ACME')]  # placeholder
    return matches


def main(pdf_path):
    conn = psycopg2.connect(dbname='scm', user='user', password='pass', host='localhost')
    text = extract_text(pdf_path)
    matches = match_invoices(text, conn)
    print('Matches found:', matches)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Usage: python invoice_match.py <pdf_path>')
