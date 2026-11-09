import pandas as pd

COUNTRY_NAMES = {
    "AT": "Austria",
    "BE": "Belgium",
    "CH": "Switzerland",
    "CY": "Cyprus",
    "CZ": "Czechia",
    "DE": "Germany",
    "DK": "Denmark",
    "EE": "Estonia",
    "ES": "Spain",
    "FI": "Finland",
    "FR": "France",
    "HR": "Croatia",
    "HU": "Hungary",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "MT": "Malta",
    "NL": "Netherlands",
    "NO": "Norway",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SE": "Sweden",
    "SI": "Slovenia",
    "TR": "Türkiye",
}

INDICATORS = {
    "emission_pc": "Transport emissions per person (tonnes CO₂-eq)",
    "cars_per_1000": "Cars per 1000 inhabitants",
    "old_cars_share": "Share of cars older than 10 years (%)",
    "gdp_pc": "GDP per person (euro, 2020 prices)",
    "density": "Population density (people per km²)",
    "emission_total": "Total transport emissions (thousand tonnes CO₂-eq)",
}


class TransportData:
    """Loads the cleaned panel data and answers questions about it"""
    def __init__(self, csv_path):
        """Read the CSV into self.df and add a 'country_name' column."""
        self.df = pd.read_csv(csv_path)
        self.df["country_name"] = self.df["country"].map(COUNTRY_NAMES)

    def countries(self):
        """Return a sorted list of (code, name) pairs, e.g. ("PT", "Portugal")."""
        country_codes = sorted(self.df["country"].unique())
        pairs = []
        for code in country_codes:
            pairs.append((code, COUNTRY_NAMES[code]))
        return pairs

    def year_range(self):
        """Return the first and last year in the data as a tuple."""
        min_year = int(self.df["year"].min())
        max_year = int(self.df["year"].max())
        return min_year, max_year

    def filter(self, countries, start_year, end_year):
        """Return only the rows for these countries and years."""
        in_countries = self.df["country"].isin(countries)
        in_years = self.df["year"].between(start_year, end_year)
        return self.df[in_countries & in_years]

    def one_year(self, year):
        """Return all countries for a single year (for bar charts and scatter plots)."""
        is_year = self.df["year"] == year
        return self.df[is_year]

    def key_stats(self, df, indicator):
        """Return a dict of headline numbers for one indicator in a filtered table."""
        if df.empty:
            return None
        
        first_year = int(df["year"].min())
        latest_year = int(df["year"].max())

        first = df[df["year"] == first_year]
        latest = df[df["year"] == latest_year]

        avg_first = first[indicator].mean()
        avg_latest = latest[indicator].mean()

        change_pct = (avg_latest - avg_first) / avg_first * 100

        ranked = latest.sort_values(indicator)
        lowest = ranked.iloc[0]
        highest = ranked.iloc[-1]

        return {
            "first_year": first_year,
            "latest_year": latest_year,
            "average": float(round(avg_latest, 2)),
            "change_pct": float(round(change_pct, 1)),
            "highest": highest["country_name"],
            "lowest": lowest["country_name"],
        }


if __name__ == "__main__":
    data = TransportData("../data/processed/panel.csv")
    subset = data.filter(["PT", "ES", "FR", "DE"], 2018, 2024)
    print(data.key_stats(subset, "emission_pc"))
