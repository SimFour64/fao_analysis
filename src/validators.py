from .config import START_YEAR, END_YEAR, COUNTRY_GROUPS

def validate_period(period: list):
    """
    Validates the period list of two integers. Raises error if invalid
    Returns the period list
    """

    if not isinstance(period, list):
        raise TypeError(f"Period must be a list of two integers, you entered a {type(period)}")

    if len(period) != 2:
        raise ValueError(f"Period must be a list of two integers, the list contains {len(period)} element(s)")

    if not isinstance(period[0], int) or not isinstance(period[1], int):
        raise TypeError("Start and End year must be integers")

    if period[0] < START_YEAR:
        print("Start year is before first year in data records -> switching it to 1961")
        period[0] = 1961
    if period[1] > END_YEAR:
        print("End year is before last year in data records -> switching it to 2023")
        period[1] = 2023

    if period[0] > period[1]:
        raise ValueError(f"End year ({period[1]}) is before start year ({period[0]}), make sure end year is after start year")

    return period


def validate_product(product, df):
    """
    Validates the product is in the list of available products from FAO data
    Raises error if invalid
    """

    if not isinstance(product, str):
        raise TypeError(f"Product is not a string. Current value : {product}")

    if not product in df["Item"].unique():
        raise ValueError(f"{product} is not in available products")


def validate_top_n(top_n, df):
    """
    Validates the top_n parameter is an integer and in the correct range
    Raises error if invalid
    """

    if not isinstance(top_n, int):
        raise TypeError("top_n must be an integer")

    number_of_countries = len(set(df["Area"]) - set(COUNTRY_GROUPS))
    if not top_n in range(1,number_of_countries+1):
        raise ValueError(f"top_n must in range 1-{number_of_countries+1}, current value: {top_n}")


def validate_countries(countries, df):
    """
    Validates list of countries are strings and in available list
    Raises error if not
    """

    try:
       iter(countries)
    except:
        raise TypeError("Countries must be an iterable!")

    countries_not_string = [country for country in countries if not isinstance(country, str)]
    if countries_not_string:
        raise TypeError(f"All countries must be strings, review: {', '.join(countries_not_string)}")

    available_countries = df["Area"].unique()
    missing_countries = [country for country in countries if not country in available_countries]
    if missing_countries:
        raise ValueError(f"Countries in list are not available in list, review: {' ,'.join(missing_countries)}")
