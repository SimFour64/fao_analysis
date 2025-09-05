import pandas as pd
from .config import FORMER_USSR_COUNTRIES, COUNTRY_GROUPS, ITEM_GROUPS
from .validators import validate_period, validate_product, validate_top_n, validate_countries

def merge_former_ussr_countries(df_prod):
    """
    Manage former USSR countries by : grouping all of their production values wihtin "Former USSR Countries" area name, except
    for Russian Federation and for Ukraine, given their production volumes compared to other countries.

    Args:
        - df_prod (pd.DataFrame): dataframe containing FAO Data for production

    Returns:
        - pd.DataFrame: same as df_prod but production for former USSR countries are aggregated under "Former USSR Countries" area name.
        Production for Russia and Ukraine are untouched.
    """
    # Retrieving and aggregating production for former USSR Countries
    df_prod_ussr = df_prod[df_prod["Area"].isin(FORMER_USSR_COUNTRIES)].groupby(["Item","Element","Year","Unit"]).sum().reset_index()
    df_prod_ussr["Area"] = "Former USSR Countries"

    # Dropping individual productions for former USSR Countries in initial dataset
    df_no_ussr = df_prod[~df_prod["Area"].isin(FORMER_USSR_COUNTRIES)]

    # Merging both dataset and resetting index
    df_merge = pd.concat((df_no_ussr, df_prod_ussr)).reset_index(drop=True)

    return df_merge


def get_top_producers(df_prod, period=[1961,2023], product=None, top_n=10):
    """
    Returns a DataFrame listing countries that are top producers for a specific product (opt.) over a period of time (opt.) and the cumumlated values in Gtons

    Args:
        - df_prod (pd.DataFrame): dataframe containing FAO Data for production
        - country_groups (np.ndarray): np array containing names of country groups as defined by FAO
        - period (list): [start_year, end_year] between 1961 and 2023. Raises an error if start_ear > end_year
        - product (str): items on which to get top producers. Raises an error if not in Item list of FAO. Default: None, meaning global production
        - top_n: number of top countries to retrieve info on. Raises an error if not int or not in (1,210) range Default: 10

    Returns:
        - top_producers_values (pd.DataFrame): Dataframe listing top producers and the cumulated productions during period
    """

    # Validation of inputs
    period = validate_period(period)

    if not product is None:
        validate_product(product, df_prod)

    validate_top_n(top_n, df_prod)

    # Defining mask for filtering the dataframe for prod
    mask = (~df_prod["Area"].isin(COUNTRY_GROUPS)) & \
            (df_prod["Year"] >= period[0]) & \
            (df_prod["Year"] <= period[1])

    if not product is None:
        mask = mask & (df_prod["Item"] == product)

    # Filtering the DF
    df_filtered = df_prod[mask]

    # Grouping and getting only top_n countries
    top_producers_values = df_filtered.groupby("Area")[["Value"]]\
                            .sum()\
                            .sort_values(by="Value", ascending=False)\
                            .nlargest(top_n, columns="Value")

    return top_producers_values


def get_historical_production(df_prod, countries, period=[1961,2023], product=None):
    """
    Computes the historical agricultural production for a list of countries during the given period
    for the given product. If product is not specified, it aggregates over all products.
    Args:
        - df_prod (pd.DataFrame): dataframe listing all productions
        - countries (list [str]): list of countries to compute and aggregate
        - period (list [int, int]): start and end dates
        - product (str): product on which to computes and aggregate. Default: None, meaning
        aggregation on all products.

    Returns:
        - pd.DataFrame: DataFrame listing aggregated yearly production on the given period for each country
    """
    # Validation of inputs
    validate_countries(countries, df_prod)
    period = validate_period(period)
    if not product is None:
        validate_product(product, df_prod)

    # Defining mask for filtering the dataframe for prod
    mask = (df_prod["Area"].isin(countries)) & \
            (df_prod["Year"] >= period[0]) & \
            (df_prod["Year"] <= period[1])

    if not product is None:
        mask = mask & (df_prod["Item"] == product)

    # Filtering the DF
    df_filtered = df_prod[mask]

    # Grouping and pivoting to get historical yearly production data
    historical_production = df_filtered.groupby(["Area","Year"])["Value"] \
                .sum() \
                .reset_index() \
                .pivot(index="Area",columns="Year", values="Value")

    # Sorting in descending values from last year for plot purposes
    last_year_rank = historical_production[period[1]].sort_values(ascending=False).index
    historical_production = historical_production.reindex(last_year_rank)

    # Filling na
    historical_production = historical_production.fillna(0)

    return historical_production


def get_historical_rank(df_prod, countries, period=[1961,2023], product=None, top_n=10):
    """
    Computes the rank for each country, for each year, for production, and filter
    only for countries that has been one year in top_n

    Args:
        - df_prod (pd.DataFrame): dataframe listing all productions
        - countries (list [str]): list of countries to compute and aggregate
        - period (list [int, int]): start and end dates
        - product (str): product on which to computes and aggregate. Default: None, meaning
        aggregation on all products.

    Returns:
        - pd.DataFrame: DataFrame listing yearly rank on the given period for each country
    """

    # Validation of top_n (other validation are done in calling other functions)
    validate_top_n(top_n, df_prod)

    # Getting historical production
    historical_production = get_historical_production(df_prod, countries, period, product)

    # Ranking the countries
    rank_production = historical_production.rank(ascending=False).astype(int)

    # Filtering only for countries that has been one day in top_n
    countries_in_top_n = rank_production[rank_production.min(axis=1) <= top_n].index
    rank_production = rank_production.reindex(countries_in_top_n)

    return rank_production


def get_country_production_items(df_prod, country, period=[1961,2023]):
    """
    Computes the production for each "Item", ie Product, for a given country

    Args:
        - df_prod (pd.DataFrame): dataframe listing all productions
        - countries (str): unique country on which to compute and aggregate
        - period (list [int, int]): start and end dates

    Returns:
        - pd.DataFrame: listing year by year production for each Item
    """

    # Validation of inputs
    validate_countries([country],df_prod)
    period = validate_period(period)

    country_prod = df_prod[(df_prod["Area"]==country) & (df_prod["Item"].isin(ITEM_GROUPS))]\
                            .groupby(["Item","Year"])[["Value"]]\
                            .sum()\
                            .reset_index()

    return country_prod
