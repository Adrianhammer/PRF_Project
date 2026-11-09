import plotly.express as px

from data import INDICATORS


def _to_html(fig):
    """Turn a plotly figure into an HTML snippet for a template"""
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def line_chart(df, indicator):
    """Line chart of one indicator over time, one line per country."""
    fig = px.line(
        df,
        x="year",
        y=indicator,
        color="country_name",
        markers=True,
        labels={
            "year": "Year",
            indicator: INDICATORS[indicator],
            "country_name": "Country",
        },
    )
    return _to_html(fig)


def bar_chart(df, indicator):
    """Bar chart of one indicator of for a single year, one bar per country, highest first"""
    fig = px.bar(
        df.sort_values(indicator, ascending=False),
        x="country_name",
        y=indicator,
        labels={
            indicator: INDICATORS[indicator],
            "country_name": "Country",
        },
    )
    return _to_html(fig)


def scatter_chart(df):
    """Scatter plot of cars per 1000 inhabitants vs emissions per person, one dot per country"""
    fig = px.scatter(
        df,
        x="cars_per_1000",
        y="emission_pc",
        hover_name="country_name",
        text="country",
        labels={
            "cars_per_1000": INDICATORS["cars_per_1000"],
            "emission_pc": INDICATORS["emission_pc"],
        },
    )
    fig.update_traces(textposition="top center")
    return _to_html(fig)


def trend_chart(df, indicator):
    """Trend chart"""
    fig = px.line(
        df,
        x="year",
        y=indicator,
        markers=True,
        labels={
            "year": "Year",
            indicator: INDICATORS[indicator],
        },
    )
    return _to_html(fig)
