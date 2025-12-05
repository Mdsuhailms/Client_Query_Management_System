

# ==> DATABASE CONNECTION..

import psycopg2

def db_connection():
    return psycopg2.connect(
        host = "localhost",
        database = "Client_Query_Management_System",
        user = "postgres",
        password = "Suhlpga",
        port = 5432
    )



