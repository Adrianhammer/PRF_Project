from pathlib import Path

import pandas as pd
from flask import Flask

BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "panel.csv"

panel = pd.read_csv(DATA_PATH)

app = Flask(__name__)


@app.route("/")
def index():
    n_countries = panel["country"].nunique()
    first_year = panel["year"].min()
    last_year = panel["year"].max()
    return f"{n_countries} countries, {first_year}-{last_year}"


@app.route("/countries")
def countries():
    country_codes = panel["country"].unique().tolist()
    return f"{sorted(country_codes)}"
