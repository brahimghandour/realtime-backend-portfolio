CREATE TABLE IF NOT EXISTS sensor_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    avg_temperature REAL,
    avg_humidity REAL,
    count INTEGER
);
