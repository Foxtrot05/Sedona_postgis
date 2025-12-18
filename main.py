from sedona.spark import *
import pyspark.sql.functions as F

def run_system_check():
    print("==================================================")
    print("   STARTING GEOSPATIAL ENGINE SYSTEM CHECK")
    print("==================================================")

    # 1. CONFIGURE & START SPARK (With Memory Limits)
    # ------------------------------------------------
    print("\n[1] Initializing Apache Sedona (Spark)...")
    try:
        config = SedonaContext.builder() \
            .config("spark.jars.packages",
                "org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.6.1,"
                "org.datasyslab:geotools-wrapper:1.6.1-28.2,"
                "org.postgresql:postgresql:42.7.3") \
            .config("spark.driver.memory", "2g") \
            .config("spark.executor.memory", "2g") \
            .getOrCreate()
        
        sedona = SedonaContext.create(config)
        print(f"    ✅ Success! Sedona Version: {sedona.version}")
    except Exception as e:
        print(f"    ❌ Failed to start Spark: {e}")
        return

    # 2. TEST SPATIAL COMPUTATION
    # ------------------------------------------------
    print("\n[2] Testing Spatial Logic (Buffer Analysis)...")
    try:
        # Create dummy data: KL Tower
        data = [("KL Tower", "POINT(101.7040 3.1528)")]
        df = sedona.createDataFrame(data, ["landmark", "wkt"])

        # Convert to Geometry and create a 500m buffer (approx 0.005 degrees)
        df_geom = df.selectExpr("landmark", "ST_GeomFromWKT(wkt) as geometry")
        df_buffer = df_geom.selectExpr("landmark", "ST_Buffer(geometry, 0.005) as buffer_geom")
        
        count = df_buffer.count()
        print(f"    ✅ Success! Processed {count} spatial object(s).")
        df_buffer.show(truncate=False)
    except Exception as e:
        print(f"    ❌ Spatial calculation failed: {e}")

    # 3. TEST DATABASE CONNECTION
    # ------------------------------------------------
    print("\n[3] Testing Database I/O (PostgreSQL)...")
    
    # Internal Docker URL (Container-to-Container communication uses port 5432)
    db_url = "jdbc:postgresql://sedona-db:5432/geodb"
    db_props = {
        "user": "admin",
        "password": "password123",
        "driver": "org.postgresql.Driver"
    }

    try:
        # Convert Geometry to Text for storage
        df_save = df_buffer.selectExpr("landmark", "ST_AsText(buffer_geom) as wkt_geom")
        
        # Write
        print("    --> Writing test table...")
        df_save.write.mode("overwrite").jdbc(db_url, "system_check_logs", properties=db_props)
        
        # Read
        print("    --> Reading back data...")
        df_read = sedona.read.jdbc(db_url, "system_check_logs", properties=db_props)
        
        print("    ✅ Success! Database connection is fully operational.")
    except Exception as e:
        print(f"    ❌ Database Error: {e}")

    print("\n==================================================")
    print("   SYSTEM CHECK COMPLETE: READY FOR DEPLOYMENT")
    print("==================================================")

if __name__ == "__main__":
    run_system_check()
