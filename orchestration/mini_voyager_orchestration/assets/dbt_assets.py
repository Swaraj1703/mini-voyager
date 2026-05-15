"""Dagster assets generated from the dbt project."""
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from mini_voyager_orchestration.resources import dbt_project


@dbt_assets(manifest=dbt_project.manifest_path)
def mini_voyager_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """All dbt models in the mini_voyager project, exposed as Dagster assets."""
    yield from dbt.cli(["build"], context=context).stream()