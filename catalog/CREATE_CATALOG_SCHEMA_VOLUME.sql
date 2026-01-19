-- Databricks notebook source
CREATE CATALOG IF NOT EXISTS `docker-workshop`
MANAGED LOCATION 's3://data4all-lake-dev/docker-workshop'
COMMENT 'Catálogo criado para hospedar os dados do Postgres - projeto Docker Workshop, do Bootcamp de Engenharia de Dados 2026';

-- COMMAND ----------

GRANT ALL PRIVILEGES
ON CATALOG `docker-workshop`
TO `joaocardoso.dataengineer@outlook.com`;

-- COMMAND ----------

CREATE SCHEMA IF NOT EXISTS `docker-workshop`.`stg`
MANAGED LOCATION 's3://data4all-lake-dev/docker-workshop/stg'
COMMENT '[STAGING LAYER] - Camada centralizadora de ingestão de dados brutos para o projeto Docker Workshop, em formato DELTA.';

-- COMMAND ----------

GRANT ALL PRIVILEGES
ON SCHEMA `docker-workshop`.`stg`
TO `joaocardoso.dataengineer@outlook.com`;

-- COMMAND ----------

CREATE EXTERNAL VOLUME IF NOT EXISTS `docker-workshop`.`stg`.`landzone`
LOCATION 's3://data4all-lake-dev/docker-workshop/stg/landzone'
COMMENT '[RAW SOURCE] - Volume centralizador de ingestão de dados brutos para o projeto Docker Workshop.';

-- COMMAND ----------

GRANT ALL PRIVILEGES
ON VOLUME `docker-workshop`.`stg`.`landzone`
TO `joaocardoso.dataengineer@outlook.com`;
