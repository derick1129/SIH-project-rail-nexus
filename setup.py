from setuptools import setup, find_packages

setup(
    name="railway-traffic-control",
    version="0.1.0",
    description="AI-Powered Precise Train Traffic Control System",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "Flask>=2.3.3",
        "Flask-CORS>=4.0.0",
        "PuLP>=2.7.0",
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "SQLAlchemy>=2.0.21",
        "Werkzeug>=2.3.7",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "railway-control=interface.app:main",
        ],
    },
)
