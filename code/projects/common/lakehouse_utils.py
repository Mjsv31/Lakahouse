from pyspark.sql.functions import expr, col

def iceberg_upsert(df_source, target_table, join_columns, partition_column=None):
    on_condition = " AND ".join([f"{target_table}.{c} = source.{c}" for c in join_columns])
    if partition_column:
        on_condition += f" AND {target_table}.{partition_column} = source.{partition_column}"
        
    columns = df_source.columns
    # Columnas para actualizar sin llaves de unión
    update_dict = {c: col(f"source.{c}") for c in columns if c not in join_columns}
    # Columnas para insertar
    insert_dict = {c: col(f"source.{c}") for c in columns}

    # Ejecución nativa mergeInto de Spark 4
    (
        df_source.alias("source")
        .mergeInto(target_table, expr(on_condition))
        .whenMatched()
        .update(update_dict)
        .whenNotMatched()
        .insert(insert_dict)
        .merge()
    )