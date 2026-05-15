-- Prod / dimension: customers
-- One row per customer, enriched with order-derived attributes.

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        customer_sk,
        count(*)                                    as total_orders,
        count(*) filter (where status = 'completed') as completed_orders,
        count(*) filter (where status = 'cancelled') as cancelled_orders,
        min(ordered_at)                              as first_ordered_at,
        max(ordered_at)                              as last_ordered_at
    from orders
    group by customer_sk
),

final as (
    select
        -- Keys
        c.customer_sk,
        c.customer_id,

        -- Customer attributes (from stg_customers)
        c.email,
        c.first_name,
        c.last_name,
        c.country_code,
        c.signed_up_at,

        -- Derived metrics (from joining orders)
        coalesce(co.total_orders,     0)            as total_orders,
        coalesce(co.completed_orders, 0)            as completed_orders,
        coalesce(co.cancelled_orders, 0)            as cancelled_orders,
        co.first_ordered_at,
        co.last_ordered_at,

        -- Customer status flag (business logic)
        case
            when co.total_orders is null then 'never_ordered'
            when co.completed_orders > 0 then 'active'
            else 'inactive'
        end                                         as customer_status,

        -- Lineage (carrying latest dlt_load_id from customer record)
        c.dlt_load_id

    from customers c
    left join customer_orders co
        on c.customer_sk = co.customer_sk
)

select * from final