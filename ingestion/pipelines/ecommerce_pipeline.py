"""dlt pipeline: ingest e-commerce source files into the Raw layer in DuckDB."""
import json
from pathlib import Path
import dlt

SOURCE_DIR = Path(__file__).parent.parent / "source_data"
WAREHOUSE  = Path(__file__).parent.parent.parent / "warehouse" / "mini_voyager.duckdb"


def _load_json(filename: str):
    """Yield records from a JSON file in source_data/."""
    with open(SOURCE_DIR / filename) as f:
        yield from json.load(f)


@dlt.resource(name="customers", primary_key="customer_id", write_disposition="merge")
def customers():
    yield from _load_json("customers.json")


@dlt.resource(name="orders", primary_key="order_id", write_disposition="merge")
def orders():
    yield from _load_json("orders.json")


@dlt.resource(name="order_items", primary_key="order_item_id", write_disposition="merge")
def order_items():
    yield from _load_json("order_items.json")


@dlt.source(name="ecommerce")
def ecommerce_source():
    return [customers(), orders(), order_items()]


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="ecommerce",
        destination=dlt.destinations.duckdb(str(WAREHOUSE)),
        dataset_name="raw_ecommerce",
    )
    load_info = pipeline.run(ecommerce_source())
    print(load_info)