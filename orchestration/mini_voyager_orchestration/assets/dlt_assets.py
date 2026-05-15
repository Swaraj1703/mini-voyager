"""Dagster assets generated from the dlt ecommerce pipeline."""
import sys
from pathlib import Path

from dagster import AssetExecutionContext, AssetKey
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets

# Add the ingestion folder to Python's path so we can import the pipeline
INGESTION_DIR = Path(__file__).parent.parent.parent.parent / "ingestion" / "pipelines"
sys.path.insert(0, str(INGESTION_DIR))

from ecommerce_pipeline import ecommerce_source  # noqa: E402
import dlt  # noqa: E402

WAREHOUSE = Path(__file__).parent.parent.parent.parent / "warehouse" / "mini_voyager.duckdb"


class EcommerceDltTranslator(DagsterDltTranslator):
    """Translate dlt resource names to match dbt's source asset keys."""

    def get_asset_key(self, resource) -> AssetKey:
        # dlt resource 'customers' -> dbt source 'ecommerce.customers'
        return AssetKey(["ecommerce", resource.name])


@dlt_assets(
    dlt_source=ecommerce_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="ecommerce",
        destination=dlt.destinations.duckdb(str(WAREHOUSE)),
        dataset_name="raw_ecommerce",
    ),
    name="ecommerce",
    group_name="raw",
    dagster_dlt_translator=EcommerceDltTranslator(),
)
def ecommerce_dlt_assets(context: AssetExecutionContext, dlt_resource: DagsterDltResource):
    """Ingest e-commerce source data into the raw_ecommerce schema."""
    yield from dlt_resource.run(context=context)