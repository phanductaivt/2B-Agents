---
file_type: "Data Artifact"
primary_agents: ["Data"]
supporting_agents: ["BE"]
activation_mode: "Generated Output"
lifecycle_stage: "Project Output"
purpose: "SQLite schema plan for req-001."
---
# req-001 SQLite Schema Plan

## Table: products

```sql
create table products (
  id text primary key,
  product_code text not null unique,
  product_name text not null,
  description text,
  unit text not null,
  quantity integer not null,
  minimum_stock integer,
  status text not null,
  is_deleted integer not null default 0,
  created_at text not null,
  updated_at text not null
);
```

## Indexes

```sql
create index idx_products_code on products(product_code);
create index idx_products_name on products(product_name);
create index idx_products_deleted on products(is_deleted);
```

## Reset/Seed

Backend initializes schema and seeds sample products on startup if the table is empty.
