import pandas as pd
from .config import FORMER_USSR_COUNTRIES

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

def get_top_producers(df_prod, country_groups, period=[1961,2023], product=None, top_n=10):
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

    # Validation of period
    if period[0] > period[1]:
        raise ValueError(f"End year ({period[1]}) is before start year ({period[0]}), please make sure end year is after start year")
    if period[0] < 1961:
        print("Start year is before first year in data records, switching it to 1961")
        period[0] = 1961
    if period[1] > 2023:
        print("End year is before first year in data records, switching it to 2023")
        period[1] = 2023

    # Validation of product
    if not product is None:
        if not product in df_prod["Item"].unique():
            raise ValueError(f"{product} not in Item list of FAO")

    # Validation of top_n:
    if not isinstance(top_n, int):
        raise TypeError(f"{top_n} must be an integer")
    if not top_n in range (1,211):
        raise ValueError(f"top_n must be between 1 and 210")

    # Defining mask for filtering the dataframe for prod
    mask = (~df_prod["Area"].isin(country_groups)) & \
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
