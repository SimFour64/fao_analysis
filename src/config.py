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
