from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# - --------------------------------------------------
# - -- Funcion(es) de transformación
# - --------------------------------------------------

# - Nombre
def combinar_nombre_apellido(nombre, apellido):
    return f"{nombre} {apellido}"

# - Telefono
def formato_telefono(telefono):    
    tel = str(telefono)
    return '('+tel[0:3]+') '+tel[3:6]+'-'+tel[6:10]

# - Genero
def genero_completo(genero):
    if genero == "M":
        return "HOMBRE"
    if genero == "F":
        return "MUJER"
    else:
        return "DESCONOCIDO"

# - Grupo de edad
def grupo_edad(edad):
    if edad < 20:
        return "MENOR DE 20"
    if (edad >= 20) & (edad <= 29):
        return "DE 20 A 29"
    if (edad >= 30) & (edad <= 39):
        return "DE 30 A 39"
    if (edad >= 40) & (edad <= 49):
        return "DE 40 A 49"
    if (edad >= 50) & (edad <= 60):
        return "DE 50 A 60"
    else:
        return "MAYOR DE 60"

# - --------------------------------------------------
# - -- Registro de funcion(es)
# - --------------------------------------------------

# - Nombre
combinar_nombre_apellido_udf = udf(combinar_nombre_apellido, StringType())

# - Telefono
formato_telefono_udf = udf(formato_telefono, StringType())

# - Genero
genero_completo_udf = udf(genero_completo, StringType())

# - Grupo de edad
grupo_edad_udf = udf(grupo_edad, StringType())