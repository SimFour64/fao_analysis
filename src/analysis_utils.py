import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .config import FORMER_USSR_COUNTRIES, COUNTRY_GROUPS, ITEM_GROUPS
from .validators import validate_period, validate_product, validate_top_n, validate_countries

def merge_former_ussr_countries(df_prod):
    """
    Manage former USSR countries by : grouping all of their production values
    within "Former USSR Countries" area name, except for Russian Federation and
    for Ukraine, given their production volumes compared to other countries.

    Args:
        - df_prod (pd.DataFrame): dataframe containing FAO Data for production

    Returns:
        - pd.DataFrame: same as df_prod but production for former USSR countries
            are aggregated under "Former USSR Countries" area name. Production
            for Russia and Ukraine are untouched.
    """
    # Retrieving and aggregating production for former USSR Countries
    df_prod_ussr = df_prod[df_prod["Area"].isin(FORMER_USSR_COUNTRIES)].groupby(["Item","Element","Year","Unit"]).sum().reset_index()
    df_prod_ussr["Area"] = "Former USSR Countries"

    # Dropping individual productions for former USSR Countries in initial dataset
    df_no_ussr = df_prod[~df_prod["Area"].isin(FORMER_USSR_COUNTRIES)]

    # Merging both dataset and resetting index
    df_merge = pd.concat((df_no_ussr, df_prod_ussr)).reset_index(drop=True)

    return df_merge


def get_historical_production(df_prod, countries=None, period=[1961,2023], product=None):
    """
    Computes the historical agricultural production for a list of countries
    during the given period for the given product. If product is not specified,
    it aggregates over all products.
    Args:
        - df_prod (pd.DataFrame): dataframe listing all productions
        - countries (list [str]): list of countries to compute and aggregate
        - period (list [int, int]): start and end dates
        - product (str): product on which to computes and aggregate.
            Default: None, meaning aggregation on all products.

    Returns:
        - pd.DataFrame: DataFrame listing aggregated yearly production on the
            given period for each country
    """
    # Validation of inputs
    if not countries is None:
        validate_countries(countries, df_prod)
    period = validate_period(period)
    if not product is None:
        validate_product(product, df_prod)

    # Defining mask for filtering the dataframe for prod
    mask = (df_prod["Year"] >= period[0]) & (df_prod["Year"] <= period[1])

    if not countries is None:
        mask &= (df_prod["Area"].isin(countries)) # Countries if specified
    else:
        mask &= (~df_prod["Area"].isin(COUNTRY_GROUPS)) # All countries without country groups

    if not product is None:
        mask &= (df_prod["Item"] == product)

    # Filtering the DF
    df_filtered = df_prod[mask]

    # Grouping to get historical yearly production data for each country
    historical_production = df_filtered.groupby(["Area","Year"])["Value"] \
                .sum() \
                .reset_index()

    return historical_production


def get_historical_rank(df_prod, countries=None, period=[1961,2023], product=None):
    """
    Computes the rank for each country, for each year, for production

    Args:
        - df_prod (pd.DataFrame): dataframe listing all productions
        - countries (list [str]): list of countries to compute and aggregate
        - period (list [int, int]): start and end dates
        - product (str): product on which to computes and aggregate.
            Default: None, meaning aggregation on all products.

    Returns:
        - pd.DataFrame: DataFrame listing yearly rank on the given period for
            each country
    """
    # Getting historical production
    historical_production = get_historical_production(df_prod, countries, period, product)

    # Ranking the countries
    historical_production["Rank"] = historical_production.groupby("Year")["Value"] \
                                            .rank(ascending=False) \
                                            .astype(int)

    return historical_production


def get_top_producers(df_prod, period=[1961,2023], product=None, top_n=10):
    """
    Returns a DataFrame listing countries that are top producers for a specific
    product (opt.) over a period of time (opt.) and the cumumlated values in
    Gtons

    Args:
        - df_prod (pd.DataFrame): dataframe containing FAO Data for production
        - period (list): [start_year, end_year] between 1961 and 2023. Raises
            an error if start_ear > end_year
        - product (str): items on which to get top producers. Raises an error
            if not in Item list of FAO. Default: None, meaning global production
        - top_n: number of top countries to retrieve info on. Raises an error
            if not int or not in (1,210) range
            Default: 10

    Returns:
        - top_producers_values (pd.DataFrame): Dataframe listing top producers
            and the cumulated productions during period
    """

    # Validation of inputs
    validate_top_n(top_n, df_prod)

    # Getting historical data values and ranks
    historical = get_historical_production(df_prod)

    # Grouping and summing production over the period
    historical = historical[(historical["Year"] >= 1961) & (historical["Year"] <= 2023)]

    # Filtering on top_n
    top_producers = historical.groupby("Area")[["Value"]]\
        .sum()\
        .sort_values(by="Value", ascending=False)\
        .nlargest(n=top_n, columns="Value")

    return top_producers


def get_country_production_items(df_prod, country, period=[1961,2023]):
    """
    Computes the production for each "Item", ie Product, for a given country

    Args:
        - df_prod (pd.DataFrame): dataframe listing all productions
        - country (str): unique country on which to compute and aggregate
        - period (list [int, int]): start and end dates

    Returns:
        - pd.DataFrame: listing year by year production for each Item
    """

    # Validation of inputs
    validate_countries([country],df_prod)
    period = validate_period(period)

    # Grouping data
    country_prod = df_prod[(df_prod["Area"]==country) & (df_prod["Item"].isin(ITEM_GROUPS))]\
                            .groupby(["Item","Year"])[["Value"]]\
                            .sum()\
                            .reset_index()

    return country_prod


def get_report_country_on_item(df_prod, country, product):
    """
    Produces a report for one country on one specific product:
        - Plot the production over whole period and compares with global prod
        - Computes shares of global production 1961 vs. 2023
        - Displays top 5 producers of item in 2023

    Args:
        - df_prod (pd.DataFrame): dataframe listing all productions
        - country (str): unique country on which to compute and aggregate
        - product (str): item on which report is run

    Returns:
        - Display of the report
    """

    ###########################################
    # 1 - Production and comparison to global #
    ###########################################
    # --- Data prep ---
    historic_country = get_historical_production(df_prod,
                                                 countries=[country],
                                                 period=[1961,2023],
                                                 product=product)

    historic_world = get_historical_production(df_prod,
                                               countries=None,
                                               period=[1961,2023],
                                               product=product)\
                                                    .groupby("Year")[["Value"]]\
                                                    .sum()\
                                                    .reset_index()
    # --- Plotting
    plt.figure(figsize=(12,6))
    # Country prod
    plt.stackplot(historic_country["Year"],
                historic_country["Value"],
                labels=[country])
    # Global prod
    sns.lineplot(data=historic_world,
                 x="Year",
                 y="Value",
                 label="World",
                 color="r",
                 ls="--")
    # Plot setup
    plt.title(f"Evolution {country} production of {product} compared to global world production 1961-2023")
    plt.xlim([1961,2023])
    plt.xlabel(None)
    plt.ylabel("Production in Gtons")
    plt.show()

    #####################################################
    # 2 - Shares of country in global prod 1961 vs 2023 #
    #####################################################
    # Share in 1961
    share_1961 = round((historic_country[historic_country["Year"]==1961]["Value"]/historic_world[historic_world["Year"]==1961]["Value"] * 100).values[0],2)
    # Share in 2023
    share_2023 = round((historic_country[historic_country["Year"]==2023]["Value"]/historic_world[historic_world["Year"]==2023]["Value"] * 100).values[0],2)
    # Displaying result
    print(f"""
          Share of {product} production in 1961 compared to global: {share_1961}%
          Share of {product} production in 2023 compared to global: {share_2023}%
          """)

    #######################################
    # 3 - Global Top5 in 2023 for product #
    #######################################
    historic_product = get_historical_production(df_prod,
                                     period=[1961,2023],
                                     product=product)

    top5 = historic_product.groupby(["Area"])[["Value"]]\
                            .sum()\
                            .nlargest(n=5, columns="Value")

    return top5
