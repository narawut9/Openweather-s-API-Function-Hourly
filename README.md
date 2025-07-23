# 🌦️ OpenWeather Daily ETL

ETL script for extracting daily weather forecast data from the OpenWeather API and loading it into a PostgreSQL database.


---

## 📁 Project Structure

```
weather_daily_os/
├── .env # API keys and DB credentials (not included in repo)
├── .gitignore # Ignore .env, pycache, etc.
├── database_manager.py # Database connection manager
├── openweather_daily.py # Main script to run the ETL process
└── requirements.txt # Python dependencies
```

## Flow diagram
```
[Start]
   ↓
[Load .env Config]
   ↓
[Connect to PostgreSQL]
   ↓
[SELECT weather_station_id, lat, lon FROM tblWeather_station_tmd]
   ↓
[Loop: each station]
   ↓
[Call OpenWeather API (daily forecast)]
   ↓
[Check response + Extract daily[]]
   ↓
[Loop: each day in daily[]]
   ↓
[Transform → INSERT INTO tblWeather_daily_os]
   ↓
[Commit]
   ↓
[End]

```
---

## Flowchart

graph TD

    A[Start] --> B(Load Environment Variables);
    B --> C{Connect to PostgreSQL Database};
    C --> D(Initialize DB Connection and Cursor);

    D --> E[Function: get_weather_station_id_list];
    E --> F{Execute SQL Query: SELECT weather_station_id, latitude, longitude FROM tblWeather_station_tmd};
    F --> G{Fetch All Results};
    G --> H(Process Rows into List of Dictionaries);
    H --> I[Return List of Stations];
    I -- Stations List --> J{Loop Through Each Station};

    J --> K{Extract Station ID, Lat, Lon};
    K --> L[Function: fetch_weather_daily];
    L --> M{Construct OpenWeatherMap API URL};
    M --> N{Send GET Request to API};
    N --> O{Parse JSON Response};
    O --> P[Return Weather Data (JSON)];
    P -- Weather Data --> Q{Extract and Transform Weather Data Fields (e.g., obs_datetime, temp, rain_1h)};
    Q --> R{Handle Missing/Invalid Data (Set to None)};

    R --> S{Prepare SQL INSERT Query for tblWeather_daily_os};
    S --> T{Execute INSERT Query with Data};
    T --> U{Commit Transaction to Database};
    U --> V{Increment Successful Insert Count};
    V --> W{Log Success/Failure for Station};
    W -- Loop End --> J;

    J -- All Stations Processed --> X[Print ETL Completion Summary];
    X --> Y{Close Database Connection};
    Y --> Z[End];

    %% Error Paths
    C -. Error .-> ErrorDBConnect(Handle DB Connection Error);
    E -. Error .-> ErrorGetStations(Log Error & Return Empty List);
    L -. Error .-> ErrorFetchWeather(Log API Error & Return None);
    Q -. Error .-> ErrorExtractTransform(Set Field to None);
    S -. Error .-> ErrorInsert(Log DB Insert Error for Station);
    Y -. Error .-> ErrorDBClose(Log DB Close Error);

