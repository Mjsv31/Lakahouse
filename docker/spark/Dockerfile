# ============================================================
# Stage 1: Spark oficial
# ============================================================
FROM apache/spark:4.1.3-scala2.13-java21-python3-ubuntu AS spark-base


# ============================================================
# Stage 2: Python oficial 3.12
# ============================================================
FROM python:3.12.14-bookworm

USER root

ARG ICEBERG_RUNTIME_VERSION=4.1_2.13
ARG ICEBERG_VERSION=1.11.0
ARG HADOOP_VERSION=3.4.2
ARG AWS_SDK_VERSION=2.29.52
ARG PY4J_VERSION=0.10.9.9
ARG DELTA_SPARK_VERSION=4.1_2.13
ARG DELTA_VERSION=4.3.1


ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/opt/java/openjdk

ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${JAVA_HOME}/bin:${PATH}"

# ------------------------------------------------------------
# Dependencias del sistema necesarias para Spark
# ------------------------------------------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        procps \
        tini \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Copiar Java 21 desde la imagen oficial de Spark
# ------------------------------------------------------------
COPY --from=spark-base /opt/java/openjdk /opt/java/openjdk

# ------------------------------------------------------------
# Copiar Spark 4.1.3 desde la imagen oficial de Spark
# ------------------------------------------------------------
COPY --from=spark-base /opt/spark /opt/spark

# ============================================================
# PySpark
# ============================================================
ENV PYTHONPATH=/opt/spark/python:/opt/spark/python/lib/pyspark.zip:/opt/spark/python/lib/py4j-${PY4J_VERSION}-src.zip

# ------------------------------------------------------------
# Iceberg
# ------------------------------------------------------------
ADD https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-${ICEBERG_RUNTIME_VERSION}/${ICEBERG_VERSION}/iceberg-spark-runtime-${ICEBERG_RUNTIME_VERSION}-${ICEBERG_VERSION}.jar \
    /opt/spark/jars/

# ------------------------------------------------------------
# Delta Lake
# ------------------------------------------------------------
ADD https://repo1.maven.org/maven2/io/delta/delta-spark_${DELTA_SPARK_VERSION}/${DELTA_VERSION}/delta-spark_${DELTA_SPARK_VERSION}-${DELTA_VERSION}.jar \
    /opt/spark/jars/

ADD https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar \
    /opt/spark/jars/

# ------------------------------------------------------------
# Hadoop AWS / S3A
# ------------------------------------------------------------
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar \
    /opt/spark/jars/

# ------------------------------------------------------------
# AWS SDK v2
# ------------------------------------------------------------
ADD https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_VERSION}/bundle-${AWS_SDK_VERSION}.jar \
    /opt/spark/jars/

RUN chmod 644 \
    /opt/spark/jars/iceberg-spark-runtime-${ICEBERG_RUNTIME_VERSION}-${ICEBERG_VERSION}.jar \
	/opt/spark/jars/delta-spark_${DELTA_SPARK_VERSION}-${DELTA_VERSION}.jar \
    /opt/spark/jars/delta-storage-${DELTA_VERSION}.jar \
    /opt/spark/jars/hadoop-aws-${HADOOP_VERSION}.jar \
    /opt/spark/jars/bundle-${AWS_SDK_VERSION}.jar

# ------------------------------------------------------------
# Workspace
# ------------------------------------------------------------
RUN mkdir -p /workspace \
    && chown -R 185:185 /workspace

# ------------------------------------------------------------
# Home de Spark
# ------------------------------------------------------------
RUN mkdir -p /home/spark \
    && chown -R 185:185 /home/spark

ENV HOME=/home/spark

# ------------------------------------------------------------
# Python dependencies
# ------------------------------------------------------------
COPY docker/spark/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ------------------------------------------------------------
# Usuario Spark
# ------------------------------------------------------------
RUN groupadd --gid 185 spark \
    && useradd \
        --uid 185 \
        --gid 185 \
        --create-home \
        --home-dir /home/spark \
        --shell /bin/bash \
        spark

RUN chown -R spark:spark /opt/spark /home/spark /workspace

USER spark

WORKDIR /workspace

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["sleep", "infinity"]