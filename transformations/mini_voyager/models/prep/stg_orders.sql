-- Prep / staging model: orders
-- One row per order, with light cleanup and surrogate keys.

with source as (
    select * from {{ source('ecommerce', 'orders') }}
),

renamed as (
    select
        -- Surrogate keys
        {{ dbt_utils.generate_surrogate_key(['order_id']) }}    as order_sk,
        {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_sk,

        -- Natural keys (preserved for traceability)
        order_id                                    as order_id,
        customer_id                                 as customer_id,

        -- Attributes
        cast(ordered_at as timestamp)               as ordered_at,
        lower(trim(status))                         as status,

        -- Lineage
        _dlt_load_id                                as dlt_load_id

    from source
)

select * from renamed