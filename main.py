from sedona.spark import *

# 1. SETUP SEDONA (With Postgres Driver)
# Notice we added the Postgres JAR to the config
config = SedonaContext.builder() \
    .config("spark.jars.packages",
           "org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.6.1,"
           "org.datasyslab:geotools-wrapper:1.6.1-28.2,"
           "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

sedona = SedonaContext.create(config)

print("\n--- 1. Sedona is Running! ---")

# 2. CREATE DUMMY DATA (No external files needed)
data = [("Point(101.6869 3.1390)", "KL Sentral"),
        ("Point(101.7119 3.1579)", "KLCC")]

df = sedona.createDataFrame(data, ["wkt", "name"])
df_geom = df.selectExpr("ST_GeomFromWKT(wkt) as geometry", "name")

df_geom.show()

# 3. CONNECT TO DATABASE
# IMPORTANT: In Docker, the hostname is the Service Name ('sedona-db'), not 'localhost'
db_url = "jdbc:postgresql://sedona-db:5432/geodb"
db_props = {
    "user": "admin",
    "password": "password123",
    "driver": "org.postgresql.Driver"
}

print("\n--- 2. Writing to Postgres (Docker) ---")
# Convert geom to text for safe transfer
df_export = df_geom.selectExpr("name", "ST_AsText(geometry) as geom_wkt")

try:
    df_export.write.mode("overwrite").jdbc(db_url, "test_places", properties=db_props)
    print("✅ Success! Data written to table 'test_places' in Postgres.")
except Exception as e:
    print("❌ Database Error:", e)