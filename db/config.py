DB_TABLE_SETUP_SQL = [
    """
CREATE TABLE IF NOT EXISTS Logger (
  id INTEGER PRIMARY KEY,
  customer CHAR(255),
  issue CHAR(255),
  start_time TIME,
  end_time TIME,
  spent TIME,
  day DATETIME DEFAULT CURRENT_TIMESTAMP,
  date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
  date_updated DATETIME
);
""",
    """
CREATE TABLE IF NOT EXISTS Logger_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(255),
    customer CHAR(255)
);
""",
    """
CREATE TABLE IF NOT EXISTS logger_categories_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag CHAR(255),
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES category_id(id)
);
""",
]


CUSTOMER_CONF = {
    "Billable hours": [],
    "Business Development": [],
    "Competence development": [],
    "DevOps intern": [],
    "Internal communication": [],
    "Internal projects": [],
    "Malvacom Board": [],
    "Malvacom Web": [],
    "Miljöarbete": [],
}

DATABSE_FILE_LOCATION = ""

HAS_RUN_CONF = False
