import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "etl_project"

list_of_files = [
    ".github/workflows/.gitkeep",
    ".github/workflows/main.yml",
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/utils/common.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/config/configuration.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/logging/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/cloud/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "Dockerfile",
    "setup.py",
    "notebooks/research.ipynb",
    "templates/index.html",
    ".gitignore",
    ".env"
]

# List of directories to create
list_of_dirs = [
    f"{project_name}/logging/",
    f"{project_name}/exception/",
    f"{project_name}/cloud/",
    "data/",
]



# Create directories first
for dir_path in list_of_dirs:
    dir_path = dir_path.rstrip("/")
    os.makedirs(dir_path, exist_ok=True)
    logging.info(f"Ensured directory exists: {dir_path}")

# Now create files
for file in list_of_files:
    filepath = Path(file)
    filedir, filename = os.path.split(filepath)

    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating dir: {filedir}, Creating file: {filename}")

    if not os.path.exists(filepath) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File: {filepath} already exists")

