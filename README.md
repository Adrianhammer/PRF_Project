# Transport in Europe: Motorisation and Emissions

Group 05 · Programming Foundations (PRF) · ISEG – Lisbon School of Economics and Management, 2026/27

Guilherme Miranda · Adrian Hammer · Federico Cessari · Quirin Spirkl · Aylin Akpinar

**Live app:** https://adrianhammer.pythonanywhere.com/

## Research questions

1. What explains how many cars a country has per inhabitant?
2. What explains the transport emissions per capita?

Data: six Eurostat tables, 25 European countries, 2015–2024.

## Project structure

```
├── notebooks/        data collection, cleaning, analysis and regression models
├── data/processed/   panel.csv: the cleaned dataset the app reads
├── app/              Flask web app
│   ├── data.py       TransportData class: loads and filters the data
│   ├── charts.py     Plotly chart functions
│   ├── app.py        routes (Dashboard and Explore pages)
│   ├── templates/    HTML pages
│   └── static/       CSS
├── tests/            automated tests (pytest)
├── report/           final report, PDF and DOCX
└── .github/workflows/  test and deploy pipeline
```

## Setup

You need **Python 3.10+**, **Git** and your editor of choice (if you use VS Code, install the Python and Jupyter extensions).

```bash
git clone https://github.com/Adrianhammer/PRF_Project.git
cd PRF_Project
./start.sh
```

`start.sh` creates the virtual environment (first time only), installs the packages
and starts the app at <http://127.0.0.1:5000>. Stop it with **Ctrl+C**.

<details>
<summary>Doing it manually instead</summary>

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd app
flask --app app run --debug
```
</details>

## Notebook

Open `notebooks/transport_emissions.ipynb`, select the `.venv` kernel and click **Run All**.
It downloads the data from Eurostat and saves the cleaned dataset to `data/processed/panel.csv`,
which the app reads.

## Tests

With the virtual environment active, run from the project folder:

```bash
pytest -v
```

- `tests/test_data.py`: unit tests for the `TransportData` class (filtering, years, countries, summary statistics)
- `tests/test_app.py`: tests for the web pages using Flask's test client, including invalid input

## Deployment

Every push to `main` runs a GitHub Actions workflow with two jobs:

1. **Test:** installs the requirements and runs the test suite.
2. **Deploy:** runs only if all tests pass. It uses the PythonAnywhere API to pull the latest code and reload the web app.

## Report

The final report is in `report/`, in PDF and DOCX format.