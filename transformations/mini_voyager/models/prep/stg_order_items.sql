-- Prep / staging model: order_items
-- One row per order line item, with light cleanup and surrogate keys.

with source as (
    select * from {{ source('ecommerce', 'order_items') }}
),

renamed as (
    select
        -- Surrogate keys
        md5(cast(order_item_id as varchar))        as order_item_sk,
        md5(cast(order_id as varchar))             as order_sk,

        -- Natural keys (preserved for traceability)
        order_item_id                               as order_item_id,
        order_id                                    as order_id,

        -- Attributes
        trim(sku)                                   as sku,
        trim(product_name)                          as product_name,
        cast(unit_price as decimal(10, 2))          as unit_price,
        cast(quantity as integer)                   as quantity,

        -- Derived field (still mechanical, not business logic)
        cast(unit_price * quantity as decimal(10, 2)) as line_total,

        -- Lineage
        _dlt_load_id                                as dlt_load_id

    from source
)

select * from renamed