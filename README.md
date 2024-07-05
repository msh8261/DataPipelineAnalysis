# DataPipelineAnalysis

## Overview
- [Overview](#overview)
- [Pipeline](#Pipeline)
- [Architecture](#architecture)

## Pipeline 
1. Streaming: Orchestrate with Docker-compose: [https://github.com/msh8261/DataPipelineAnalysis/tree/main/1_Processing]
    - Producer streaming with Kafka
    - Consumer streaming and processing with Spark
2. Data Analysis: [https://github.com/msh8261/DataPipelineAnalysis/tree/main/2_Analysis]
    - Query with PostgreSQL
3. Dashboard: Orchestrate with Docker-compose: [https://github.com/msh8261/DataPipelineAnalysis/tree/main/3_Dashboard]
    - Visualization with Superset

## Architecture
![](images/arch.png)