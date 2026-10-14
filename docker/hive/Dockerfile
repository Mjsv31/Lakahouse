FROM apache/hive:4.0.0

ARG MARIADB_JDBC_VERSION=3.5.7

USER root

# MariaDB Connector/J
ADD https://repo1.maven.org/maven2/org/mariadb/jdbc/mariadb-java-client/${MARIADB_JDBC_VERSION}/mariadb-java-client-${MARIADB_JDBC_VERSION}.jar \
    /opt/hive/lib/mariadb-java-client.jar

RUN chmod 644 \
    /opt/hive/lib/mariadb-java-client.jar 

USER hive