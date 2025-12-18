# 🌍 Apache Sedona: High-Performance Spatial Computing
**Author:** Imran Mazlan
**Date:** December 2025

---

## 1. What is Apache Sedona?
Apache Sedona (formerly GeoSpark) is a **cluster computing system for processing large-scale spatial data**.

Think of it as **"Pandas/SQL but for Maps"**—but instead of running on a single laptop, it runs on **Spark**, which allows it to process **millions of coordinate points** in seconds.

### **Why Do We Need It?**
Standard tools like `ArcGIS`, `QGIS`, or Python's `GeoPandas` are great for *visualizing* data, but they often crash or become incredibly slow when you try to calculate:
* "Which of these 10 million GPS points are inside a forest reserve?"
* "Calculate the distance between 500,000 GrabFood orders and 20,000 restaurants."

**Sedona solves this by:**
1.  **Distributing the load:** Breaking the map into small chunks and processing them in parallel.
2.  **Spatial Indexing:** Using R-Tree/Quad-Tree indexes to instantly find nearby points (instead of scanning the whole map).

---

## 2. Core Features (The "Engine")

### **A. Spatial SQL**
You can write standard SQL queries with special "ST" (Spatial Type) functions.
> **Example:** `ST_Contains(forest_boundary, illegal_logging_point)`

### **B. Spatial RDD & DataFrame**
It extends Spark DataFrames to understand "Geometry" columns. It can natively read:
* Shapefiles (.shp)
* GeoJSON
* WKT (Well-Known Text)
* WKB (Well-Known Binary)

### **C. Geometry Serialization**
It efficiently compresses complex shapes (polygons of states like Pahang or Sarawak) so they travel fast across the network.

---

## 3. Example Use Cases in Malaysia

Here are three practical scenarios where we would use Sedona instead of standard Python scripts.

### **Use Case 1: Flood Risk Analysis (Banjir) in Kelantan**
* **Problem:** We have 5 million historical rainfall points and a complex polygon map of Kelantan's river basins. We need to identify which villages are in "High Risk" zones based on rainfall density.
* **Sedona Solution:**
    1.  Load the **River Basin Polygons** (Complex Shapes).
    2.  Load **5 Million Rainfall Points** (CSV/Parquet).
    3.  Run a **Spatial Join**:
        ```python
        # "Find all rain points that fall inside the flood zone"
        df_risk = sedona.sql("""
            SELECT village_name, count(*) as rain_intensity
            FROM rain_data, flood_zones
            WHERE ST_Contains(flood_zones.geometry, rain_data.geometry)
            GROUP BY village_name
        """)
        ```

### **Use Case 2: Palm Oil Plantation Monitoring**
* **Problem:** We have satellite detection data (YOLO output) showing 200,000 detected palm trees. We need to verify if these trees are inside a **Legal Concession** or an **Illegal Forest Reserve**.
* **Sedona Solution:**
    * Use `ST_Intersects` to check millions of tree points against the Forestry Department's boundary map in seconds.

### **Use Case 3: Telco Coverage Optimization (5G)**
* **Problem:** Maximizing 5G coverage in Kuala Lumpur.
* **Sedona Solution:**
    * Create 500m buffers around every existing tower: `ST_Buffer(tower_point, 0.005)`.
    * Overlay this with population density data to find "blind spots" (areas with high population but no coverage).

---

## 4. Key Functions Cheat Sheet

| Function | Description | Example SQL |
| :--- | :--- | :--- |
| **ST_GeomFromWKT** | Converts text to geometry | `ST_GeomFromWKT('POINT(101.7 3.1)')` |
| **ST_Contains** | Checks if Shape A is inside Shape B | `ST_Contains(state_poly, city_point)` |
| **ST_Distance** | Calculates distance (in degrees) | `ST_Distance(p1, p2)` |
| **ST_Buffer** | Creates a circle/zone around a point | `ST_Buffer(point, 0.01)` |
| **ST_Intersects** | Checks if two shapes touch/overlap | `ST_Intersects(road, river)` |

---

## 5. Why Docker?
We use Docker for Sedona because installing **Spark + Java + Scala + Python + GEOS** on a local Windows/Ubuntu laptop is extremely difficult and fragile. Docker guarantees that if it works on my machine, it works on the server/cloud.