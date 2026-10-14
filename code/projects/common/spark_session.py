import os
from pyspark.sql import SparkSession

def configure_s3(builder):
    return (
        builder
        .config("spark.hadoop.fs.s3a.access.key", os.environ["AWS_ACCESS_KEY_ID"])
        .config("spark.hadoop.fs.s3a.secret.key", os.environ["AWS_SECRET_ACCESS_KEY"])
    )

def configure_iceberg_catalog(builder):
    return (
        builder
        .enableHiveSupport()
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")
        .config("spark.sql.catalog.spark_catalog.type", "hive")
        .config("spark.hadoop.hive.metastore.uris", "thrift://hive-iceberg:9083")
        .config("spark.sql.warehouse.dir", "s3a://insurance-dlh-hms/warehouse/")        
    )

def configure_delta_catalog(builder):
    return (
        builder
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.catalogImplementation", "hive")
        .config("spark.hadoop.hive.metastore.uris", "thrift://hive-delta:9083")
        .config("spark.sql.warehouse.dir", "s3a://retail-dlh-hms/warehouse/")
    )

def configure_polaris_restcatalog(builder):
    return (
        builder
        .config("spark.sql.catalog.polaris", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.polaris.type", "rest")
        .config("spark.sql.catalog.polaris.uri", "http://polaris:8181/api/catalog")        
        .config("spark.sql.catalog.polaris.oauth2-server-uri", "http://polaris:8181/api/catalog/v1/oauth/tokens")        
        .config("spark.sql.catalog.polaris.scope", "PRINCIPAL_ROLE:ALL")
        .config("spark.sql.catalog.polaris.header.Polaris-Realm", "POLARIS")
        .config("spark.sql.catalog.polaris.header.X-Iceberg-Access-Delegation", "vended-credentials")
    )

def configure_insurance_polaris(builder):
    return (
        builder
        .config("spark.sql.catalog.polaris.warehouse", "insurance-dlh-rest")
        .config("spark.sql.catalog.polaris.credential",
                f"{os.environ['POLARIS_CLIENT_INSURANCE_ID_OAUTH2']}:"
                f"{os.environ['POLARIS_CLIENT_INSURANCE_SECRET_OAUTH2']}"
        ) 
    )

def configure_retail_polaris(builder):
    return (
        builder
        .config("spark.sql.catalog.polaris.warehouse", "retail-dlh-rest")
        .config("spark.sql.catalog.polaris.credential",
                f"{os.environ['POLARIS_CLIENT_RETAIL_ID_OAUTH2']}:"
                f"{os.environ['POLARIS_CLIENT_RETAIL_SECRET_OAUTH2']}"
        )        
    )

def configure_iceberg_extensions(builder):
    return (
        builder
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")        
    )

def configure_delta_extensions(builder):
    return (
        builder
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    )

def configure_iceberg_delta_extensions(builder):
    return (
        builder
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions, \
                io.delta.sql.DeltaSparkSessionExtension")
    )

def create_spark_session(app_name, configs=None):
    builder = SparkSession.builder.appName(app_name)

    for configure in configs or []:
        builder = configure(builder)

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    
    return spark