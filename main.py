"""Run all core agents sequentially."""
from pathlib import Path
import subprocess


def ensure_database():
    """Create sample DB if missing."""
    if not Path('db/scm.sqlite').exists():
        subprocess.run(['python', 'pravichain-scm/scripts/populate_sample_db.py'], check=True)


def ensure_sample_invoice() -> Path:
    """Create a demo invoice PDF for the invoice agent."""
    sample = Path('uploads/invoice_demo.pdf')
    if not sample.exists():
        sample.parent.mkdir(exist_ok=True)
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(str(sample))
        c.drawString(100, 750, 'Invoice Vendor: ACME')
        c.save()
    return sample


def main():
    ensure_database()
    invoice_path = ensure_sample_invoice()
    from pravichain_scm.agents import forecast, inventory, logistics, invoice_match

    forecast.main()
    inventory.main()
    logistics.main()
    invoice_match.run(str(invoice_path))
    print('All agents executed successfully.')


if __name__ == '__main__':
    main()
