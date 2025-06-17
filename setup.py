from pathlib import Path
from setuptools import setup, find_packages

# Read requirements
reqs = Path('requirements.txt').read_text().splitlines()

# Discover subpackages under the directory with the hyphen
subpackages = find_packages('pravichain-scm')
packages = ['pravichain_scm'] + ['pravichain_scm.' + p for p in subpackages]

setup(
    name='pravichain-scm',
    version='0.1.0',
    package_dir={'pravichain_scm': 'pravichain-scm'},
    packages=packages,
    install_requires=reqs,
    entry_points={
        'console_scripts': [
            'pravichain-forecast=pravichain_scm.agents.forecast:main',
            'pravichain-inventory=pravichain_scm.agents.inventory:main',
            'pravichain-logistics=pravichain_scm.agents.logistics:main',
            'pravichain-invoice=pravichain_scm.agents.invoice_match:main',
            'pravichain-dashboard=pravichain_scm.dashboards.app:main',
        ]
    },
)
