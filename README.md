# Weather ETL Pipeline (OpenWeather ➜ PostgreSQL)

Extract real-time (Hourly) weather data using OpenWeather API and insert into a PostgreSQL table for downstream use.

---
## Project Structure

```bash

weather_hourly_os/
│
├── manin.py                      # Main ETL script (run this)
├── database_manager.py           # DB connection function (get_db_connection)
├── .env                          # Environment variables (API_KEY, DB credentials)
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview and documentation

```

## Overview

This project performs a full ETL (Extract-Transform-Load) process:

- **Extract**: Fetch weather data by lat/lon from OpenWeather API  
- **Transform**: Clean and parse JSON fields (handle nulls, types)  
- **Load**: Insert into PostgreSQL (`tblWeather_daily_os`)  

---

## Example Insert Output

```bash
Complete to insert weather. (WeatherStationID: 2279, DateTime = 2025-07-22 14:54:02)
...
ETL Completed
Total successful inserts: 52
Database connection closed successfully.
```
---

## Flowchart

```mermaid
flowchart TD
    A[Start] --> B[Load .env and Connect to DB]
    B --> C[Query station master table: lat & lon]
    C --> D[Loop each station]
    D --> E[Call OpenWeather API by lat/lon]
    E --> F[Extract weather fields from JSON]
    F --> G[Transform → type conversion: float, str, datetime]
    G --> H[Insert into PostgreSQL table]
    H --> I{More stations?}
    I -->|Yes| D
    I -->|No| J[Commit & Close DB]
    J --> K[Print success count and done]

