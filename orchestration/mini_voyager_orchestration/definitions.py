"""Dagster Definitions for the mini-voyager platform.

This is the entry point Dagster loads to discover all assets, resources,
and configuration for the project.
"""
from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_dlt import DagsterDltResource

from mini_voyager_orchestration.assets.dbt_assets import mini_voyager_dbt_assets
from mini_voyager_orchestration.assets.dlt_assets import ecommerce_dlt_assets
from mini_voyager_orchestration.resources import dbt_project, DBT_PROFILES_DIR

defs = Definitions(
    assets=[mini_voyager_dbt_assets, ecommerce_dlt_assets],
    resources={
        "dbt": DbtCliResource(
            project_dir=dbt_project,
            profiles_dir=str(DBT_PROFILES_DIR),
        ),
        "dlt_resource": DagsterDltResource(),
    },
)