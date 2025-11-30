from pathlib import Path

# Базовые пути
DATA_DIR = Path("data")
PATH_TO_SAVE_IMAGE = DATA_DIR / "img"
PATH_TO_DATABASE = DATA_DIR / "database" 
DATA_BASE_NAME = "db.db"

# Полный путь к БД
DATABASE_URL = f"sqlite+aiosqlite:///{PATH_TO_DATABASE / DATA_BASE_NAME}"

# Путь к отчётам
REPORT_PATH = DATA_DIR / "report.xlsx"