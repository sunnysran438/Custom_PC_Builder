import sqlite3
from contextlib import contextmanager
from typing import Any, Iterable, Optional

DB_NAME = "parts_picker.db"

PART_TYPES = [
    "psu",
    "case",
    "fan",
    "ethernet_controller",
    "motherboard",
    "air_cooler",
    "liquid_cooler",
    "m2_storage",
    "hhd_storage",
    "sata_storage",
    "gpu",
    "cpu",
    "ram",
    "wifi_module",
]

# order matters for deletion of subtype tables first
DELETE_ORDER = [
    "POWER_SUPPLY_CONNECTORS",
    "CASE_RADIATOR_SPACE",
    "CASE_IO_PORT",
    "CASE_FORM_FACTOR_COMPATIBLE",
    "CASE_FAN_SIZE_COMPATIBLE",
    "MOTHERBOARD_IO_PORTS",
    "MOTHERBOARD_PCI_SLOT",
    "AIR_COOLER",
    "LIQUID_COOLER",
    "CPU_COOLER",
    "M2_STORAGE",
    "HHD_STORAGE",
    "SATA_STORAGE",
    "STORAGE",
    "POWER_SUPPLY_UNIT",
    "PC_CASE",
    "FAN",
    "MOTHERBOARD",
    "ETHERNET_CONTROLLER",
    "GPU",
    "RAM",
    "CPU",
    "WIFI_MODULE",
    "STORE_ITEM",
    "CONTAINS_COMPONENT",
    "COMPONENT",
    "LIST_PART",
]

PART_TABLES_FOR_SEARCH = [
    "POWER_SUPPLY_UNIT",
    "PC_CASE",
    "FAN",
    "ETHERNET_CONTROLLER",
    "MOTHERBOARD",
    "AIR_COOLER",
    "LIQUID_COOLER",
    "M2_STORAGE",
    "HHD_STORAGE",
    "SATA_STORAGE",
    "GPU",
    "CPU",
    "RAM",
    "WIFI_MODULE",
]


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _rows_to_dicts(rows: Iterable[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(r) for r in rows]


def _fetch_all(conn: sqlite3.Connection, query: str, params: tuple = ()) -> list[dict[str, Any]]:
    cur = conn.cursor()
    cur.execute(query, params)
    return _rows_to_dicts(cur.fetchall())


def _fetch_one(conn: sqlite3.Connection, query: str, params: tuple = ()) -> Optional[dict[str, Any]]:
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    return dict(row) if row else None


def _scalar(conn: sqlite3.Connection, query: str, params: tuple = (), default=None):
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    if not row:
        return default
    value = row[0]
    return default if value is None else value


def _next_id(conn: sqlite3.Connection, table: str, column: str) -> int:
    return int(_scalar(conn, f"SELECT COALESCE(MAX({column}), -1) + 1 FROM {table}", default=0))


def manual_query(query: str, params: tuple = ()) -> list[dict[str, Any]] | bool:
    """
    For admin/debug only.
    """
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            if cur.description is not None:
                return _rows_to_dicts(cur.fetchall())
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def create_tables():
    """
    Rebuilds the whole database and reseeds sample data.
    WARNING: destructive.
    """
    schema = """
    PRAGMA foreign_keys = OFF;

    DROP TABLE IF EXISTS CASE_FORM_FACTOR_COMPATIBLE;
    DROP TABLE IF EXISTS CASE_FAN_SIZE_COMPATIBLE;

    DROP TABLE IF EXISTS WIFI_MODULE;
    DROP TABLE IF EXISTS CPU;
    DROP TABLE IF EXISTS RAM;
    DROP TABLE IF EXISTS GPU;
    DROP TABLE IF EXISTS SATA_STORAGE;
    DROP TABLE IF EXISTS HHD_STORAGE;
    DROP TABLE IF EXISTS M2_STORAGE;
    DROP TABLE IF EXISTS STORAGE;
    DROP TABLE IF EXISTS LIQUID_COOLER;
    DROP TABLE IF EXISTS AIR_COOLER;
    DROP TABLE IF EXISTS CPU_COOLER;
    DROP TABLE IF EXISTS MOTHERBOARD_PCI_SLOT;
    DROP TABLE IF EXISTS MOTHERBOARD_IO_PORTS;
    DROP TABLE IF EXISTS MOTHERBOARD;
    DROP TABLE IF EXISTS ETHERNET_CONTROLLER;
    DROP TABLE IF EXISTS FAN;
    DROP TABLE IF EXISTS CASE_IO_PORT;
    DROP TABLE IF EXISTS CASE_RADIATOR_SPACE;
    DROP TABLE IF EXISTS PC_CASE;
    DROP TABLE IF EXISTS POWER_SUPPLY_CONNECTORS;
    DROP TABLE IF EXISTS POWER_SUPPLY_UNIT;
    DROP TABLE IF EXISTS MOTHERBOARD_FORM_FACTOR;
    DROP TABLE IF EXISTS PCI_SLOT;
    DROP TABLE IF EXISTS RAM_TYPE;
    DROP TABLE IF EXISTS CPU_SOCKET_TYPE;
    DROP TABLE IF EXISTS FAN_SIZE;
    DROP TABLE IF EXISTS CONTAINS_COMPONENT;
    DROP TABLE IF EXISTS BUILD_LIST;
    DROP TABLE IF EXISTS COMPONENT;
    DROP TABLE IF EXISTS STORE_ITEM;
    DROP TABLE IF EXISTS LIST_PART;
    DROP TABLE IF EXISTS SUPPLIER;
    DROP TABLE IF EXISTS MANUFACTURER;
    DROP TABLE IF EXISTS CUSTOMER;

    CREATE TABLE CUSTOMER(
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        last_name TEXT,
        postal_code TEXT NOT NULL,
        street_no TEXT NOT NULL,
        city TEXT NOT NULL,
        province TEXT NOT NULL,
        country TEXT NOT NULL
    );

    CREATE TABLE MANUFACTURER(
        manufacturer_id INTEGER PRIMARY KEY,
        manufacturer_name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE SUPPLIER(
        supplier_id INTEGER PRIMARY KEY,
        supplier_name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE LIST_PART(
        list_part_id INTEGER PRIMARY KEY
    );

    CREATE TABLE STORE_ITEM(
        item_number INTEGER PRIMARY KEY,
        supplier_id INTEGER NOT NULL,
        price REAL NOT NULL,
        list_part_id INTEGER NOT NULL,
        FOREIGN KEY(supplier_id) REFERENCES SUPPLIER(supplier_id) ON DELETE CASCADE,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE,
        UNIQUE(supplier_id, list_part_id)
    );

    CREATE TABLE COMPONENT(
        part_id INTEGER PRIMARY KEY,
        manufacturer_id INTEGER NOT NULL,
        list_part_id INTEGER NOT NULL UNIQUE,
        FOREIGN KEY(manufacturer_id) REFERENCES MANUFACTURER(manufacturer_id) ON DELETE CASCADE,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE BUILD_LIST(
        list_number INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES CUSTOMER(customer_id) ON DELETE CASCADE
    );

    CREATE TABLE CONTAINS_COMPONENT(
        list_number INTEGER NOT NULL,
        list_part_id INTEGER NOT NULL,
        num_components INTEGER NOT NULL,
        PRIMARY KEY(list_number, list_part_id),
        FOREIGN KEY(list_number) REFERENCES BUILD_LIST(list_number) ON DELETE CASCADE,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE FAN_SIZE(
        size_category_mm INTEGER PRIMARY KEY
    );

    CREATE TABLE CPU_SOCKET_TYPE(
        socket_type TEXT PRIMARY KEY
    );

    CREATE TABLE RAM_TYPE(
        ram_type TEXT PRIMARY KEY
    );

    CREATE TABLE PCI_SLOT(
        pci_type_id INTEGER PRIMARY KEY,
        pci_version TEXT NOT NULL,
        pin_count INTEGER NOT NULL,
        UNIQUE(pci_version, pin_count)
    );

    CREATE TABLE MOTHERBOARD_FORM_FACTOR(
        form_factor TEXT PRIMARY KEY
    );

    CREATE TABLE POWER_SUPPLY_UNIT(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        power_rating INTEGER NOT NULL,
        modular INTEGER NOT NULL,
        length_mm INTEGER NOT NULL,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE POWER_SUPPLY_CONNECTORS(
        list_part_id INTEGER NOT NULL,
        conn_type TEXT NOT NULL,
        num_pins INTEGER NOT NULL,
        count INTEGER NOT NULL,
        PRIMARY KEY(list_part_id, conn_type, num_pins),
        FOREIGN KEY(list_part_id) REFERENCES POWER_SUPPLY_UNIT(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE PC_CASE(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        height INTEGER,
        width INTEGER,
        len_case INTEGER,
        material TEXT,
        num_35_bays INTEGER,
        num_25_bays INTEGER,
        max_gpu_len_mm INTEGER,
        max_psu_len_mm INTEGER,
        max_air_cooler_height INTEGER,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE CASE_RADIATOR_SPACE(
        list_part_id INTEGER NOT NULL,
        loc_in_case TEXT NOT NULL,
        height INTEGER,
        width INTEGER,
        len_rad INTEGER,
        PRIMARY KEY(list_part_id, loc_in_case),
        FOREIGN KEY(list_part_id) REFERENCES PC_CASE(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE CASE_IO_PORT(
        list_part_id INTEGER NOT NULL,
        con_version TEXT NOT NULL,
        generation TEXT NOT NULL,
        con_type TEXT NOT NULL,
        count INTEGER NOT NULL,
        PRIMARY KEY(list_part_id, con_version, generation, con_type),
        FOREIGN KEY(list_part_id) REFERENCES PC_CASE(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE FAN(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        fan_rpm INTEGER,
        noise_level REAL,
        size_category_mm INTEGER NOT NULL,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(size_category_mm) REFERENCES FAN_SIZE(size_category_mm)
    );

    CREATE TABLE ETHERNET_CONTROLLER(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE MOTHERBOARD(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        num_ram_slots INTEGER,
        chipset_name TEXT,
        num_sata_connectors INTEGER,
        num_cooler_headers INTEGER,
        num_fan_headers INTEGER,
        form_factor TEXT NOT NULL,
        socket_type TEXT NOT NULL,
        ram_type TEXT NOT NULL,
        ethernet_con_id INTEGER,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(form_factor) REFERENCES MOTHERBOARD_FORM_FACTOR(form_factor),
        FOREIGN KEY(socket_type) REFERENCES CPU_SOCKET_TYPE(socket_type),
        FOREIGN KEY(ram_type) REFERENCES RAM_TYPE(ram_type),
        FOREIGN KEY(ethernet_con_id) REFERENCES ETHERNET_CONTROLLER(list_part_id)
    );

    CREATE TABLE MOTHERBOARD_IO_PORTS(
        list_part_id INTEGER NOT NULL,
        con_version TEXT NOT NULL,
        generation TEXT NOT NULL,
        con_type TEXT NOT NULL,
        count INTEGER NOT NULL,
        PRIMARY KEY(list_part_id, con_version, generation, con_type),
        FOREIGN KEY(list_part_id) REFERENCES MOTHERBOARD(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE MOTHERBOARD_PCI_SLOT(
        list_part_id INTEGER NOT NULL,
        pci_type_id INTEGER NOT NULL,
        num_slots INTEGER NOT NULL,
        PRIMARY KEY(list_part_id, pci_type_id),
        FOREIGN KEY(list_part_id) REFERENCES MOTHERBOARD(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(pci_type_id) REFERENCES PCI_SLOT(pci_type_id)
    );

    CREATE TABLE CPU_COOLER(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        noise_level INTEGER,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE AIR_COOLER(
        list_part_id INTEGER PRIMARY KEY,
        fan_rpm INTEGER,
        height INTEGER,
        FOREIGN KEY(list_part_id) REFERENCES CPU_COOLER(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE LIQUID_COOLER(
        list_part_id INTEGER PRIMARY KEY,
        num_fans INTEGER,
        len_cool INTEGER,
        width INTEGER,
        height INTEGER,
        fan_rpm INTEGER,
        cooling_tube_length INTEGER,
        FOREIGN KEY(list_part_id) REFERENCES CPU_COOLER(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE STORAGE(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        capacity INTEGER,
        read_speed INTEGER,
        write_speed INTEGER,
        form_factor TEXT,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE M2_STORAGE(
        list_part_id INTEGER PRIMARY KEY,
        pci_type_id INTEGER NOT NULL,
        FOREIGN KEY(list_part_id) REFERENCES STORAGE(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(pci_type_id) REFERENCES PCI_SLOT(pci_type_id)
    );

    CREATE TABLE HHD_STORAGE(
        list_part_id INTEGER PRIMARY KEY,
        interface TEXT,
        FOREIGN KEY(list_part_id) REFERENCES STORAGE(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE SATA_STORAGE(
        list_part_id INTEGER PRIMARY KEY,
        interface TEXT,
        FOREIGN KEY(list_part_id) REFERENCES STORAGE(list_part_id) ON DELETE CASCADE
    );

    CREATE TABLE GPU(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        series TEXT,
        architecture TEXT,
        base_clock INTEGER,
        boost_clock INTEGER,
        memory_size INTEGER,
        memory_type TEXT,
        num_cores INTEGER,
        power_consumption INTEGER,
        pci_type_id INTEGER NOT NULL,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(pci_type_id) REFERENCES PCI_SLOT(pci_type_id)
    );

    CREATE TABLE RAM(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        max_freq INTEGER NOT NULL,
        ram_type TEXT NOT NULL,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(ram_type) REFERENCES RAM_TYPE(ram_type)
    );

    CREATE TABLE CPU(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        chip_family TEXT NOT NULL,
        series TEXT NOT NULL,
        tdp INTEGER NOT NULL,
        base_clock INTEGER,
        boost_clock INTEGER,
        l1_cache INTEGER,
        l2_cache INTEGER,
        l3_cache INTEGER,
        num_cores INTEGER,
        num_threads INTEGER,
        architecture TEXT,
        socket_type TEXT NOT NULL,
        ram_type TEXT NOT NULL,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(socket_type) REFERENCES CPU_SOCKET_TYPE(socket_type),
        FOREIGN KEY(ram_type) REFERENCES RAM_TYPE(ram_type)
    );

    CREATE TABLE WIFI_MODULE(
        list_part_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        pci_type_id INTEGER NOT NULL,
        FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(pci_type_id) REFERENCES PCI_SLOT(pci_type_id)
    );

    CREATE TABLE CASE_FORM_FACTOR_COMPATIBLE(
        case_id INTEGER NOT NULL,
        form_factor TEXT NOT NULL,
        PRIMARY KEY(case_id, form_factor),
        FOREIGN KEY(case_id) REFERENCES PC_CASE(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(form_factor) REFERENCES MOTHERBOARD_FORM_FACTOR(form_factor)
    );

    CREATE TABLE CASE_FAN_SIZE_COMPATIBLE(
        case_id INTEGER NOT NULL,
        size_category_mm INTEGER NOT NULL,
        PRIMARY KEY(case_id, size_category_mm),
        FOREIGN KEY(case_id) REFERENCES PC_CASE(list_part_id) ON DELETE CASCADE,
        FOREIGN KEY(size_category_mm) REFERENCES FAN_SIZE(size_category_mm)
    );

    PRAGMA foreign_keys = ON;
    """

    with get_connection() as conn:
        conn.executescript(schema)
        _seed_database(conn)


def _seed_database(conn: sqlite3.Connection):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO CUSTOMER VALUES
        (1, 'Art', 'middlename', 'Vandeley', 'A0A 0A0', '123-routeway', 'New York', 'New York', 'U.S.A')
    """)

    cur.executemany(
        "INSERT INTO MANUFACTURER (manufacturer_id, manufacturer_name) VALUES (?, ?)",
        [
            (1, "Nvidia"),
            (2, "Intel"),
            (3, "AMD"),
            (4, "Corsair"),
            (5, "Asus"),
            (6, "G.SKILL"),
            (7, "Qualcomm"),
            (8, "MSI"),
            (9, "GIGABYTE"),
            (10, "Arctic"),
            (11, "Seagate"),
            (12, "Realtek"),
        ],
    )

    cur.executemany(
        "INSERT INTO SUPPLIER (supplier_id, supplier_name) VALUES (?, ?)",
        [
            (1, "Amazon"),
            (2, "Newegg"),
            (3, "Memory Express"),
            (4, "Best Buy"),
        ],
    )

    cur.executemany(
        "INSERT INTO LIST_PART (list_part_id) VALUES (?)",
        [(i,) for i in range(1, 13)],
    )

    cur.executemany(
        "INSERT INTO COMPONENT (part_id, manufacturer_id, list_part_id) VALUES (?, ?, ?)",
        [
            (1, 8, 1),
            (2, 4, 2),
            (3, 4, 3),
            (4, 2, 4),
            (5, 9, 5),
            (6, 10, 6),
            (7, 11, 7),
            (8, 3, 8),
            (9, 4, 9),
            (10, 3, 10),
            (11, 12, 11),
            (12, 5, 12),
        ],
    )

    cur.executemany(
        "INSERT INTO STORE_ITEM (item_number, supplier_id, price, list_part_id) VALUES (?, ?, ?, ?)",
        [
            (1, 1, 100.0, 12),
            (2, 2, 100.0, 11),
            (3, 3, 100.0, 10),
            (4, 4, 100.0, 9),
            (5, 1, 100.0, 8),
            (6, 2, 100.0, 7),
            (7, 3, 200.0, 1),
            (8, 3, 120.0, 2),
            (9, 3, 20.0, 3),
            (10, 3, 100.0, 4),
            (11, 3, 250.0, 5),
            (12, 3, 220.0, 6),
        ],
    )

    cur.execute("INSERT INTO BUILD_LIST (list_number, customer_id) VALUES (1, 1)")
    cur.execute("INSERT INTO CONTAINS_COMPONENT (list_number, list_part_id, num_components) VALUES (1, 1, 1)")

    cur.executemany("INSERT INTO FAN_SIZE (size_category_mm) VALUES (?)", [(90,), (120,), (140,), (200,)])

    cpu_sockets = [
        "Socket sTR5", "Socket SP6", "Socket SP5", "Socket AM5", "Socket sWRX8",
        "Socket sTRX4", "Socket TR4", "Socket SP3", "Socket AM4", "Socket AM1",
        "Socket FM2+", "Socket FM2", "Socket AM3+", "Socket FS1", "Socket FM1",
        "Socket C32", "Socket C34", "Socket AM3", "rPGA 988A", "LGA 1156",
        "LGA 1567", "LGA 1155", "rPGA 988B", "LGA 1356", "LGA 1150",
        "rPGA 946B/947", "LGA 2011", "LGA 1151", "LGA 3647", "LGA 2066",
        "LGA 4189", "LGA 1200", "LGA 1700", "LGA 4677", "LGA 1851",
        "LGA 4710", "LGA 7529",
    ]
    cur.executemany("INSERT INTO CPU_SOCKET_TYPE (socket_type) VALUES (?)", [(s,) for s in cpu_sockets])

    cur.executemany("INSERT INTO RAM_TYPE (ram_type) VALUES (?)", [("DDR1",), ("DDR2",), ("DDR3",), ("DDR4",), ("DDR5",)])

    cur.executemany(
        "INSERT INTO PCI_SLOT (pci_type_id, pci_version, pin_count) VALUES (?, ?, ?)",
        [
            (0, "PCIe 5.0", 16),
            (1, "PCIe 4.0", 16),
            (2, "PCIe 3.0", 16),
            (3, "PCIe 2.0", 16),
            (4, "PCIe 5.0", 4),
            (5, "PCIe 4.0", 4),
            (6, "PCIe 3.0", 4),
            (7, "PCIe 2.0", 4),
        ],
    )

    cur.executemany(
        "INSERT INTO MOTHERBOARD_FORM_FACTOR (form_factor) VALUES (?)",
        [("ATX",), ("Micro-ATX",), ("Mini-ATX",), ("XT",), ("Mini-ITX",), ("Nano-ITX",), ("Pico-ITX",), ("Mobile-ITX",)],
    )

    cur.execute(
        "INSERT INTO POWER_SUPPLY_UNIT VALUES (?, ?, ?, ?, ?)",
        (1, "MPG A1000GS PCIE5, FULLY Modular", 1000, 1, 150),
    )
    cur.executemany(
        "INSERT INTO POWER_SUPPLY_CONNECTORS VALUES (?, ?, ?, ?)",
        [
            (1, "ATX", 28, 1),
            (1, "CPU/PCIe", 8, 3),
            (1, "SATA/Peripheral", 6, 3),
            (1, "12V 2x6", 12, 2),
        ],
    )

    cur.execute(
        "INSERT INTO PC_CASE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (2, "Corsair FRAME 4000D RS", 500, 240, 600, "Steel", 4, 2, 400, 220, 200),
    )
    cur.executemany(
        "INSERT INTO CASE_RADIATOR_SPACE VALUES (?, ?, ?, ?, ?)",
        [
            (2, "FRONT", 50, 220, 360),
            (2, "TOP", 50, 220, 360),
            (2, "SIDE", 50, 220, 360),
            (2, "REAR", 50, 220, 140),
        ],
    )
    cur.executemany(
        "INSERT INTO CASE_IO_PORT VALUES (?, ?, ?, ?, ?)",
        [
            (2, "USB", "3.0", "", 2),
            (2, "USB-C", "3.0", "", 1),
        ],
    )
    cur.executemany(
        "INSERT INTO CASE_FORM_FACTOR_COMPATIBLE VALUES (?, ?)",
        [(2, "ATX"), (2, "Micro-ATX"), (2, "Mini-ITX")],
    )
    cur.executemany(
        "INSERT INTO CASE_FAN_SIZE_COMPATIBLE VALUES (?, ?)",
        [(2, 120), (2, 140)],
    )

    cur.execute(
        "INSERT INTO FAN VALUES (?, ?, ?, ?, ?)",
        (3, "RS120 ARGB PWM", 2100, 36.0, 120),
    )

    cur.execute(
        "INSERT INTO ETHERNET_CONTROLLER VALUES (?, ?)",
        (4, "Intel Ethernet Converged Network Adapter X550"),
    )

    cur.execute(
        "INSERT INTO MOTHERBOARD VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (5, "X870 GAMING WIFI6 AM5 LGA 1718", 4, "X870", 4, 1, 4, "ATX", "Socket AM5", "DDR5", 4),
    )
    cur.executemany(
        "INSERT INTO MOTHERBOARD_IO_PORTS VALUES (?, ?, ?, ?, ?)",
        [
            (5, "HDMI", "", "", 1),
            (5, "USB-C", "4.0", "", 2),
            (5, "USB", "3.2", "Gen 2", 1),
            (5, "USB", "3.2", "Gen 1", 3),
            (5, "USB", "2.0", "", 4),
            (5, "RJ", "45", "", 1),
            (5, "Audio jacks", "", "", 3),
        ],
    )
    cur.executemany(
        "INSERT INTO MOTHERBOARD_PCI_SLOT VALUES (?, ?, ?)",
        [(5, 0, 1), (5, 2, 2), (5, 4, 1), (5, 5, 1)],
    )

    cur.execute(
        "INSERT INTO CPU_COOLER VALUES (?, ?, ?)",
        (6, "Arctic Liquid Freezer III Pro 360", 39),
    )
    cur.execute(
        "INSERT INTO LIQUID_COOLER VALUES (?, ?, ?, ?, ?, ?, ?)",
        (6, 3, 360, 120, 38, 3000, 400),
    )

    cur.execute(
        "INSERT INTO STORAGE VALUES (?, ?, ?, ?, ?, ?)",
        (7, "Firecuda 520", 500, 5000, 2500, "M.2"),
    )
    cur.execute("INSERT INTO M2_STORAGE VALUES (?, ?)", (7, 5))

    cur.execute(
        "INSERT INTO GPU VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (8, "AMD Radeon RX 9060 XT", "RX 9000", "", 2530, 3130, 16, "GDDR6", 2048, 160, 0),
    )

    cur.execute(
        "INSERT INTO RAM VALUES (?, ?, ?, ?, ?)",
        (9, "Vengeance 2x32GB", 64, 6400, "DDR5"),
    )

    cur.execute(
        "INSERT INTO CPU VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (10, "Ryzen 9 9950x", "Ryzen", "9 9000", 170, 4300, 5700, 1280, 16, 64, 16, 32, "Zen-5", "Socket AM5", "DDR5"),
    )

    cur.execute("INSERT INTO WIFI_MODULE VALUES (?, ?, ?)", (11, "Realtek Wi-Fi 6", 4))

    cur.execute(
        "INSERT INTO MOTHERBOARD VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (12, "ROG STRIX B650-A", 4, "B650", 4, 1, 4, "ATX", "Socket AM5", "DDR5", None),
    )


def seed_database():
    create_tables()


# --------------------------------------------------------------------------------------
# lookup helpers
# --------------------------------------------------------------------------------------

def _ensure_exists(conn: sqlite3.Connection, table: str, column: str, value: Any):
    exists = _fetch_one(conn, f"SELECT 1 AS ok FROM {table} WHERE {column} = ?", (value,))
    if exists is None:
        raise ValueError(f"{table}.{column} value does not exist: {value}")


def _ensure_lookup(conn: sqlite3.Connection, table: str, column: str, value: Any):
    existing = _fetch_one(conn, f"SELECT 1 AS ok FROM {table} WHERE {column} = ?", (value,))
    if existing is None:
        conn.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))


def _ensure_pci_slot(conn: sqlite3.Connection, pci_version: str, pin_count: int) -> int:
    row = _fetch_one(
        conn,
        "SELECT pci_type_id FROM PCI_SLOT WHERE pci_version = ? AND pin_count = ?",
        (pci_version, pin_count),
    )
    if row:
        return int(row["pci_type_id"])

    new_id = _next_id(conn, "PCI_SLOT", "pci_type_id")
    conn.execute(
        "INSERT INTO PCI_SLOT (pci_type_id, pci_version, pin_count) VALUES (?, ?, ?)",
        (new_id, pci_version, pin_count),
    )
    return new_id


def _add_base_part(conn: sqlite3.Connection, manufacturer_id: int) -> tuple[int, int]:
    _ensure_exists(conn, "MANUFACTURER", "manufacturer_id", manufacturer_id)

    part_id = _next_id(conn, "COMPONENT", "part_id")
    list_part_id = _next_id(conn, "LIST_PART", "list_part_id")

    conn.execute("INSERT INTO LIST_PART (list_part_id) VALUES (?)", (list_part_id,))
    conn.execute(
        "INSERT INTO COMPONENT (part_id, manufacturer_id, list_part_id) VALUES (?, ?, ?)",
        (part_id, manufacturer_id, list_part_id),
    )
    return part_id, list_part_id


# --------------------------------------------------------------------------------------
# manufacturers
# --------------------------------------------------------------------------------------

def get_manufacturers():
    try:
        with get_connection() as conn:
            return _fetch_all(conn, "SELECT * FROM MANUFACTURER ORDER BY manufacturer_id")
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def add_manufacturer(name: str) -> bool:
    try:
        with get_connection() as conn:
            existing = _fetch_one(conn, "SELECT * FROM MANUFACTURER WHERE manufacturer_name = ?", (name,))
            if existing:
                return False

            new_id = _next_id(conn, "MANUFACTURER", "manufacturer_id")
            conn.execute(
                "INSERT INTO MANUFACTURER (manufacturer_id, manufacturer_name) VALUES (?, ?)",
                (new_id, name),
            )
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def delete_manufacturer(manufacturer_id: int) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM MANUFACTURER WHERE manufacturer_id = ?", (manufacturer_id,))
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def get_parts_of_manufacturer(manufacturer_id: int):
    try:
        with get_connection() as conn:
            query = """
                SELECT
                    c.part_id,
                    c.manufacturer_id,
                    c.list_part_id,
                    CASE
                        WHEN psu.list_part_id IS NOT NULL THEN 'psu'
                        WHEN pc.list_part_id IS NOT NULL THEN 'case'
                        WHEN fan.list_part_id IS NOT NULL THEN 'fan'
                        WHEN ec.list_part_id IS NOT NULL THEN 'ethernet_controller'
                        WHEN mb.list_part_id IS NOT NULL THEN 'motherboard'
                        WHEN ac.list_part_id IS NOT NULL THEN 'air_cooler'
                        WHEN lc.list_part_id IS NOT NULL THEN 'liquid_cooler'
                        WHEN m2.list_part_id IS NOT NULL THEN 'm2_storage'
                        WHEN hhd.list_part_id IS NOT NULL THEN 'hhd_storage'
                        WHEN sata.list_part_id IS NOT NULL THEN 'sata_storage'
                        WHEN gpu.list_part_id IS NOT NULL THEN 'gpu'
                        WHEN cpu.list_part_id IS NOT NULL THEN 'cpu'
                        WHEN ram.list_part_id IS NOT NULL THEN 'ram'
                        WHEN wifi.list_part_id IS NOT NULL THEN 'wifi_module'
                        ELSE 'unknown'
                    END AS part_type,
                    COALESCE(
                        psu.product_name,
                        pc.product_name,
                        fan.product_name,
                        ec.product_name,
                        mb.product_name,
                        cc.product_name,
                        st.product_name,
                        gpu.product_name,
                        cpu.product_name,
                        ram.product_name,
                        wifi.product_name
                    ) AS product_name
                FROM COMPONENT c
                LEFT JOIN POWER_SUPPLY_UNIT psu ON psu.list_part_id = c.list_part_id
                LEFT JOIN PC_CASE pc ON pc.list_part_id = c.list_part_id
                LEFT JOIN FAN fan ON fan.list_part_id = c.list_part_id
                LEFT JOIN ETHERNET_CONTROLLER ec ON ec.list_part_id = c.list_part_id
                LEFT JOIN MOTHERBOARD mb ON mb.list_part_id = c.list_part_id
                LEFT JOIN CPU_COOLER cc ON cc.list_part_id = c.list_part_id
                LEFT JOIN AIR_COOLER ac ON ac.list_part_id = c.list_part_id
                LEFT JOIN LIQUID_COOLER lc ON lc.list_part_id = c.list_part_id
                LEFT JOIN STORAGE st ON st.list_part_id = c.list_part_id
                LEFT JOIN M2_STORAGE m2 ON m2.list_part_id = c.list_part_id
                LEFT JOIN HHD_STORAGE hhd ON hhd.list_part_id = c.list_part_id
                LEFT JOIN SATA_STORAGE sata ON sata.list_part_id = c.list_part_id
                LEFT JOIN GPU gpu ON gpu.list_part_id = c.list_part_id
                LEFT JOIN CPU cpu ON cpu.list_part_id = c.list_part_id
                LEFT JOIN RAM ram ON ram.list_part_id = c.list_part_id
                LEFT JOIN WIFI_MODULE wifi ON wifi.list_part_id = c.list_part_id
                WHERE c.manufacturer_id = ?
                ORDER BY c.list_part_id
            """
            return _fetch_all(conn, query, (manufacturer_id,))
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


# --------------------------------------------------------------------------------------
# suppliers / store items
# --------------------------------------------------------------------------------------

def get_suppliers():
    try:
        with get_connection() as conn:
            return _fetch_all(conn, "SELECT * FROM SUPPLIER ORDER BY supplier_id")
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def add_supplier(name: str) -> bool:
    try:
        with get_connection() as conn:
            existing = _fetch_one(conn, "SELECT * FROM SUPPLIER WHERE supplier_name = ?", (name,))
            if existing:
                return False

            new_id = _next_id(conn, "SUPPLIER", "supplier_id")
            conn.execute(
                "INSERT INTO SUPPLIER (supplier_id, supplier_name) VALUES (?, ?)",
                (new_id, name),
            )
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def delete_supplier(supplier_id: int) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM SUPPLIER WHERE supplier_id = ?", (supplier_id,))
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def get_suppliers_of_part(list_part_id: int):
    try:
        with get_connection() as conn:
            query = """
                SELECT si.item_number, si.supplier_id, s.supplier_name, si.price, si.list_part_id
                FROM STORE_ITEM si
                INNER JOIN SUPPLIER s ON s.supplier_id = si.supplier_id
                WHERE si.list_part_id = ?
                ORDER BY si.price ASC
            """
            return _fetch_all(conn, query, (list_part_id,))
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def get_parts_sold_by_supplier(supplier_id: int):
    try:
        with get_connection() as conn:
            query = """
                SELECT
                    si.item_number,
                    si.supplier_id,
                    si.price,
                    si.list_part_id,
                    CASE
                        WHEN psu.list_part_id IS NOT NULL THEN 'psu'
                        WHEN pc.list_part_id IS NOT NULL THEN 'case'
                        WHEN fan.list_part_id IS NOT NULL THEN 'fan'
                        WHEN ec.list_part_id IS NOT NULL THEN 'ethernet_controller'
                        WHEN mb.list_part_id IS NOT NULL THEN 'motherboard'
                        WHEN ac.list_part_id IS NOT NULL THEN 'air_cooler'
                        WHEN lc.list_part_id IS NOT NULL THEN 'liquid_cooler'
                        WHEN m2.list_part_id IS NOT NULL THEN 'm2_storage'
                        WHEN hhd.list_part_id IS NOT NULL THEN 'hhd_storage'
                        WHEN sata.list_part_id IS NOT NULL THEN 'sata_storage'
                        WHEN gpu.list_part_id IS NOT NULL THEN 'gpu'
                        WHEN cpu.list_part_id IS NOT NULL THEN 'cpu'
                        WHEN ram.list_part_id IS NOT NULL THEN 'ram'
                        WHEN wifi.list_part_id IS NOT NULL THEN 'wifi_module'
                        ELSE 'unknown'
                    END AS part_type,
                    COALESCE(
                        psu.product_name,
                        pc.product_name,
                        fan.product_name,
                        ec.product_name,
                        mb.product_name,
                        cc.product_name,
                        st.product_name,
                        gpu.product_name,
                        cpu.product_name,
                        ram.product_name,
                        wifi.product_name
                    ) AS product_name
                FROM STORE_ITEM si
                LEFT JOIN POWER_SUPPLY_UNIT psu ON psu.list_part_id = si.list_part_id
                LEFT JOIN PC_CASE pc ON pc.list_part_id = si.list_part_id
                LEFT JOIN FAN fan ON fan.list_part_id = si.list_part_id
                LEFT JOIN ETHERNET_CONTROLLER ec ON ec.list_part_id = si.list_part_id
                LEFT JOIN MOTHERBOARD mb ON mb.list_part_id = si.list_part_id
                LEFT JOIN CPU_COOLER cc ON cc.list_part_id = si.list_part_id
                LEFT JOIN AIR_COOLER ac ON ac.list_part_id = si.list_part_id
                LEFT JOIN LIQUID_COOLER lc ON lc.list_part_id = si.list_part_id
                LEFT JOIN STORAGE st ON st.list_part_id = si.list_part_id
                LEFT JOIN M2_STORAGE m2 ON m2.list_part_id = si.list_part_id
                LEFT JOIN HHD_STORAGE hhd ON hhd.list_part_id = si.list_part_id
                LEFT JOIN SATA_STORAGE sata ON sata.list_part_id = si.list_part_id
                LEFT JOIN GPU gpu ON gpu.list_part_id = si.list_part_id
                LEFT JOIN CPU cpu ON cpu.list_part_id = si.list_part_id
                LEFT JOIN RAM ram ON ram.list_part_id = si.list_part_id
                LEFT JOIN WIFI_MODULE wifi ON wifi.list_part_id = si.list_part_id
                WHERE si.supplier_id = ?
                ORDER BY si.list_part_id
            """
            return _fetch_all(conn, query, (supplier_id,))
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def add_store_item(list_part_id: int, supplier_id: int, price: float) -> bool:
    try:
        with get_connection() as conn:
            _ensure_exists(conn, "LIST_PART", "list_part_id", list_part_id)
            _ensure_exists(conn, "SUPPLIER", "supplier_id", supplier_id)

            existing = _fetch_one(
                conn,
                "SELECT item_number FROM STORE_ITEM WHERE supplier_id = ? AND list_part_id = ?",
                (supplier_id, list_part_id),
            )
            if existing:
                return False

            new_id = _next_id(conn, "STORE_ITEM", "item_number")
            conn.execute(
                "INSERT INTO STORE_ITEM (item_number, supplier_id, price, list_part_id) VALUES (?, ?, ?, ?)",
                (new_id, supplier_id, price, list_part_id),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def delete_store_item(item_number: int) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM STORE_ITEM WHERE item_number = ?", (item_number,))
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


# --------------------------------------------------------------------------------------
# customers / build lists
# --------------------------------------------------------------------------------------

def get_customers():
    try:
        with get_connection() as conn:
            return _fetch_all(conn, "SELECT * FROM CUSTOMER ORDER BY customer_id")
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def add_customer(
    first_name: str,
    middle_name: Optional[str],
    last_name: Optional[str],
    postal_code: str,
    street_no: str,
    city: str,
    province: str,
    country: str,
) -> bool:
    try:
        with get_connection() as conn:
            existing = _fetch_one(
                conn,
                "SELECT customer_id FROM CUSTOMER WHERE first_name = ? AND IFNULL(last_name, '') = IFNULL(?, '')",
                (first_name, last_name),
            )
            if existing:
                return False

            new_id = _next_id(conn, "CUSTOMER", "customer_id")
            conn.execute(
                """
                INSERT INTO CUSTOMER
                (customer_id, first_name, middle_name, last_name, postal_code, street_no, city, province, country)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (new_id, first_name, middle_name, last_name, postal_code, street_no, city, province, country),
            )
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def delete_customer(customer_id: int) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM CUSTOMER WHERE customer_id = ?", (customer_id,))
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def create_build_list(customer_id: int) -> bool:
    try:
        with get_connection() as conn:
            _ensure_exists(conn, "CUSTOMER", "customer_id", customer_id)
            new_id = _next_id(conn, "BUILD_LIST", "list_number")
            conn.execute("INSERT INTO BUILD_LIST (list_number, customer_id) VALUES (?, ?)", (new_id, customer_id))
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def delete_build_list(list_id: int) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM BUILD_LIST WHERE list_number = ?", (list_id,))
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def add_to_build_list(list_id: int, list_part_id: int, num_comps: int) -> bool:
    try:
        with get_connection() as conn:
            _ensure_exists(conn, "BUILD_LIST", "list_number", list_id)
            _ensure_exists(conn, "LIST_PART", "list_part_id", list_part_id)

            existing = _fetch_one(
                conn,
                "SELECT * FROM CONTAINS_COMPONENT WHERE list_number = ? AND list_part_id = ?",
                (list_id, list_part_id),
            )
            if existing:
                return False

            conn.execute(
                "INSERT INTO CONTAINS_COMPONENT (list_number, list_part_id, num_components) VALUES (?, ?, ?)",
                (list_id, list_part_id, num_comps),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def delete_part_in_build_list(list_id: int, list_part_id: int) -> bool:
    try:
        with get_connection() as conn:
            conn.execute(
                "DELETE FROM CONTAINS_COMPONENT WHERE list_number = ? AND list_part_id = ?",
                (list_id, list_part_id),
            )
            return True
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def get_parts_in_build_list(build_list_id: int):
    try:
        with get_connection() as conn:
            query = """
                SELECT
                    bl.list_number,
                    bl.customer_id,
                    cc.list_part_id,
                    cc.num_components,
                    CASE
                        WHEN psu.list_part_id IS NOT NULL THEN 'psu'
                        WHEN pc.list_part_id IS NOT NULL THEN 'case'
                        WHEN fan.list_part_id IS NOT NULL THEN 'fan'
                        WHEN ec.list_part_id IS NOT NULL THEN 'ethernet_controller'
                        WHEN mb.list_part_id IS NOT NULL THEN 'motherboard'
                        WHEN ac.list_part_id IS NOT NULL THEN 'air_cooler'
                        WHEN lc.list_part_id IS NOT NULL THEN 'liquid_cooler'
                        WHEN m2.list_part_id IS NOT NULL THEN 'm2_storage'
                        WHEN hhd.list_part_id IS NOT NULL THEN 'hhd_storage'
                        WHEN sata.list_part_id IS NOT NULL THEN 'sata_storage'
                        WHEN gpu.list_part_id IS NOT NULL THEN 'gpu'
                        WHEN cpu.list_part_id IS NOT NULL THEN 'cpu'
                        WHEN ram.list_part_id IS NOT NULL THEN 'ram'
                        WHEN wifi.list_part_id IS NOT NULL THEN 'wifi_module'
                        ELSE 'unknown'
                    END AS part_type,
                    COALESCE(
                        psu.product_name,
                        pc.product_name,
                        fan.product_name,
                        ec.product_name,
                        mb.product_name,
                        cc2.product_name,
                        st.product_name,
                        gpu.product_name,
                        cpu.product_name,
                        ram.product_name,
                        wifi.product_name
                    ) AS product_name
                FROM BUILD_LIST bl
                INNER JOIN CONTAINS_COMPONENT cc ON cc.list_number = bl.list_number
                LEFT JOIN POWER_SUPPLY_UNIT psu ON psu.list_part_id = cc.list_part_id
                LEFT JOIN PC_CASE pc ON pc.list_part_id = cc.list_part_id
                LEFT JOIN FAN fan ON fan.list_part_id = cc.list_part_id
                LEFT JOIN ETHERNET_CONTROLLER ec ON ec.list_part_id = cc.list_part_id
                LEFT JOIN MOTHERBOARD mb ON mb.list_part_id = cc.list_part_id
                LEFT JOIN CPU_COOLER cc2 ON cc2.list_part_id = cc.list_part_id
                LEFT JOIN AIR_COOLER ac ON ac.list_part_id = cc.list_part_id
                LEFT JOIN LIQUID_COOLER lc ON lc.list_part_id = cc.list_part_id
                LEFT JOIN STORAGE st ON st.list_part_id = cc.list_part_id
                LEFT JOIN M2_STORAGE m2 ON m2.list_part_id = cc.list_part_id
                LEFT JOIN HHD_STORAGE hhd ON hhd.list_part_id = cc.list_part_id
                LEFT JOIN SATA_STORAGE sata ON sata.list_part_id = cc.list_part_id
                LEFT JOIN GPU gpu ON gpu.list_part_id = cc.list_part_id
                LEFT JOIN CPU cpu ON cpu.list_part_id = cc.list_part_id
                LEFT JOIN RAM ram ON ram.list_part_id = cc.list_part_id
                LEFT JOIN WIFI_MODULE wifi ON wifi.list_part_id = cc.list_part_id
                WHERE bl.list_number = ?
                ORDER BY cc.list_part_id
            """
            return _fetch_all(conn, query, (build_list_id,))
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def display_all_build_lists():
    try:
        with get_connection() as conn:
            query = """
                SELECT
                    cu.customer_id,
                    cu.first_name,
                    cu.last_name,
                    bl.list_number,
                    cc.list_part_id,
                    cc.num_components
                FROM CUSTOMER cu
                INNER JOIN BUILD_LIST bl ON bl.customer_id = cu.customer_id
                LEFT JOIN CONTAINS_COMPONENT cc ON cc.list_number = bl.list_number
                ORDER BY cu.customer_id, bl.list_number, cc.list_part_id
            """
            return _fetch_all(conn, query)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


# --------------------------------------------------------------------------------------
# add part helpers
# --------------------------------------------------------------------------------------

def add_part_psu(
    manufacturer_id: int,
    product_name: str,
    power_rating: int,
    modular: bool,
    length_mm: int,
    connectors: list[tuple[str, int, int]],
) -> bool:
    try:
        with get_connection() as conn:
            _, list_part_id = _add_base_part(conn, manufacturer_id)

            conn.execute(
                """
                INSERT INTO POWER_SUPPLY_UNIT
                (list_part_id, product_name, power_rating, modular, length_mm)
                VALUES (?, ?, ?, ?, ?)
                """,
                (list_part_id, product_name, power_rating, int(modular), length_mm),
            )

            for conn_type, num_pins, count in connectors:
                conn.execute(
                    """
                    INSERT INTO POWER_SUPPLY_CONNECTORS
                    (list_part_id, conn_type, num_pins, count)
                    VALUES (?, ?, ?, ?)
                    """,
                    (list_part_id, conn_type, num_pins, count),
                )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_case(
    manufacturer_id: int,
    product_name: str,
    height: int,
    width: int,
    len_case: int,
    material: str,
    num_35_bays: int,
    num_25_bays: int,
    max_gpu_length_mm: int,
    max_psu_length_mm: int,
    max_air_cooler_height: int,
    radiator_spaces: list[tuple[str, int, int, int]],
    io_ports: list[tuple[str, str, str, int]],
    fans: list[int],
    compatible_form_factors: list[str] | None = None,
) -> bool:
    try:
        with get_connection() as conn:
            _, list_part_id = _add_base_part(conn, manufacturer_id)

            conn.execute(
                """
                INSERT INTO PC_CASE
                (list_part_id, product_name, height, width, len_case, material, num_35_bays, num_25_bays,
                 max_gpu_len_mm, max_psu_len_mm, max_air_cooler_height)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    list_part_id, product_name, height, width, len_case, material,
                    num_35_bays, num_25_bays, max_gpu_length_mm, max_psu_length_mm,
                    max_air_cooler_height
                ),
            )

            for loc_in_case, rad_height, rad_width, len_rad in radiator_spaces:
                conn.execute(
                    """
                    INSERT INTO CASE_RADIATOR_SPACE
                    (list_part_id, loc_in_case, height, width, len_rad)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (list_part_id, loc_in_case, rad_height, rad_width, len_rad),
                )

            for con_version, generation, con_type, count in io_ports:
                conn.execute(
                    """
                    INSERT INTO CASE_IO_PORT
                    (list_part_id, con_version, generation, con_type, count)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (list_part_id, con_version, generation, con_type, count),
                )

            for size_mm in fans:
                _ensure_lookup(conn, "FAN_SIZE", "size_category_mm", size_mm)
                conn.execute(
                    "INSERT INTO CASE_FAN_SIZE_COMPATIBLE (case_id, size_category_mm) VALUES (?, ?)",
                    (list_part_id, size_mm),
                )

            for ff in compatible_form_factors or []:
                _ensure_lookup(conn, "MOTHERBOARD_FORM_FACTOR", "form_factor", ff)
                conn.execute(
                    "INSERT INTO CASE_FORM_FACTOR_COMPATIBLE (case_id, form_factor) VALUES (?, ?)",
                    (list_part_id, ff),
                )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_fan(manufacturer_id: int, product_name: str, fan_rpm: int, noise_level: float, size_category_mm: int) -> bool:
    try:
        with get_connection() as conn:
            _ensure_lookup(conn, "FAN_SIZE", "size_category_mm", size_category_mm)
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                """
                INSERT INTO FAN (list_part_id, product_name, fan_rpm, noise_level, size_category_mm)
                VALUES (?, ?, ?, ?, ?)
                """,
                (list_part_id, product_name, fan_rpm, noise_level, size_category_mm),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_ethernetcontroller(manufacturer_id: int, product_name: str) -> bool:
    try:
        with get_connection() as conn:
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                "INSERT INTO ETHERNET_CONTROLLER (list_part_id, product_name) VALUES (?, ?)",
                (list_part_id, product_name),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_motherboard(
    manufacturer_id: int,
    product_name: str,
    num_ram_slots: int,
    chipset_name: str,
    num_sata_conn: int,
    num_cooler_headers: int,
    num_fan_headers: int,
    form_factor: str,
    socket_type: str,
    ram_type: str,
    ethernet_con_id: Optional[int],
    io_ports: list[tuple[str, str, str, int]],
    pci_slots: list[tuple[str, int, int]],
) -> bool:
    try:
        with get_connection() as conn:
            _ensure_lookup(conn, "MOTHERBOARD_FORM_FACTOR", "form_factor", form_factor)
            _ensure_lookup(conn, "CPU_SOCKET_TYPE", "socket_type", socket_type)
            _ensure_lookup(conn, "RAM_TYPE", "ram_type", ram_type)
            if ethernet_con_id is not None:
                _ensure_exists(conn, "ETHERNET_CONTROLLER", "list_part_id", ethernet_con_id)

            _, list_part_id = _add_base_part(conn, manufacturer_id)

            conn.execute(
                """
                INSERT INTO MOTHERBOARD
                (list_part_id, product_name, num_ram_slots, chipset_name, num_sata_connectors,
                 num_cooler_headers, num_fan_headers, form_factor, socket_type, ram_type, ethernet_con_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    list_part_id, product_name, num_ram_slots, chipset_name, num_sata_conn,
                    num_cooler_headers, num_fan_headers, form_factor, socket_type, ram_type, ethernet_con_id
                ),
            )

            for con_version, generation, con_type, count in io_ports:
                conn.execute(
                    """
                    INSERT INTO MOTHERBOARD_IO_PORTS
                    (list_part_id, con_version, generation, con_type, count)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (list_part_id, con_version, generation, con_type, count),
                )

            for pci_version, pin_count, num_slots in pci_slots:
                pci_type_id = _ensure_pci_slot(conn, pci_version, pin_count)
                conn.execute(
                    """
                    INSERT INTO MOTHERBOARD_PCI_SLOT (list_part_id, pci_type_id, num_slots)
                    VALUES (?, ?, ?)
                    """,
                    (list_part_id, pci_type_id, num_slots),
                )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_air_cooler(manufacturer_id: int, product_name: str, noise_level: int, fan_rpm: int, height: int) -> bool:
    try:
        with get_connection() as conn:
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                "INSERT INTO CPU_COOLER (list_part_id, product_name, noise_level) VALUES (?, ?, ?)",
                (list_part_id, product_name, noise_level),
            )
            conn.execute(
                "INSERT INTO AIR_COOLER (list_part_id, fan_rpm, height) VALUES (?, ?, ?)",
                (list_part_id, fan_rpm, height),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_liquid_cooler(
    manufacturer_id: int,
    product_name: str,
    noise_level: int,
    num_fans: int,
    len_cool: int,
    width: int,
    height: int,
    fan_rpm: int,
    cooling_tube_length: int,
) -> bool:
    try:
        with get_connection() as conn:
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                "INSERT INTO CPU_COOLER (list_part_id, product_name, noise_level) VALUES (?, ?, ?)",
                (list_part_id, product_name, noise_level),
            )
            conn.execute(
                """
                INSERT INTO LIQUID_COOLER
                (list_part_id, num_fans, len_cool, width, height, fan_rpm, cooling_tube_length)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (list_part_id, num_fans, len_cool, width, height, fan_rpm, cooling_tube_length),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_m2storage(
    manufacturer_id: int,
    product_name: str,
    capacity: int,
    read_speed: int,
    write_speed: int,
    form_factor: str,
    pci_version: str,
    pin_count: int = 4,
) -> bool:
    try:
        with get_connection() as conn:
            pci_type_id = _ensure_pci_slot(conn, pci_version, pin_count)
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                """
                INSERT INTO STORAGE
                (list_part_id, product_name, capacity, read_speed, write_speed, form_factor)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (list_part_id, product_name, capacity, read_speed, write_speed, form_factor),
            )
            conn.execute(
                "INSERT INTO M2_STORAGE (list_part_id, pci_type_id) VALUES (?, ?)",
                (list_part_id, pci_type_id),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_hhdstorage(
    manufacturer_id: int,
    product_name: str,
    capacity: int,
    read_speed: int,
    write_speed: int,
    form_factor: str,
    interface: str,
) -> bool:
    try:
        with get_connection() as conn:
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                """
                INSERT INTO STORAGE
                (list_part_id, product_name, capacity, read_speed, write_speed, form_factor)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (list_part_id, product_name, capacity, read_speed, write_speed, form_factor),
            )
            conn.execute(
                "INSERT INTO HHD_STORAGE (list_part_id, interface) VALUES (?, ?)",
                (list_part_id, interface),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_satastorage(
    manufacturer_id: int,
    product_name: str,
    capacity: int,
    read_speed: int,
    write_speed: int,
    form_factor: str,
    interface: str,
) -> bool:
    try:
        with get_connection() as conn:
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                """
                INSERT INTO STORAGE
                (list_part_id, product_name, capacity, read_speed, write_speed, form_factor)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (list_part_id, product_name, capacity, read_speed, write_speed, form_factor),
            )
            conn.execute(
                "INSERT INTO SATA_STORAGE (list_part_id, interface) VALUES (?, ?)",
                (list_part_id, interface),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_gpu(
    manufacturer_id: int,
    product_name: str,
    series: str,
    architecture: str,
    base_clock: int,
    boost_clock: int,
    memory_size: int,
    memory_type: str,
    num_cores: int,
    power_cons: int,
    pci_version: str,
    pin_count: int = 16,
) -> bool:
    try:
        with get_connection() as conn:
            pci_type_id = _ensure_pci_slot(conn, pci_version, pin_count)
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                """
                INSERT INTO GPU
                (list_part_id, product_name, series, architecture, base_clock, boost_clock,
                 memory_size, memory_type, num_cores, power_consumption, pci_type_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    list_part_id, product_name, series, architecture, base_clock, boost_clock,
                    memory_size, memory_type, num_cores, power_cons, pci_type_id
                ),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_ram(manufacturer_id: int, product_name: str, capacity: int, max_freq: int, ram_ddr_type: str) -> bool:
    try:
        with get_connection() as conn:
            _ensure_lookup(conn, "RAM_TYPE", "ram_type", ram_ddr_type)
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                """
                INSERT INTO RAM (list_part_id, product_name, capacity, max_freq, ram_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (list_part_id, product_name, capacity, max_freq, ram_ddr_type),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_cpu(
    manufacturer_id: int,
    product_name: str,
    chip_family: str,
    series: str,
    tdp: int,
    base_clock: int,
    boost_clock: int,
    l1_cache: int,
    l2_cache: int,
    l3_cache: int,
    num_cores: int,
    num_threads: int,
    architecture: str,
    socket_type: str,
    ram_ddr_type: str,
) -> bool:
    try:
        with get_connection() as conn:
            _ensure_lookup(conn, "CPU_SOCKET_TYPE", "socket_type", socket_type)
            _ensure_lookup(conn, "RAM_TYPE", "ram_type", ram_ddr_type)
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                """
                INSERT INTO CPU
                (list_part_id, product_name, chip_family, series, tdp, base_clock, boost_clock,
                 l1_cache, l2_cache, l3_cache, num_cores, num_threads, architecture, socket_type, ram_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    list_part_id, product_name, chip_family, series, tdp, base_clock, boost_clock,
                    l1_cache, l2_cache, l3_cache, num_cores, num_threads, architecture,
                    socket_type, ram_ddr_type
                ),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


def add_part_wifimodule(manufacturer_id: int, product_name: str, pci_version: str, pin_count: int) -> bool:
    try:
        with get_connection() as conn:
            pci_type_id = _ensure_pci_slot(conn, pci_version, pin_count)
            _, list_part_id = _add_base_part(conn, manufacturer_id)
            conn.execute(
                "INSERT INTO WIFI_MODULE (list_part_id, product_name, pci_type_id) VALUES (?, ?, ?)",
                (list_part_id, product_name, pci_type_id),
            )
            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


# --------------------------------------------------------------------------------------
# listing / compatibility placeholders
# --------------------------------------------------------------------------------------

def list_all_parts_of_type(part_type: str):
    part_type = part_type.lower().strip()
    queries = {
        "psu": "SELECT list_part_id, product_name, power_rating, modular, length_mm FROM POWER_SUPPLY_UNIT ORDER BY list_part_id",
        "case": "SELECT list_part_id, product_name, height, width, len_case FROM PC_CASE ORDER BY list_part_id",
        "fan": "SELECT list_part_id, product_name, fan_rpm, noise_level, size_category_mm FROM FAN ORDER BY list_part_id",
        "ethernet_controller": "SELECT list_part_id, product_name FROM ETHERNET_CONTROLLER ORDER BY list_part_id",
        "motherboard": "SELECT list_part_id, product_name, form_factor, socket_type, ram_type FROM MOTHERBOARD ORDER BY list_part_id",
        "air_cooler": """
            SELECT ac.list_part_id, cc.product_name, cc.noise_level, ac.fan_rpm, ac.height
            FROM AIR_COOLER ac
            INNER JOIN CPU_COOLER cc ON cc.list_part_id = ac.list_part_id
            ORDER BY ac.list_part_id
        """,
        "liquid_cooler": """
            SELECT lc.list_part_id, cc.product_name, cc.noise_level, lc.num_fans, lc.len_cool, lc.width, lc.height
            FROM LIQUID_COOLER lc
            INNER JOIN CPU_COOLER cc ON cc.list_part_id = lc.list_part_id
            ORDER BY lc.list_part_id
        """,
        "m2_storage": """
            SELECT m2.list_part_id, st.product_name, st.capacity, st.read_speed, st.write_speed, st.form_factor
            FROM M2_STORAGE m2
            INNER JOIN STORAGE st ON st.list_part_id = m2.list_part_id
            ORDER BY m2.list_part_id
        """,
        "hhd_storage": """
            SELECT h.list_part_id, st.product_name, st.capacity, st.read_speed, st.write_speed, st.form_factor, h.interface
            FROM HHD_STORAGE h
            INNER JOIN STORAGE st ON st.list_part_id = h.list_part_id
            ORDER BY h.list_part_id
        """,
        "sata_storage": """
            SELECT s.list_part_id, st.product_name, st.capacity, st.read_speed, st.write_speed, st.form_factor, s.interface
            FROM SATA_STORAGE s
            INNER JOIN STORAGE st ON st.list_part_id = s.list_part_id
            ORDER BY s.list_part_id
        """,
        "gpu": "SELECT list_part_id, product_name, series, memory_size, memory_type, power_consumption FROM GPU ORDER BY list_part_id",
        "cpu": "SELECT list_part_id, product_name, chip_family, series, socket_type, ram_type FROM CPU ORDER BY list_part_id",
        "ram": "SELECT list_part_id, product_name, capacity, max_freq, ram_type FROM RAM ORDER BY list_part_id",
        "wifi_module": "SELECT list_part_id, product_name, pci_type_id FROM WIFI_MODULE ORDER BY list_part_id",
    }

    if part_type not in queries:
        return False

    try:
        with get_connection() as conn:
            return _fetch_all(conn, queries[part_type])
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False


def get_compatible_part(build_list: int, customer_id: int, part_type: str):
    """
    Basic compatibility implementation for a few common cases.
    For anything else, returns all parts of that type.
    """
    try:
        with get_connection() as conn:
            _ensure_exists(conn, "BUILD_LIST", "list_number", build_list)
            _ensure_exists(conn, "CUSTOMER", "customer_id", customer_id)

            # build must belong to customer
            row = _fetch_one(
                conn,
                "SELECT 1 AS ok FROM BUILD_LIST WHERE list_number = ? AND customer_id = ?",
                (build_list, customer_id),
            )
            if row is None:
                return False

            part_type = part_type.lower().strip()

            cpu = _fetch_one(
                conn,
                """
                SELECT cpu.socket_type, cpu.ram_type
                FROM CONTAINS_COMPONENT cc
                INNER JOIN CPU cpu ON cpu.list_part_id = cc.list_part_id
                WHERE cc.list_number = ?
                LIMIT 1
                """,
                (build_list,),
            )

            motherboard = _fetch_one(
                conn,
                """
                SELECT mb.form_factor, mb.socket_type, mb.ram_type
                FROM CONTAINS_COMPONENT cc
                INNER JOIN MOTHERBOARD mb ON mb.list_part_id = cc.list_part_id
                WHERE cc.list_number = ?
                LIMIT 1
                """,
                (build_list,),
            )

            pc_case = _fetch_one(
                conn,
                """
                SELECT pc.list_part_id, pc.max_gpu_len_mm, pc.max_psu_len_mm, pc.max_air_cooler_height
                FROM CONTAINS_COMPONENT cc
                INNER JOIN PC_CASE pc ON pc.list_part_id = cc.list_part_id
                WHERE cc.list_number = ?
                LIMIT 1
                """,
                (build_list,),
            )

            if part_type == "motherboard" and cpu:
                return _fetch_all(
                    conn,
                    """
                    SELECT list_part_id, product_name, form_factor, socket_type, ram_type
                    FROM MOTHERBOARD
                    WHERE socket_type = ? AND ram_type = ?
                    ORDER BY list_part_id
                    """,
                    (cpu["socket_type"], cpu["ram_type"]),
                )

            if part_type == "cpu" and motherboard:
                return _fetch_all(
                    conn,
                    """
                    SELECT list_part_id, product_name, socket_type, ram_type
                    FROM CPU
                    WHERE socket_type = ? AND ram_type = ?
                    ORDER BY list_part_id
                    """,
                    (motherboard["socket_type"], motherboard["ram_type"]),
                )

            if part_type == "ram" and motherboard:
                return _fetch_all(
                    conn,
                    """
                    SELECT list_part_id, product_name, capacity, max_freq, ram_type
                    FROM RAM
                    WHERE ram_type = ?
                    ORDER BY list_part_id
                    """,
                    (motherboard["ram_type"],),
                )

            if part_type == "case" and motherboard:
                return _fetch_all(
                    conn,
                    """
                    SELECT pc.list_part_id, pc.product_name, pc.max_gpu_len_mm, pc.max_psu_len_mm, pc.max_air_cooler_height
                    FROM PC_CASE pc
                    INNER JOIN CASE_FORM_FACTOR_COMPATIBLE cffc
                        ON cffc.case_id = pc.list_part_id
                    WHERE cffc.form_factor = ?
                    ORDER BY pc.list_part_id
                    """,
                    (motherboard["form_factor"],),
                )

            if part_type == "gpu" and pc_case:
                return _fetch_all(
                    conn,
                    """
                    SELECT list_part_id, product_name, series, memory_size, power_consumption
                    FROM GPU
                    ORDER BY list_part_id
                    """
                )

            return list_all_parts_of_type(part_type)
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False


# --------------------------------------------------------------------------------------
# delete part
# --------------------------------------------------------------------------------------

def delete_part(list_part_id: int) -> bool:
    try:
        with get_connection() as conn:
            _ensure_exists(conn, "LIST_PART", "list_part_id", list_part_id)

            # Because not every relation cascades all the way through multiple subtype layers,
            # explicit deletes keep this robust.
            for table in DELETE_ORDER:
                conn.execute(f"DELETE FROM {table} WHERE list_part_id = ?", (list_part_id,))

            return True
    except (sqlite3.Error, ValueError) as e:
        print(f"query error: {e}")
        return False