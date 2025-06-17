import os
import subprocess
import sqlite3
from pathlib import Path

from pravichain_scm.agents import forecast, inventory, logistics, invoice_match

DB_PATH = Path("db/scm.sqlite")


def setup_module():
    """Prepare sample data and a test invoice."""
    subprocess.run(["python", "pravichain-scm/scripts/populate_sample_db.py"], check=True)
    os.makedirs("uploads", exist_ok=True)
    from reportlab.pdfgen import canvas
    c = canvas.Canvas("uploads/invoice_test.pdf")
    c.drawString(100, 750, "Invoice Vendor: ACME")
    c.save()


def test_forecast():
    forecast.main()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("select count(*) from forecast")
    assert cur.fetchone()[0] > 0


def test_inventory():
    inventory.main()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("select count(*) from reorder_plan")
    assert cur.fetchone()[0] > 0


def test_logistics():
    logistics.main()


def test_invoice_match():
    invoice_match.run("uploads/invoice_test.pdf")
