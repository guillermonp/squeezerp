"""
resources: includes paths
"""

import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PATHS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PRJ_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_UPLOADER_PATH_XLS = os.path.join(PRJ_PATH, "resources", "data_uploader.xls")
DATA_UPLOADER_PATH_CSV = os.path.join(PRJ_PATH, "resources", "data_uploader.csv")
DATABASE = os.path.join(PRJ_PATH, "resources", "database.db")
DATABASE_SCHEMA = os.path.join(PRJ_PATH, "database", "database_schema.sql")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ICONS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ICON_LOGO = os.path.join(PRJ_PATH, "gui", "imgs", "icon.png")
ICON_ERROR = os.path.join(PRJ_PATH, "gui", "imgs", "error.png")
ICON_CSV = os.path.join(PRJ_PATH, "gui", "imgs", "csv.png")
ICON_XLS = os.path.join(PRJ_PATH, "gui", "imgs", "xls.png")
ICON_PASS = os.path.join(PRJ_PATH, "gui", "imgs", "pass.png")
ICON_MINI_WAIT = os.path.join(PRJ_PATH, "gui", "imgs", "mini_wait.png")
ICON_HISTORY = os.path.join(PRJ_PATH, "gui", "imgs", "history.png")
