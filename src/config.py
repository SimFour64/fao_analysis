import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = PROJECT_DIR / "data/raw"
PROCESSED_DIR = PROJECT_DIR / "data/processed"
EXTERNAL_DIR = PROJECT_DIR / "data/external"

SOURCES = ["Production_Crops_Livestock", "Land_Use", "Emissions_Totals", "Food_Balance"]

COLUMNS = {
    "Production_Crops_Livestock": ["Area", "Item", "Element", "Year", "Unit", "Value"],
    "Land_Use": ["Area", "Item", "Element", "Year", "Unit", "Value"],
    "Emissions_Totals": ["Area", "Item", "Element", "Year", "Unit", "Value"],
    "Food_Balance": ["Area", "Item", "Element", "Year", "Unit", "Value"]
}

COUNTRY_GROUPS = ['Africa', 'Americas', 'Asia', 'Australia and New Zealand',
       'Caribbean', 'Central America', 'Central Asia', 'Eastern Africa',
       'Eastern Asia', 'Eastern Europe', 'Europe', 'European Union (27)',
       'Land Locked Developing Countries (LLDCs)',
       'Least Developed Countries (LDCs)',
       'Low Income Food Deficit Countries (LIFDCs)', 'Melanesia',
       'Micronesia', 'Middle Africa',
       'Net Food Importing Developing Countries (NFIDCs)',
       'Northern Africa', 'Northern America', 'Northern Europe',
       'Oceania', 'Polynesia', 'Small Island Developing States (SIDS)',
       'South America', 'South-eastern Asia', 'Southern Africa',
       'Southern Asia', 'Southern Europe', 'Western Africa',
       'Western Asia', 'Western Europe', 'World', 'China, mainland']

FORMER_USSR_COUNTRIES = ['Uzbekistan', 'Kazakhstan', 'Belarus', 'Azerbaijan',
       'Lithuania', 'Tajikistan', 'Turkmenistan', 'Kyrgyzstan',
       'Republic of Moldova', 'Latvia', 'Armenia', 'Estonia', 'Georgia']

ITEM_GROUPS = ['Crops, primary', 'Live Animals', 'Livestock primary',
       'Beef and Buffalo Meat, primary', 'Butter and Ghee',
       'Cattle and Buffaloes', 'Cereals, primary', 'Cheese (All Kinds)',
       'Citrus Fruit, Total', 'Crops Processed', 'Eggs Primary',
       'Evaporated & Condensed Milk', 'Fibre Crops Primary',
       'Fibre Crops, Fibre Equivalent', 'Fruit Primary',
       'Hides and skins, primary', 'Livestock processed', 'Meat, Poultry',
       'Meat, Total', 'Milk, Total', 'Oilcrops Primary',
       'Oilcrops, Cake Equivalent', 'Oilcrops, Oil Equivalent',
       'Poultry Birds', 'Pulses, Total', 'Roots and Tubers, Total',
       'Sheep and Goat Meat', 'Sheep and Goats',
       'Skim Milk & Buttermilk, Dry', 'Sugar Crops Primary',
       'Treenuts, Total', 'Vegetables Primary']

START_YEAR = 1961
END_YEAR = 2023
