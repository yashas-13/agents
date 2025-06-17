import subprocess
import sys
from pathlib import Path


def run(cmd, **kwargs):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True, **kwargs)


def install_requirements():
    run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])


def setup_database():
    run([sys.executable, 'pravichain-scm/scripts/populate_sample_db.py'])


def init_agents():
    from pravichain_scm.agents import forecast, inventory, logistics, invoice_match
    # ensure sample invoice
    sample = Path('uploads/invoice_demo.pdf')
    if not sample.exists():
        sample.parent.mkdir(exist_ok=True)
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(str(sample))
        c.drawString(100, 750, 'Invoice Vendor: ACME')
        c.save()
    forecast.main()
    inventory.main()
    logistics.main()
    invoice_match.run(str(sample))


def start_services():
    api_proc = subprocess.Popen([
        sys.executable,
        '-m',
        'uvicorn',
        'pravichain_scm.api.main:app',
        '--host',
        '127.0.0.1',
        '--port',
        '8000',
    ])
    dash_proc = subprocess.Popen([sys.executable, 'pravichain-scm/dashboards/app.py'])
    print('API running at http://127.0.0.1:8000')
    print('Dashboard running at http://127.0.0.1:8050')
    api_proc.wait()
    dash_proc.wait()


def main():
    install_requirements()
    setup_database()
    init_agents()
    start_services()


if __name__ == '__main__':
    main()
