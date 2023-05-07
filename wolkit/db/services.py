from db import _cursor, _connection
from lib.services import Service, services


def create_services_table():
    _cursor.execute("""CREATE TABLE IF NOT EXISTS services (
        name TEXT PRIMARY KEY,
        description TEXT,
        active INTEGER NOT NULL
    );""")

    ss = []
    for s_name, s in services.items():
        ss.append((s_name, s[0], s[1]))

    _cursor.executemany("""INSERT OR IGNORE INTO services VALUES (?, ?, ?)""", ss)


def get_services():
    return [Service(**{
        "name": s[0],
        "description": s[1],
        "active": s[2] == 1
    }) for s in _cursor.execute("SELECT * FROM services;").fetchall()]


def set_service(service_name: str, new_value: bool):
    service = _cursor.execute("SELECT * FROM services WHERE name=?", [service_name]).fetchone()
    if service is None:
        raise ValueError(f"Service {service_name} not found")

    enabled = service[2] == 1
    if new_value == enabled:
        raise ValueError(f"Service {service_name} already {'enabled' if enabled else 'disabled'}")

    _cursor.execute("UPDATE services SET active=? WHERE name=?;", (new_value, service_name))
    _connection.commit()


def set_all_services(new_value: bool):
    _cursor.execute("UPDATE services SET active=?;", (1 if new_value else 0))
    _connection.commit()