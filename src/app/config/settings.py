import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if getattr(sys, "frozen", False):
    BASE_PATH = Path(sys._MEIPASS)
else:
    BASE_PATH = PROJECT_ROOT


PRIMARY_BLUE = "#0B4F8A"
SECONDARY_BLUE = "#1F78B4"
RED_ACCENT = "#C62828"
ORANGE_ACCENT = "#F57C00"
