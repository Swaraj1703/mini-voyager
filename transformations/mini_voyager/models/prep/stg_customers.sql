-- Prep / staging model: customers
-- One row per customer, with light cleanup and a surrogate key.

with source as (
    select * from {{ source('ecommerce', 'customers') }}
),

renamed as (
    select
        -- Surrogate key (deterministic hash of the natural key)
        {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_sk,

        -- Natural key (preserved for traceability)
        customer_id                                as customer_id,

        -- Attributes (light cleanup)
        lower(trim(email))                         as email,
        trim(first_name)                           as first_name,
        trim(last_name)                            as last_name,
        upper(trim(country))                       as country_code,
        cast(signed_up_at as timestamp)            as signed_up_at,

        -- Lineage
        _dlt_load_id                               as dlt_load_id

    from source
)

select * from renamed