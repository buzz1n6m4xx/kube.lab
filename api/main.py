from fastapi import FastAPI
from sqlalchemy import create_engine, text
from ldap3 import Server, Connection, ALL

import os

app = FastAPI()

# --- PostgreSQL connection ---
PG_HOST = os.getenv("POSTGRES_HOST", "db")
PG_USER = os.getenv("POSTGRES_USER", "postgres")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
PG_DB = os.getenv("POSTGRES_DB", "mydb")

engine = create_engine(f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}", echo=True)

# --- LDAP connection ---
LDAP_HOST = os.getenv("LDAP_HOST", "openldap")
LDAP_USER = os.getenv("LDAP_USER", "cn=admin,dc=kube,dc=lab")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD", "admin")

server = Server(LDAP_HOST, get_info=ALL)
conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD)
conn.bind()

@app.get("/")
def root():
    return {"message": "Welcome to the API root!"}

@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI!"}

@app.get("/postgres_test")
def postgres_test():
    with engine.connect() as conn_pg:
        result = conn_pg.execute(text("SELECT NOW()"))
        return {"postgres_time": str(list(result)[0][0])}

@app.get("/users")
def get_users():
    conn.search('dc=kube,dc=lab', '(objectClass=person)', attributes=['cn', 'uid'])
    return [e.entry_to_json() for e in conn.entries]

@app.get("/groups")
def get_groups():
    conn.search('dc=kube,dc=lab', '(objectClass=posixGroup)', attributes=['cn','gidNumber'])
    return [e.entry_to_json() for e in conn.entries]
