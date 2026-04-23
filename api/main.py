from fastapi import FastAPI
from sqlalchemy import create_engine, text
from ldap3 import Server, Connection, ALL, SUBTREE

import os

app = FastAPI()

# --- PostgreSQL connection ---
# -- Set environment variables in local .env file, otherwise these fallback variables are used --
PG_HOST = os.getenv("POSTGRES_HOST", "db")
PG_USER = os.getenv("POSTGRES_USER", "postgres")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
PG_DB = os.getenv("POSTGRES_DB", "mydb")

engine = create_engine(f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}", echo=True)

# --- LDAP connection ---
# -- Set environment variables in local .env file, otherwise these fallback variables are used --
LDAP_HOST = os.getenv("LDAP_HOST", "openldap")
LDAP_USER = os.getenv("LDAP_USER", "cn=admin,dc=kube,dc=lab")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD", "admin")

# Define the port (389 for standard, 636 for LDAPS)
# Note: use_ssl=True is required if using port 636
LDAP_PORT = 389 

# Initialize Server with explicit port
server = Server(LDAP_HOST, port=LDAP_PORT, get_info=ALL)

# Initialize Connection with auto_bind
# Use AUTO_BIND_NO_TLS for standard or AUTO_BIND_TLS_BEFORE_BIND for SSL
def get_ldap_conn():
    return Connection(
        server,
        user=LDAP_USER,
        password=LDAP_PASSWORD,
        auto_bind=True
    )

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
    conn = get_ldap_conn()
    conn.search('dc=kube,dc=lab', '(objectClass=person)', attributes=['cn', 'uid'])
    return [entry.entry_attributes_as_dict for entry in conn.entries]

@app.get("/groups")
def get_groups():
    conn = get_ldap_conn()
    conn.search(
        'dc=kube,dc=lab',
        '(objectClass=groupOfNames)',
        search_scope=SUBTREE,
        attributes=['cn', 'member']
    )
    return [entry.entry_attributes_as_dict for entry in conn.entries]

@app.get("/posixgroups")
def get_posixgroup():
    conn = get_ldap_conn()
    conn.search(
        'dc=kube,dc=lab',
        '(objectClass=posixGroup)',
        search_scope=SUBTREE,
        attributes=['cn', 'memberUid']
    )
    return [entry.entry_attributes_as_dict for entry in conn.entries]
