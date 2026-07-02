import psycopg2

local = psycopg2.connect("postgresql://postgres:0111@localhost:5432/data_sic")
remote = psycopg2.connect("postgresql://neondb_owner:npg_XrCifF4cP0ju@ep-icy-block-aesdmdyu-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

local_cur = local.cursor()
remote_cur = remote.cursor()

tablas = [
    "rol", "usuario", "login", "categoria", "tabla_examenes",
    "facturacion", "pago_detalle", "historial_medico", "tabla_citas", "configuracion", "sessiones"
]

tablas_sql = ",".join(tablas)
remote_cur.execute(f"TRUNCATE TABLE {tablas_sql} RESTART IDENTITY CASCADE;")

for t in tablas:
    remote_cur.execute(f"SELECT * FROM {t} LIMIT 0;")
    columnas = [desc[0] for desc in remote_cur.description]
    columnas_sql = ",".join(columnas)

    local_cur.execute(f"SELECT {columnas_sql} FROM {t};")
    filas = local_cur.fetchall()
    
    if filas:
        marcadores = ",".join(["%s"] * len(columnas))
        remote_cur.executemany(f"INSERT INTO {t} ({columnas_sql}) VALUES({marcadores});", filas)
remote.commit()
print("listo madfaca")