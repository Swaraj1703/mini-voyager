"""Shared Dagster resources for the mini-voyager platform."""
from pathlib import Path
from dagster_dbt import DbtProject

# Absolute path to the dbt project (transformations/mini_voyager)
DBT_PROJECT_DIR = (
    Path(__file__).parent.parent.parent  # → mini-voyager/
    / "transformations"
    / "mini_voyager"
)

# Absolute path to the dbt profiles directory (~/.dbt)
DBT_PROFILES_DIR = Path.home() / ".dbt"

# DbtProject points Dagster at your dbt project and prepares its manifest.
dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR,
)
dbt_project.prepare_if_dev()