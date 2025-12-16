# **Realtime Backend Pipeline – Portfolio Project**

Dieses Projekt implementiert eine vereinfachte Echtzeit-Datenpipeline mit Kafka, Python Microservices, PostgreSQL und einer REST-API.  
Es dient als technische Umsetzung für das IU-Modul **Datenvisualisierung und -verarbeitung (DLMDWWDE02)**.

Die Architektur besteht aus fünf Services, die Daten von Sensor-Simulation über Validierung, Aggregation, Persistenz bis zur API-Ausgabe verarbeiten.

---

## **📌 Architekturüberblick**

Die Pipeline verarbeitet Messdaten in mehreren Schritten:

1. **sensor-simulator**  
   Erzeugt synthetische Sensordaten und schreibt sie nach Kafka (`sensor_raw`).

2. **ingestion-service**  
   Liest Rohdaten, prüft sie und filtert ungültige Einträge heraus.  
   Valide Daten werden nach `sensor_clean` geschrieben.

3. **stream-processing-service**  
   Aggregiert Sensordaten in festen Zeitfenstern (bzw. Gruppengrößen)  
   und schreibt die Ergebnisse nach `sensor_agg`.

4. **storage-service**  
   Persistiert aggregierte Werte in PostgreSQL (Tabelle: `sensor_metrics`).

5. **api-service**  
   Stellt eine REST-API bereit, um die neuesten aggregierten Werte abzufragen.

---

## **🗂 Verwendete Technologien**

| Komponente | Beschreibung |
|-----------|--------------|
| **Apache Kafka** | Message Broker für Streaming |
| **Python 3.11** | Implementierung der Microservices |
| **FastAPI** | REST API Server |
| **PostgreSQL** | Persistenzschicht |
| **Docker & Docker Compose** | Orchestrierung aller Services |

---

## **📁 Projektstruktur**

```text
realtime-backend-portfolio/
│
├── docker-compose.yml
├── README.md
│
├── infra/
│   └── db/
│       └── init.sql
│
└── services/
    ├── sensor-simulator/
    │   ├── app.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── ingestion-service/
    │   ├── app.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── stream-processing-service/
    │   ├── app.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── storage-service/
    │   ├── app.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    └── api-service/
        ├── app.py
        ├── Dockerfile
        └── requirements.txt
