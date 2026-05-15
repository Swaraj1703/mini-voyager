-- Prod / fact: orders
-- One row per order, with measures aggregated from order_items.

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

order_item_aggregates as (
    select
        order_sk,
        count(*)                                    as item_count,
        sum(quantity)                               as total_quantity,
        sum(line_total)                             as order_total
    from order_items
    group by order_sk
),

final as (
    select
        -- Keys
        o.order_sk,
        o.customer_sk,
        o.order_id,
        o.customer_id,

        -- Order attributes
        o.ordered_at,
        o.status,

        -- Measures (from order_items aggregation)
        coalesce(oia.item_count,      0)            as item_count,
        coalesce(oia.total_quantity,  0)            as total_quantity,
        coalesce(oia.order_total,     0)            as order_total,

        -- Date dimensions (useful for time-based slicing)
        cast(o.ordered_at as date)                  as ordered_date,
        date_trunc('month', o.ordered_at)           as ordered_month,
        date_trunc('year',  o.ordered_at)           as ordered_year,

        -- Lineage
        o.dlt_load_id

    from orders o
    left join order_item_aggregates oia
        on o.order_sk = oia.order_sk
)

select * from final