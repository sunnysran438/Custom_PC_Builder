import sqlite3

#########################################################################################
# Backend file for handeling the database
#########################################################################################


## SETUP THE DATABASE ###################################################################
def create_tables():
    """sets up the tables, Note: this will delete any existing tables"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()

    # setup the tables
    cursor.executescript("""
                         
PRAGMA foreign_keys=off;
-- Remove tables if they already exist
-- compatibility relations ##########################################################
DROP TABLE IF EXISTS CASE_FORM_FACTOR_COMPATIBLE;
DROP TABLE IF EXISTS CASE_FAN_SIZE_COMPATIBLE;

-- Components #########################################################
-- network group

DROP TABLE IF EXISTS WIFI_MODULE;

-- cpu 
DROP TABLE IF EXISTS CPU;
-- ram 
DROP TABLE IF EXISTS RAM;
-- gpu
DROP TABLE IF EXISTS GPU;
-- storage group
DROP TABLE IF EXISTS SATA_STORAGE;
DROP TABLE IF EXISTS HHD_STORAGE;
DROP TABLE IF EXISTS M2_STORAGE;
DROP TABLE IF EXISTS STORAGE;
-- cooler group
DROP TABLE IF EXISTS LIQUID_COOLER;
DROP TABLE IF EXISTS AIR_COOLER;
DROP TABLE IF EXISTS CPU_COOLER;

-- motherboard group
DROP TABLE IF EXISTS MOTHERBOARD_PCI_SLOT;
DROP TABLE IF EXISTS MOTHERBOARD_IO_PORTS;
DROP TABLE IF EXISTS MOTHERBOARD;
DROP TABLE IF EXISTS ETHERNET_CONTROLLER;

-- fan
DROP TABLE IF EXISTS FAN;
-- case group
DROP TABLE IF EXISTS CASE_IO_PORT;
DROP TABLE IF EXISTS CASE_IO_PORTS;
DROP TABLE IF EXISTS CASE_RADIATOR_SPACE;
DROP TABLE IF EXISTS PC_CASE;

-- power supply group
DROP TABLE IF EXISTS POWER_SUPPLY_CONNECTORS;
DROP TABLE IF EXISTS POWER_SUPPLY_UNIT;

-- Component Formats #################################################
DROP TABLE IF EXISTS MOTHERBOARD_FORM_FACTOR;
DROP TABLE IF EXISTS PCI_SLOT;
DROP TABLE IF EXISTS RAM_TYPE;
DROP TABLE IF EXISTS CPU_SOCKET_TYPE;
DROP TABLE IF EXISTS FAN_SIZE;

-- Users ############################################################
-- customer build list stuf
DROP TABLE IF EXISTS CONTAINS_COMPONENT;
DROP TABLE IF EXISTS BUILD_LIST;

-- Base classes
DROP TABLE IF EXISTS COMPONENT;
DROP TABLE IF EXISTS STORE_ITEM;
DROP TABLE IF EXISTS LIST_PART;
-- suppliers
DROP TABLE IF EXISTS SUPPLIER;
DROP TABLE IF EXISTS MANUFACTURER;
DROP TABLE IF EXISTS CUSTOMER;

-- CREATE TABLES ###################################################################
-- #################################################################################

-- User tables #####################################################################
CREATE TABLE CUSTOMER(
    customer_id INTEGER NOT NULL,
    first_name VARCHAR(63) NOT NULL,
    middle_name VARCHAR(63),
    last_name VARCHAR(63),
    postal_code VARCHAR(63) NOT NULL,
    street_no VARCHAR(63) NOT NULL,
    city VARCHAR(63) NOT NULL,
    province VARCHAR(63) NOT NULL,
    country VARCHAR(63) NOT NULL,
    PRIMARY KEY(customer_id)
);

CREATE TABLE MANUFACTURER(
    manufacturer_id INTEGER NOT NULL,
    manufacturer_name VARCHAR(63) NOT NULL,
    PRIMARY KEY(manufacturer_id)
);

CREATE TABLE SUPPLIER(
    supplier_id INTEGER NOT NULL,
    supplier_name VARCHAR(63) NOT NULL,
    PRIMARY KEY(supplier_id)
);

-- Base classes ####################################################################
CREATE TABLE LIST_PART(
    list_part_id INTEGER NOT NULL,
    PRIMARY KEY(list_part_id)
);

CREATE TABLE STORE_ITEM(
    item_number INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    price FLOAT(24) NOT NULL,
    list_part_id INTEGER NOT NULL,
    PRIMARY KEY(item_number),
    FOREIGN KEY(supplier_id) REFERENCES SUPPLIER(supplier_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id)
);

CREATE TABLE COMPONENT(
    part_id INTEGER NOT NULL,
    manufacturer_id INTEGER NOT NULL,
    list_part_id INTEGER NOT NULL,
    PRIMARY KEY(part_id),
    FOREIGN KEY(manufacturer_id) REFERENCES MANUFACTURER(manufacturer_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id)
);

-- customer build list stuf ########################################################

CREATE TABLE BUILD_LIST(
    list_number INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    CONSTRAINT pk PRIMARY KEY(list_number),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
);

CREATE TABLE CONTAINS_COMPONENT(
    list_number INTEGER NOT NULL,
    list_part_id INTEGER NOT NULL,
    num_components INTEGER NOT NULL,
    CONSTRAINT pk PRIMARY KEY(list_number, list_part_id),
    FOREIGN KEY (list_number) REFERENCES BUILD_LIST(list_number),
    FOREIGN KEY (list_part_id) REFERENCES LIST_PART(list_part_id)
);

-- Component Formats #################################################
CREATE TABLE FAN_SIZE(
    size_category_mm INTEGER NOT NULL,
    PRIMARY KEY(size_category_mm)
);

CREATE TABLE CPU_SOCKET_TYPE(
    socket_type VARCHAR(127) NOT NULL,
    PRIMARY KEY(socket_type)
);

CREATE TABLE RAM_TYPE(
    ram_type INTEGER NOT NULL,
    PRIMARY KEY(ram_type)
);

CREATE TABLE PCI_SLOT(
    pci_type_id INTEGER NOT NULL,
    pci_version VARCHAR(31) NOT NULL,
    pin_count INTEGER NOT NULL,
    PRIMARY KEY(pci_type_id)
);

CREATE TABLE MOTHERBOARD_FORM_FACTOR(
    form_factor VARCHAR(127) NOT NULL,
    PRIMARY KEY(form_factor)
);

-- COMPONENTS ##############################################################
-- power supply group
CREATE TABLE POWER_SUPPLY_UNIT(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    power_rating INTEGER NOT NULL,
    modular BOOLEAN NOT NULL,
    length_mm INTEGER NOT NULL,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id)
);
CREATE TABLE POWER_SUPPLY_CONNECTORS(
    list_part_id INTEGER NOT NULL,
    conn_type VARCHAR(63),
    num_pins INTEGER,
    count INTEGER,
    PRIMARY KEY(list_part_id, conn_type, num_pins),
    FOREIGN KEY(list_part_id) REFERENCES POWER_SUPPLY_UNIT(list_part_id)
);

CREATE TABLE PC_CASE(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    height INTEGER,
    width INTEGER,
    len_case INTEGER, 
    material VARCHAR(31),
    num_35_bays INTEGER,
    num_25_bays INTEGER,
    max_gpu_len_mm INTEGER,
    max_psu_len_mm INTEGER,
    max_air_cooler_height INTEGER,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id)
);

CREATE TABLE CASE_RADIATOR_SPACE(
    list_part_id INTEGER NOT NULL,
    loc_in_case VARCHAR(31),
    height INTEGER,
    width INTEGER,
    len_rad INTEGER,
    PRIMARY KEY(list_part_id, loc_in_case),
    FOREIGN KEY(list_part_id) REFERENCES PC_CASE(list_part_id)
);
CREATE TABLE CASE_IO_PORT(
    list_part_id INTEGER NOT NULL,
    con_version VARCHAR(63),
    generation VARCHAR(15),
    con_type VARCHAR(63),
    count INTEGER,
    PRIMARY KEY(list_part_id, con_version),
    FOREIGN KEY(list_part_id) REFERENCES PC_CASE(list_part_id)
);

CREATE TABLE FAN(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    fan_rpm INTEGER,
    noise_level FLOAT(24),
    size_category_mm INTEGER NOT NULL,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id),
    FOREIGN KEY(size_category_mm) REFERENCES FAN_SIZE(size_category_mm)
);

CREATE TABLE ETHERNET_CONTROLLER(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id)
);

CREATE TABLE MOTHERBOARD(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    num_ram_slots INTEGER,
    chipset_name VARCHAR(127),
    num_SATA_connectors INTEGER,
    num_cooler_headers INTEGER,
    num_fan_headers INTEGER,
    form_factor VARCHAR(127) NOT NULL,
    socket_type VARCHAR(127) NOT NULL,
    ram_type VARCHAR(127) NOT NULL,
    ethernet_con_id INTEGER,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id),
    FOREIGN KEY(form_factor) REFERENCES MOTHERBOARD_FORM_FACTOR(form_factor),
    FOREIGN KEY(socket_type) REFERENCES CPU_SOCKET_TYPE(socket_type),
    FOREIGN KEY(ram_type) REFERENCES RAM_TYPE(ram_type),
    FOREIGN KEY(ethernet_con_id) REFERENCES ETHERNET_CONTROLLER(list_part_id)
);
CREATE TABLE MOTHERBOARD_IO_PORTS(
    list_part_id INTEGER NOT NULL,
    con_version VARCHAR(63),
    generation VARCHAR(15),
    con_type VARCHAR(63),
    count INTEGER,
    PRIMARY KEY(list_part_id, con_version, generation, con_type),
    FOREIGN KEY(list_part_id) REFERENCES MOTHERBOARD(list_part_id)
);
CREATE TABLE MOTHERBOARD_PCI_SLOT(
    list_part_id INTEGER NOT NULL,
    pci_type_id INTEGER NOT NULL,
    num_slots INTEGER NOT NULL,
    PRIMARY KEY(list_part_id, pci_type_id),
    FOREIGN KEY(list_part_id) REFERENCES MOTHERBOARD(list_part_id),
    FOREIGN KEY(pci_type_id) REFERENCES PCI_SLOT(pci_type_id)
);

CREATE TABLE CPU_COOLER(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    nosie_level INTEGER,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id)
);
CREATE TABLE AIR_COOLER(
    list_part_id INTEGER NOT NULL,
    fan_rpm INTEGER,
    height INTEGER,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES CPU_COOLER(list_part_id)
);
CREATE TABLE LIQUID_COOLER(
    list_part_id INTEGER NOT NULL,
    num_fans INTEGER,
    len_cool INTEGER,
    width INTEGER,
    height INTEGER,
    fan_rpm INTEGER,
    cooling_tube_length INTEGER,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES CPU_COOLER(list_part_id)
);

-- capacity is in GB
-- read/write speed is in MB/s
CREATE TABLE STORAGE(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    capacity INTEGER,
    read_speed INTEGER,
    write_speed INTEGER,
    form_factor VARCHAR(127),
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id)
);

CREATE TABLE M2_STORAGE(
    list_part_id INTEGER NOT NULL,
    pci_type_id INTEGER NOT NULL,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES STORAGE(list_part_id),
    FOREIGN KEY(pci_type_id) REFERENCES PCI_SLOT(pci_type_id)
);

CREATE TABLE HHD_STORAGE(
    list_part_id INTEGER NOT NULL,
    interface VARCHAR(127),
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES STORAGE(list_part_id)
);

CREATE TABLE SATA_STORAGE(
    list_part_id INTEGER NOT NULL,
    interface VARCHAR(127),
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES STORAGE(list_part_id)
);

-- clock is in MHz
CREATE TABLE GPU(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    series VARCHAR(63),
    architecture VARCHAR(63),
    base_clock INTEGER,
    boost_clock INTEGER,
    memory_size INTEGER,
    memory_type INTEGER,
    num_cores INTEGER,
    power_consumption INTEGER,
    pci_type_id INTEGER NOT NULL,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id),
    FOREIGN KEY(pci_type_id) REFERENCES PCI_SLOT(pci_type_id)
);

-- frequency is in MHz
CREATE TABLE RAM(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    capacity INTEGER NOT NULL,
    max_freq INTEGER NOT NULL,
    ram_type VARCHAR(127) NOT NULL,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id),
    FOREIGN KEY(ram_type) REFERENCES RAM_TYPE(ram_type)
);

-- clock is in MHz (NOT GHz because int would convert 5.0 - 5.9 to 5)
-- l1, cache is in KB (total size, not per core)
-- l2 and l3 cache is in MB
CREATE TABLE CPU(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    chip_family VARCHAR(63) NOT NULL,
    series VARCHAR(63) NOT NULL,
    TDP INTEGER NOT NULL,
    base_clock INTEGER,
    boost_clock INTEGER,
    l1_cache INTEGER,
    l2_cache INTEGER,
    l3_cache INTEGER,
    num_cores INTEGER,
    num_threads INTEGER,
    architecture VARCHAR(31),
    socket_type VARCHAR(127) NOT NULL,
    ram_type VARCHAR(127) NOT NULL,
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id),
    FOREIGN KEY(socket_type) REFERENCES CPU_SOCKET_TYPE(socket_type),
    FOREIGN KEY(ram_type) REFERENCES RAM_TYPE(ram_type)
);

CREATE TABLE WIFI_MODULE(
    list_part_id INTEGER NOT NULL,
    product_name VARCHAR(127) NOT NULL,
    pci_type_id INTEGER NOT NULL,    
    PRIMARY KEY(list_part_id),
    FOREIGN KEY(list_part_id) REFERENCES LIST_PART(list_part_id),
    FOREIGN KEY(pci_type_id) REFERENCES PCI_SLOT(pci_type_id)
);


-- compatibility relations ##########################################################
CREATE TABLE CASE_FORM_FACTOR_COMPATIBLE(
    list_part_id INTEGER NOT NULL,
    form_factor VARCHAR(127) NOT NULL,
    CONSTRAINT pk PRIMARY KEY(list_part_id, form_factor),
    FOREIGN KEY(form_factor) REFERENCES MOTHERBOARD_FORM_FACTOR(form_factor),
    FOREIGN KEY(list_part_id) REFERENCES PC_CASE(list_part_id)
);

CREATE TABLE CASE_FAN_SIZE_COMPATIBLE(
    list_part_id INTEGER NOT NULL,
    size_category_mm INTEGER NOT NULL,
    num_fans INTEGER NOT NULL,
    CONSTRAINT pk PRIMARY KEY(list_part_id, size_category_mm),
    FOREIGN KEY(list_part_id) REFERENCES PC_CASE(list_part_id),
    FOREIGN KEY(size_category_mm) REFERENCES FAN_SIZE(size_category_mm)
);

""")
    
    cursor.executescript("""
-- SEED with some example components #############################################################
-- ###############################################################################################

-- User tables #####################################################################

-- (custID, 'firstname', 'middlename', 'lastname', 'A0A 0A0', '123-routeway','city','province', 'country')
INSERT INTO CUSTOMER VALUES(1, 'Art', 'middlename', 'Vandeley', 'A0A 0A0', '123-routeway','New York','New York', 'U.S.A');

-- (manid, 'name')
INSERT INTO MANUFACTURER VALUES
(1, "Nvidia"),
(2, "Intel"),
(3, "AMD"),
(4, "Crosair"),
(5, "Asus"),
(6, "G.SKILL"),
(7, "Qualcomm"),
(8, "MSI"),
(9, "GIGABYTE"),
(10, "Arctic"),
(11, "Seagate"),
(12, "Realtek");

-- (supid, 'name')
INSERT INTO SUPPLIER VALUES
(1, "Amazon"),
(2, "Newegg"),
(3, "Memory Express"),
(4, "Best Buy");

-- Base classes ####################################################################
-- (listpartid)
INSERT INTO LIST_PART VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10),
(11),
(12),
(13),
(14),
(15),
(16);

-- (itmnumber, supid, price,listpartid)
INSERT INTO STORE_ITEM VALUES
(1, 1, 100.0, 16),
(2, 2, 100.0, 15),
(3, 3, 100.0, 14),
(4, 4, 100.0, 13),
(5, 1, 100.0, 12),
(6, 2, 100.0, 11),
(7, 3, 200.0, 1),
(8, 3, 120.0, 2),
(9, 3, 20.0, 3),
(10, 3, 100.0, 4),
(11, 3, 250.0, 5),
(12, 3, 220.0, 6),
(13, 3, 500.0, 7),
(14, 3, 550.0, 8),
(15, 3, 1500.0, 9),
(16, 3, 900.0, 10),
(17, 3, 100.0, 11);


-- (partid, manid, listpartid)
INSERT INTO COMPONENT VALUES
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
(12, 5, 12);

-- customer build list stuf ########################################################

-- (listnumber, custid)
INSERT INTO BUILD_LIST VALUES(1,1);

-- (listnumber, custid, listpartid, num_comps)
INSERT INTO CONTAINS_COMPONENT VALUES(1, 1, 3);

-- Component Formats #################################################

INSERT INTO FAN_SIZE VALUES (90), (120), (140), (200);
INSERT INTO CPU_SOCKET_TYPE VALUES ("Socket sTR5"),
("Socket SP6"),
("Socket SP5"),
("Socket AM5"),
("Socket sWRX8"),
("Socket sTRX4"),
("Socket TR4"),
("Socket SP3"),
("Socket AM4"),
("Socket AM1"),
("Socket FM2+"),
("Socket FM2"),
("Socket AM3+"),
("Socket FS1"),
("Socket FM1"),
("Socket C32"),
("Socket C34"),
("Socket AM3"),
("rPGA 988A"),
("LGA 1156"),
("LGA 1567"),
("LGA 1155"),
("rPGA 988B"),
("LGA 1356"),
("LGA 1150"),
("rPGA 946B/947"),
("LGA 2011"),
("LGA 1151"),
("LGA 3647"),
("LGA 2066"),
("LGA 4189"),
("LGA 1200"),
("LGA 1700"),
("LGA 4677"),
("LGA 1851"),
("LGA 4710"),
("LGA 7529");

INSERT INTO PCI_SLOT VALUES (0, "PCIe 5.0", 16), (1, "PCIe 4.0", 16), (2, "PCIe 3.0", 16), (3, "PCIe 2.0", 16),
(4, "PCIe 5.0", 4), (5, "PCIe 4.0", 4), (6, "PCIe 3.0", 4), (7, "PCIe 2.0", 4);

INSERT INTO MOTHERBOARD_FORM_FACTOR VALUES ("ATX"), ("Micro-ATX"), ("Mini-ATX"), ("XT"), ("Mini-ITX"), ("Nano-ITX"), ("Pico-ITX"), ("Mobile-ITX");

-- COMPONENTS ##############################################################

INSERT INTO POWER_SUPPLY_UNIT VALUES (1, "MPG A1000GS PCIE5, FULLY Modular", 1000, 1, 150);

INSERT INTO POWER_SUPPLY_CONNECTORS VALUES(1, "ATX", 28, 1),
(1, "CPU/PCIe", 8, 3),
(1, "SATA/Peripheral", 6, 3),
(1, "12V 2x6", 12, 2);

INSERT INTO PC_CASE VALUES(2, "Corsair FRAME 4000D RS", 500, 240, 600, "Steel", 4, 2, 400, 220, 200);

INSERT INTO CASE_RADIATOR_SPACE VALUES(2, "FRONT", 50, 220, 360),
(2, "TOP", 50, 220, 360),
(2, "SIDE", 50, 220, 360),
(2, "REAR", 50, 220, 140);

INSERT INTO CASE_IO_PORT VALUES(2, "USB", "3.0", "", 2),
(2, "USB-C", "3.0", "", 1);

INSERT INTO FAN VALUES(3, "RS120 ARGB PWM", 2100, 36, 120);

INSERT INTO ETHERNET_CONTROLLER VALUES(4, "Intel Ethernet Converged Network Adapter X550");

INSERT INTO MOTHERBOARD VALUES(5, "X870 GAMING WIFI6 AM5 LGA 1718", 4, "X870", 4, 1, 4, "ATX", "Socket AM5", "DDR5", 4);

INSERT INTO MOTHERBOARD_IO_PORTS VALUES(5, "HDMI", "", "", 1),
(5, "USB-C", "4.0", "", 2),
(5, "USB", "3.2", "Gen 2", 1),
(5, "USB", "3.2", "Gen 1", 3),
(5, "USB", "2.0", "", 4),
(5, "RJ", "45", "", 1),
(5, "Audio jacks", "", "", 3);

INSERT INTO MOTHERBOARD_PCI_SLOT VALUES(5, 0, 1), 
(5, 2, 2),
(5, 4, 1),
(5, 5, 1);

INSERT INTO CPU_COOLER VALUES(6, "Arctic Liquid Freezer III Pro 360", 39);

INSERT INTO LIQUID_COOLER VALUES(6, 3, 360, 120, 38, 3000, 400);

-- capacity is in GB
-- read/write speed is in MB/s
INSERT INTO STORAGE VALUES(7, "Firecuda 520", 500, 5000, 2500, "M.2");

INSERT INTO M2_STORAGE VALUES(7, 5);


-- capacity is in GB
-- read/write speed is in MB/s

-- clock is in MHz
INSERT INTO GPU VALUES (8, "AMD Radeon RX 9060 XT", "RX 9000", "", 2530, 3130, 16, "GDDR6", 2048, 160, 0);

-- frequency is in MHz
INSERT INTO RAM VALUES (9, "Vengenance 2x32GB", 64, 6400, "DDR5");

-- clock is in MHz (NOT GHz because int would convert 5.0 - 5.9 to 5)
-- l1, cache is in KB (total size, not per core)
-- l2 and l3 cache is in MB
INSERT INTO CPU VALUES (10, "Ryzen 9 9950x", "Ryzen", "9 9000", 170, 4300, 5700, 1280, 16, 64, 16, 32, "Zen-5", "Socket AM5", "DDR5");

INSERT INTO WIFI_MODULE VALUES(11, "Realtek Wi-Fi 6", 4);


""")
    
    conn.commit()
    conn.close()



PART_TYPES=["psu", "case", "air_cooler", "liquid_cooler", "gpu", "ram", "cpu", "motherboard", "m2_storage", "sata_storage", "hhd_storage", "wifi_module"]
COMPONENT_TABLES=["POWER_SUPPLY_UNIT", "PC_CASE", "FAN", "ETHERNET_CONTROLLER", "MOTHERBOARD", "CPU_COOLER", "STORAGE", "GPU", "CPU", "RAM", "WIFI_MODULE"]
COMPONENT_TABLES_SYS=["POWER_SUPPLY_UNIT", "POWER_SUPPLY_CONNECTORS", "PC_CASE", "CASE_RADIATOR_SPACE", "CASE_IO_PORT", "FAN", "ETHERNET_CONTROLLER", "MOTHERBOARD", "MOTHERBOARD_IO_PORTS", "MOTHERBOARD_PCI_SLOT","CPU_COOLER", "AIR_COOLER", "LIQUID_COOLER", "STORAGE", "M2_STORAGE", "HHD_STORAGE", "SATA_STORAGE", "GPU", "CPU", "RAM", "WIFI_MODULE"]

def seed_database():
    """fill the database with some default values"""

## DATABASE MODIFICATION FUNCTIONS ######################################################
def manuel_query(query):
    """directly passes query to the database and returns the output"""
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # blindly pass the query to sql
    query_string = query
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    # pass results if there are any
    if results != None:
        return results
    
    return True

# MANUFACTURER STUFF###############################################################################################################################
# #################################################################################################################################################

def get_manufacturers():
    """gets a list of all manufacturers"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this manufacturer already exists, if so return false
    query_string = f"SELECT * FROM MANUFACTURER"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    conn.close()
    return results

def add_manufacturer(name: str) -> bool:
    """add a manufacturer to the 'MANUFACTURER' table
    returns true on success """
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this manufacturer already exists, if so return false
    query_string = f"SELECT * FROM MANUFACTURER WHERE manufacturer_name = '{name}'"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        print(("Could not add manufacturer: %s as it already exists" % (name)))
        return False
    
    # the manufacturer does not exist so add them
    # first get highest id number of the existing manufacturers
    query_string = "SELECT MAX(manufacturer_id) FROM MANUFACTURER"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    # get the current max, check if it is null 
    current_max = results[0][0]
    if current_max == None:
        current_max = -1
    # increment the current max to get the next id
    new_id = current_max + 1
    
    # command for adding the manufacturer
    query_string = f"INSERT INTO MANUFACTURER VALUES ({new_id},'{name}');"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def delete_manufacturer(id: int) -> bool:
    """deletes a manufacturer from 'MANUFACTURER' table,
    Note that this may delete any related items from the tables:
    'CONTAINS_COMPONENT', 'STORE_ITEM', 'COMPONENT',
    'LIST_PART' or any part table,
    Returns true on success"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()

    # command to delete from build lists 
    query_string = f"DELETE FROM CONTAINS_COMPONENT WHERE CONTAINS_COMPONENT.list_part_id IN (SELECT COMPONENT.list_part_id FROM COMPONENT WHERE COMPONENT.manufacturer_id = {id});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    # command to delete asociated store items
    query_string = f"DELETE FROM STORE_ITEM WHERE STORE_ITEM.list_part_id IN (SELECT COMPONENT.list_part_id FROM COMPONENT WHERE COMPONENT.manufacturer_id = {id});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # loop over every part table and delete parts with this manufacturer 
    output=[]
    for part_type in COMPONENT_TABLES_SYS:
        query_string = f"DELETE FROM {part_type} WHERE {part_type}.list_part_id IN (SELECT COMPONENT.list_part_id FROM COMPONENT WHERE COMPONENT.manufacturer_id = {id});"

        try:
            cursor.execute(query_string)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query error: {e}")
            conn.close()
            return False
        
        if len(results) > 0:
            output = output + results
    
    # command to delete list part
    query_string = f"DELETE FROM LIST_PART WHERE LIST_PART.list_part_id IN (SELECT COMPONENT.list_part_id FROM COMPONENT WHERE COMPONENT.manufacturer_id = {id});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # command to delete the component base class
    query_string = f"DELETE FROM COMPONENT WHERE COMPONENT.manufacturer_id = {id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    
    # command for deleting the manufacturer
    query_string = f"DELETE FROM MANUFACTURER WHERE manufacturer_id={id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    conn.commit()
    conn.close()

    return True

def get_parts_of_manufacturer(manufacturer_id:int):
    """returns a list of all the parts bellonging to a manufacturer"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    

    # loop over every part table and get the parts 
    output=[]
    for part_type in COMPONENT_TABLES:
        query_string = f"SELECT * FROM (SELECT * FROM COMPONENT WHERE COMPONENT.manufacturer_id = {manufacturer_id}) AS T INNER JOIN {part_type} ON {part_type}.list_part_id = T.list_part_id;"

        try:
            cursor.execute(query_string)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query error: {e}")
            conn.close()
            return False
        
        if len(results) > 0:
            output = output + results
        
    conn.close()
    return output


# SUPPLIER STUFF###############################################################################################################################
# #################################################################################################################################################
def get_suppliers():
    """gets a list of all suppliers"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this supplier already exists, if so return false
    query_string = f"SELECT * FROM SUPPLIER"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.close()
    return results

def get_suppliers_of_part(list_part_id:int):
    """Gets all suppliers that have this part"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()

    # query the database to see what suppliers sell this part, and for what cost
    query_string = f"""SELECT * FROM ((SELECT * FROM STORE_ITEM WHERE STORE_ITEM.list_part_id = {list_part_id}) AS T INNER JOIN SUPPLIER ON SUPPLIER.supplier_id = T.supplier_id)"""
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.close()
    return results

def add_supplier(name:str)->bool:
    """add a supplier to the 'SUPPLIER' table
     returns true on success"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this supplier already exists, if so return false
    query_string = f"SELECT * FROM SUPPLIER WHERE supplier_name = '{name}'"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        print(("Could not add supplier: %s as it already exists" % (name)))
        return False
    
    # the supplier does not exist so add them
    # first get highest id number of the existing suppliers
    query_string = "SELECT MAX(supplier_id) FROM SUPPLIER"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    # get the current max, check if it is null 
    current_max = results[0][0]
    if current_max == None:
        current_max = -1
    # increment the current max to get the next id
    new_id = current_max + 1
    
    # command for adding the supplier
    query_string = f"INSERT INTO SUPPLIER VALUES ({new_id},'{name}');"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def delete_supplier(id: int) -> bool:
    """deletes a Supplier from 'SUPPLIER' table,
    Note that this may delete any related items from the tables:
    'STORE_ITEM',
    Returns true on success"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for deleting the supplier
    query_string = f"DELETE FROM SUPPLIER WHERE supplier_id={id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def get_parts_sold_by_supplier(supplier_id:int):
    """returns a list of all parts sold by a supplier"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    

    # loop over every part table and get the parts 
    output=[]
    for part_type in COMPONENT_TABLES:
        query_string = f"SELECT * FROM (SELECT * FROM STORE_ITEM WHERE STORE_ITEM.supplier_id = {supplier_id}) AS T INNER JOIN {part_type} ON {part_type}.list_part_id = T.list_part_id;"

        try:
            cursor.execute(query_string)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query error: {e}")
            conn.close()
            return False
        
        if len(results) > 0:
            output = output + results
        
    conn.close()
    return output

def add_store_item(list_part_id:int, supplier_id:int, price:int)->bool:
    """add a store item to 'STORE_ITEM' that corresponds to part with key 'list_part_id'
    returns true on success"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this store item already exists, if so return false
    query_string = f"SELECT * FROM STORE_ITEM WHERE supplier_id = {supplier_id} AND list_part_id = {list_part_id}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        print(("Could not add store item: %d %d as this item already exists" % (list_part_id, supplier_id)))
        return False
    
    # ensure that the list_part corresponds to an actual part
    query_string = f"SELECT * FROM LIST_PART WHERE list_part_id = {list_part_id}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) == 0:
        conn.close()
        print(("list_part_id does not correspond to an available part %d" % (list_part_id)))
        return False
    
    # ensure that the supplier_id corresponds to an actual supplier
    query_string = f"SELECT * FROM SUPPLIER WHERE supplier_id = {supplier_id}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) == 0:
        conn.close()
        print(("supplier_id does not correspond to an available supplier %d" % (supplier_id)))
        return False
    
    # the store item does not exist so add it
    # first get highest id number of the store items
    query_string = f"SELECT MAX(item_number) FROM STORE_ITEM;"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    # get the current max, check if it is null 
    current_max = results[0][0]
    if current_max == None:
        current_max = -1
    # increment the current max to get the next id
    new_id = current_max + 1
    
    # command for adding the customer
    query_string = f"INSERT INTO STORE_ITEM VALUES ({new_id},{supplier_id}, {price}, {list_part_id});"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True


def delete_store_item(item_number : int) -> bool:
    """Deletes a part from the 'STORE_ITEM' table by key {item_number, supplier_id},
    Does not modify any other table
    Returns success or failure"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for deleting the store item
    query_string = f"DELETE FROM STORE_ITEM WHERE item_number = {item_number};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

# CUSTOMER STUFF###############################################################################################################################
# #################################################################################################################################################

def get_customers():
    """gets a list of all customers"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this  already exists, if so return false
    query_string = f"SELECT * FROM CUSTOMER"
    cursor.execute(query_string)
    results = cursor.fetchall()
    conn.close()
    return results

def add_customer(first_name:str, middle_name:str, last_name:str, postal_code:str, street_no:str, city:str, province:str, country:str)->bool:
    """Add a customer to table 'CUSTOMER' returns true on success"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this supplier already exists, if so return false
    query_string = f"SELECT * FROM CUSTOMER WHERE first_name = '{first_name}' AND last_name = '{last_name}'"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        print(("Could not add customer: %s %s as this person already exists" % (first_name, last_name)))
        return False
    
    # the customer does not exist so add them
    # first get highest id number of the existing customer
    query_string = "SELECT MAX(customer_id) FROM CUSTOMER"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    # get the current max, check if it is null 
    current_max = results[0][0]
    if current_max == None:
        current_max = -1
    # increment the current max to get the next id
    new_id = current_max + 1
    
    # command for adding the customer
    query_string = f"INSERT INTO CUSTOMER VALUES ({new_id},'{first_name}', '{middle_name}', '{last_name}', '{postal_code}', '{street_no}', '{city}', '{province}', '{country}');"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True


def delete_customer(customer_id:int)->bool:
    """Delete a customer from table 'CUSTOMER', modifies tables 'BUILD_LIST' and 'CONTAINS_COMPONENT' returns true on success"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for deleting the customer
    query_string = f"DELETE FROM CUSTOMER WHERE customer_id={customer_id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def create_build_list(customer_id:int)->bool:
    """add a build list to 'BUILD_LIST' returns true on success"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()

    # ensure that the customer_id corresponds to an actual customer
    query_string = f"SELECT * FROM CUSTOMER WHERE customer_id = {customer_id}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) == 0:
        conn.close()
        print(("customer_id does not correspond to an available customer %d" % (customer_id)))
        return False
    
    # the customer does exist so add a new build list
    # first get highest id number of the existing customer
    query_string = f"SELECT MAX(list_number) FROM BUILD_LIST"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    # get the current max, check if it is null 
    current_max = results[0][0]
    if current_max == None:
        current_max = -1
    # increment the current max to get the next id
    new_id = current_max + 1
    
    # command for adding the new build list
    query_string = f"INSERT INTO BUILD_LIST VALUES ({new_id},{customer_id});"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def delete_build_list(list_id:int)->bool:
    """Delete a build list from table 'BUILD_LIST' and any related list"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for deleting the build list
    query_string = f"DELETE FROM BUILD_LIST WHERE list_number={list_id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # delete from the contains component table
    # command for deleting the customer
    query_string = f"DELETE FROM CONTAINS_COMPONENT WHERE list_number={list_id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def add_to_build_list(list_id:int, list_part_id:int, num_comps:int)->bool:
    """add a list part to a build list, modifies table 'CONTAINS_COMPONENT' returns true on success"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this component is already on the build list, if so return false
    query_string = f"SELECT * FROM CONTAINS_COMPONENT WHERE list_number = {list_id} AND list_part_id = {list_part_id}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        print(("Could not add item: %d to build list %d as this item is already included" % (list_id, list_part_id)))
        return False
    
    # ensure that the list_part corresponds to an actual part
    query_string = f"SELECT * FROM LIST_PART WHERE list_part_id = {list_part_id}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) == 0:
        conn.close()
        print(("list_part_id does not correspond to an available part %d" % (list_part_id)))
        return False
    
    # ensure that the list_id corresponds to an actual value
    query_string = f"SELECT * FROM BUILD_LIST WHERE list_number = {list_id}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) == 0:
        conn.close()
        print(("list_id does not correspond to an available build list %d" % (list_id)))
        return False
    
    # the list exists, and the component exists, so add the component to the list
    # command for adding the customer
    query_string = f"INSERT INTO CONTAINS_COMPONENT VALUES ({list_id}, {list_part_id}, {num_comps});"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def delete_part_in_build_list(list_id:int, list_part_id:int)->bool:
    """Delete a part form the build list, modifies 'CONTAINS_COMPONENT' table, returns true on success"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for deleting the build list component
    query_string = f"DELETE FROM CONTAINS_COMPONENT WHERE list_number={list_id} AND list_part_id={list_part_id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def get_parts_in_build_list(build_list_id:int):
    """returns a list of all parts in a build list"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    

    # loop over every part table and get the parts 
    output=[]
    for part_type in COMPONENT_TABLES:
        query_string = f"""SELECT * FROM ((
        (SELECT * FROM BUILD_LIST WHERE BUILD_LIST.list_number = {build_list_id}) AS T1 
        INNER JOIN CUSTOMER ON CUSTOMER.customer_id = T1.customer_id) AS T2
        INNER JOIN CONTAINS_COMPONENT ON T2.list_number = CONTAINS_COMPONENT.list_number) AS T3
        INNER JOIN {part_type} ON {part_type}.list_part_id = T3.list_part_id"""

        try:
            cursor.execute(query_string)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query error: {e}")
            conn.close()
            return False
        
        if len(results) > 0:
            output = output + results
        
    conn.close()
    return output

def display_all_build_lists():
    """displays all build lists and their corresponding customers and components"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    

    # loop over every part table and get the parts 
    output=[]
    for part_type in COMPONENT_TABLES:
        query_string = f"""SELECT * FROM (
            (CUSTOMER INNER JOIN BUILD_LIST ON CUSTOMER.customer_id = BUILD_LIST.customer_id) AS T1
            INNER JOIN CONTAINS_COMPONENT ON T1.list_number = CONTAINS_COMPONENT.list_number
            ) AS T2 INNER JOIN {part_type} ON {part_type}.list_part_id = T2.list_part_id"""
        try:
            cursor.execute(query_string)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query error: {e}")
            conn.close()
            return False
        
        if len(results) > 0:
            output = output + results
        
    conn.close()
    return output

# Adding components ###############################################################################################################################
# #################################################################################################################################################

def add_base_part(manufacturer_id:int, cursor: sqlite3.Cursor)->bool:
    """adds a base part, used internally, do not call from the frontend or interface"""
    # query the database to ensure that the manufacturer exists, if not return false
    query_string = f"SELECT * FROM MANUFACTURER WHERE manufacturer_id = {manufacturer_id}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False

    if len(results) == 0:
        print(("Not a valid manufacturer id: %d cannot add part" % (manufacturer_id)))
        return False
    
    # the manufacturer does exist so add the part
    # first get highest id number of the component and the list part id
    query_string = "SELECT MAX(part_id), MAX(list_part_id) FROM COMPONENT;"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False

    part_id = results[0][0]
    list_part_id = results[0][1]

    
    if part_id == None:
        part_id = -1
    
    if list_part_id == None:
        list_part_id = -1

    part_id += 1
    list_part_id += 1
    print("list part id: %d" % (list_part_id))
    # command for adding the part to components
    query_string = f"INSERT INTO COMPONENT VALUES ({part_id}, {manufacturer_id}, {list_part_id});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False
    
    # command for adding part to list part
    query_string = f"INSERT INTO LIST_PART VALUES ({list_part_id});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        return False
    
    return part_id, list_part_id

def add_part_psu(manufacturer_id:int, product_name: str, power_rating: int, modular: bool, length_mm: bool, connectors) -> bool:
    """adds to tables: 'LIST_PART' and 'POWER_SUPPLY_UNIT' and 'POWER_SUPPLY_CONNECTORS' returns true on success,
    connectors is an array with tuple elements {conn_type:str, num_pins:int, count:int}"""

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO POWER_SUPPLY_UNIT VALUES ({list_part_id}, '{product_name}', {power_rating}, {modular}, {length_mm});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # if we have connectors, add connectors
    if len(connectors) > 0:
        for c in connectors:
            # check that the number of parameters is correct
            if len(c) == 3:
                # for each connector 
                conn_type, num_pins, count = c
                # command for adding the part 
                query_string = f"INSERT INTO POWER_SUPPLY_CONNECTORS VALUES ({list_part_id},'{conn_type}', {num_pins}, {count});"
                try:
                    cursor.execute(query_string)
                except sqlite3.Error as e:
                    print(f"query error: {e}")
                    conn.close()
                    return False
                    
    conn.commit()
    conn.close()

    return True

def add_form_factor(form_factor:str)->bool:
    """add a motherboard form factor"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this form factor already exists
    query_string = f"SELECT * FROM MOTHERBOARD_FORM_FACTOR WHERE form_factor = '{form_factor}';"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        return False
    # the from factor does not exist so add the new form factor
    # first get highest id number of the existing customer

    # command for adding the customer
    query_string = f"INSERT INTO MOTHERBOARD_FORM_FACTOR VALUES ('{form_factor}');"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    print("added new form factor %s" % (form_factor))
    conn.commit()
    conn.close()

    return True

def add_fan_size(fan_size:int)->bool:
    """add a motherboard form factor"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this fan size already exists
    query_string = f"SELECT * FROM FAN_SIZE WHERE size_category_mm = {fan_size};"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        return False
    # the fan size does not exist so add the new form factor

    # command for adding the customer
    query_string = f"INSERT INTO FAN_SIZE VALUES ({fan_size});"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    print("added new fan size %d" % (fan_size))
    conn.commit()
    conn.close()

    return True

def add_case_form_factor_compatible(case_id:int, form_factor:str):
    """adds compatibility relation between case and form factor"""

    # ensure that the form factor exists
    add_form_factor(form_factor)
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this element already exists
    query_string = f"SELECT * FROM CASE_FORM_FACTOR_COMPATIBLE WHERE list_part_id = {case_id} AND form_factor = '{form_factor}';"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        return False
    # the fan size does not exist so add the new form factor

    # command for adding the element
    query_string = f"INSERT INTO CASE_FORM_FACTOR_COMPATIBLE VALUES ({case_id},'{form_factor}');"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()
    
    return True

def add_case_fans_compatible(case_id:int, size_category_mm:int, num_fans:int):
    """adds compatibility relation between case and form factor"""

    # ensure that the form factor exists
    add_fan_size(size_category_mm)
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this element already exists
    query_string = f"SELECT * FROM CASE_FAN_SIZE_COMPATIBLE WHERE list_part_id = {case_id} AND size_category_mm = {size_category_mm};"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        return False
    # the fan size does not exist so add the new form factor

    # command for adding the element
    query_string = f"INSERT INTO CASE_FAN_SIZE_COMPATIBLE VALUES ({case_id},{size_category_mm},{num_fans});"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()
    
    return True

def add_part_case(manufacturer_id:int, product_name: str,
                height: int, width: int, len_case: int, material: str,
                num_35_bays: int, num_25_bays:int, max_gpu_length_mm:int, 
                max_psu_length_mm:int,max_air_cooler_height:int, 
                radiator_spaces, io_ports, fans, form_factors)->bool:
    """adds to tables: 'LIST_PART', 'PC_CASE', 'CASE_RADIATOR_SPACE', 'CASE_IO_PORT','CASE_FITS_FAN_SIZE', 'FAN_SIZE' returns true on success
    radiator_spaces is an array with tuple elements {loc_in_case:str, height:int, width:int, len_rad:int}
    io_ports is an array with tuple elements {con_version:str, generation:str, con_type:str}
    fans is an array with tuple elements {size_mm:int, num_fans:int}"""

 

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO PC_CASE VALUES ({list_part_id}, '{product_name}', {height}, {width}, {len_case}, '{material}', {num_35_bays}, {num_25_bays}, {max_gpu_length_mm}, {max_psu_length_mm}, {max_air_cooler_height});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    # ensure that the fan sizes exist
    if len(fans) > 0:
        for f in fans:
            if len(f) == 2:
                fan_size, num_fans = f
                add_case_fans_compatible(list_part_id, fan_size, num_fans)

    # ensure that the form factor exists
    if len(form_factors) > 0:
        for f in form_factors:
            add_case_form_factor_compatible(list_part_id, f)

    return True

def add_part_fan(manufacturer_id:int, product_name:str, fan_rpm:int, noise_level:float, size_category_mm:int)->bool:
    """adds to tables: 'LIST_PART' and 'FAN' and 'FAN_SIZE'returns true on success'"""
    # ensure that the form factor exists
    add_fan_size(size_category_mm)

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO FAN VALUES ({list_part_id}, '{product_name}', {fan_rpm}, {noise_level}, {size_category_mm});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()
    return True

def add_part_ethernetcontroller(manufacturer_id:int, product_name:str)->bool:
    """adds to tables: 'LIST_PART' and 'ETHERNET_CONTROLLER' returns true on success'"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO ETHERNET_CONTROLLER VALUES ({list_part_id}, '{product_name}');"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()
    return True

def add_socket_type(cpu_socket_type:str):
    """add a cpu socket type"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this fan size already exists
    query_string = f"SELECT * FROM CPU_SOCKET_TYPE WHERE socket_type = '{cpu_socket_type}';"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        return False
    # the fan size does not exist so add the new form factor

    # command for adding the customer
    query_string = f"INSERT INTO CPU_SOCKET_TYPE VALUES ('{cpu_socket_type}');"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    print("added new socket type %s" % (cpu_socket_type))
    conn.commit()
    conn.close()

    return True

def add_ram_type(ram_type:int):
    """add a cpu socket type"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # query the database to see if this fan size already exists
    query_string = f"SELECT * FROM RAM_TYPE WHERE ram_type = {ram_type};"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    if len(results) > 0:
        conn.close()
        return False
    # the fan size does not exist so add the new form factor

    # command for adding the customer
    query_string = f"INSERT INTO RAM_TYPE VALUES ({ram_type});"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    print("added new socket type ddr%d" % (ram_type))
    conn.commit()
    conn.close()

    return True

def add_part_motherboard(manufacturer_id:int, product_name:str, num_ram_slots:int, chipset_name:str, num_sata_conn:int,num_cooler_headers:int, num_fan_headers:int, form_factor:str, socket_type:str, ram_type:int, eth_controller:int,io_ports, pci_slots)->bool:
    """adds to tables: 'LIST_PART', 'MOTHERBOARD', 'MOTHERBOARD_IO_PORTS', 'MOTHERBOARD_PCI_SLOT','PCI_SLOT','ETHERNET_CONTROLLER' returns true on success
    io_ports is an array with tuple elements {version:str, generation:str, con_type:str,count:int}
    pci_slots is an array with tuple elements {pci_version:str, pin_count:int, num_slots:int}'"""

    # ensure the part format types exist
    add_socket_type(socket_type)
    add_form_factor(form_factor)
    add_ram_type(ram_type)
        
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO MOTHERBOARD VALUES ({list_part_id}, '{product_name}', {num_ram_slots}, '{chipset_name}', {num_sata_conn}, {num_cooler_headers}, {num_fan_headers}, '{form_factor}', '{socket_type}', {ram_type}, {eth_controller});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()
    return True

def add_part_cpu_cooler(manufacturer_id:int, product_name:str, noise_level:int):
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO CPU_COOLER VALUES ({list_part_id}, '{product_name}', {noise_level});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return list_part_id

def add_part_air_cooler(manufacturer_id:int, product_name:str, noise_level:int, fan_rpm:int, height:int)->bool:
    """adds to tables: 'LIST_PART' and 'AIR_COOLER','CPU_COOLER' returns true on success'"""

    # create the base part
    list_part_id = add_part_cpu_cooler(manufacturer_id, product_name, noise_level)
    if list_part_id == False:
        return False
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for adding the part 
    query_string = f"INSERT INTO AIR_COOLER VALUES ({list_part_id}, {fan_rpm}, {height});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return True

def add_part_liquid_cooler(manufacturer_id:int, product_name:str, noise_level:int,num_fans:int, len_cool:int, width:int, height:int, fan_rpm:int, cooling_tube_length:int)->bool:
    """adds to tables: 'LIST_PART' and 'LIQUID_COOLER','CPU_COOLER' returns true on success'"""
    # create the base part
    list_part_id = add_part_cpu_cooler(manufacturer_id, product_name, noise_level)
    if list_part_id == False:
        return False
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for adding the part 
    query_string = f"INSERT INTO LIQUID_COOLER VALUES ({list_part_id},{num_fans}, {len_cool}, {width}, {height}, {fan_rpm}, {cooling_tube_length});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return True

def add_part_storage(manufacturer_id:int, product_name:str, capacity:int, read_speed:int, write_speed:int, form_factor:str):
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO STORAGE VALUES ({list_part_id}, '{product_name}', {capacity}, {read_speed}, {write_speed}, '{form_factor}');"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return list_part_id

def add_part_m2storage(manufacturer_id:int, product_name:str, capacity:int, read_speed:int, write_speed:int, form_factor:str, pci_version:str)->bool:
    """adds to tables: 'LIST_PART','STORAGE', 'M2_STORAGE' returns true on success'"""
    # create the base part
    list_part_id = add_part_storage(manufacturer_id, product_name, capacity, read_speed, write_speed, form_factor)
    if list_part_id == False:
        return False
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for adding the part 
    query_string = f"INSERT INTO M2_STORAGE VALUES ({list_part_id},'{pci_version}');"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return True


def add_part_hhdstorage(manufacturer_id:int, product_name:str, capacity:int, read_speed:int, write_speed:int, form_factor:str, interface:str)->bool:
    """adds to tables: 'LIST_PART','STORAGE', 'HHD_STORAGE' returns true on success'"""
    # create the base part
    list_part_id = add_part_storage(manufacturer_id, product_name, capacity, read_speed, write_speed, form_factor)
    if list_part_id == False:
        return False
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for adding the part 
    query_string = f"INSERT INTO HHD_STORAGE VALUES ({list_part_id},'{interface}');"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return True

def add_part_satastorage(manufacturer_id:int, product_name:str, capacity:int, read_speed:int, write_speed:int, form_factor:str, interface:str)->bool:
    """adds to tables: 'LIST_PART','STORAGE', 'SATA_STORAGE' returns true on success'"""
    # create the base part
    list_part_id = add_part_storage(manufacturer_id, product_name, capacity, read_speed, write_speed, form_factor)
    if list_part_id == False:
        return False
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # command for adding the part 
    query_string = f"INSERT INTO SATA_STORAGE VALUES ({list_part_id},'{interface}');"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return True


def add_part_gpu(manufacturer_id:int, product_name:str, series:str, architecture:str, base_clock:int, boost_clock:int, memory_size:int, memory_type:int, num_cores:int, power_cons:int, pci_version:int)->bool:
    """adds to tables: 'LIST_PART','GPU','PCI_SLOT' returns true on success'"""



    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO GPU VALUES ({list_part_id}, '{product_name}', '{series}', '{architecture}', {base_clock}, {boost_clock}, {memory_size}, {memory_type}, {num_cores}, {power_cons}, {pci_version});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return False

def add_part_ram(manufacturer_id:int, product_name:str, capacity:int, max_freq:int, ram_ddr_type:int)->bool:
    """adds to tables: 'LIST_PART' and 'RAM', 'RAM_TYPE' returns true on success'"""
    # ensure ram type exists
    add_ram_type(ram_ddr_type)

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO RAM VALUES ({list_part_id}, '{product_name}', {capacity}, {max_freq}, {ram_ddr_type});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return False

def add_part_cpu(manufacturer_id:int, product_name:str, chip_family:str, series:str, tdp:int, base_clock:int, boost_clock:int, l1_cache:int, l2_cache:int, l3_cache:int, num_cores:int, num_threads:int, architecture:str, socket_type:str, ram_ddr_type:int)->bool:
    """adds to tables: 'LIST_PART','CPU', 'RAM_TYPE', 'CPU_SOCKET_TYPE' returns true on success"""
    # ensure ram type exists
    add_ram_type(ram_ddr_type)
    # ensure socket type exits
    add_socket_type(socket_type)
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO CPU VALUES ({list_part_id}, '{product_name}', '{chip_family}', '{series}', {tdp}, {base_clock}, {boost_clock}, {l1_cache}, {l2_cache}, {l3_cache}, {num_cores}, {num_threads}, '{architecture}', '{socket_type}', {ram_ddr_type});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()

    return False


def add_part_wifimodule(manufacturer_id:int, product_name:str, pci_version:int, pin_count:int)->bool:
    """adds to tables: 'LIST_PART' and 'WIFI_MODULE' and 'PCI_SLOT' returns true on success'"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()
    
    # add the base part
    res = add_base_part(manufacturer_id, cursor)
    # check for success
    if res == False:
        conn.close()
        return False

    # get the id numbers to use
    part_id, list_part_id = res
    
    # command for adding the part 
    query_string = f"INSERT INTO WIFI_MODULE VALUES ({list_part_id}, '{product_name}', {pci_version});"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # add the form factors
    conn.commit()
    conn.close()
    return True








## functions for user interface FUNCTIONS ######################################################

def list_all_parts_of_type(part_type:str):
    """returns a list of all parts of one of the types: ["psu", "case", "air_cooler", "liquid_cooler", "gpu", "ram", "cpu", "motherboard", "m2_storage", "sata_storage", "hhd_storage", "wifi_module"]"""

    if not(part_type in COMPONENT_TABLES_SYS):
        return [(0, f"error, no componenets of type {part_type}")]
    
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()


    query_string = f"SELECT * FROM {part_type}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    conn.close()
    return results


def get_compatible_part(build_list:int, customer_id:int, part_type:str):
    """returns all components of type 'part_type' that are compatible with all components in the give build list"""

    res = []
    if part_type == "POWER_SUPPLY_UNIT":
        # check case compatibility
        res = []
    elif part_type == "CASE":
        # check compatibility with:
        # motherboard,
        # gpu,
        # psu,
        # fans,
        # air cooler,
        # liquid cooler,
        res = []

    elif part_type == "CPU_COOLER":
        # check compatibility with:
        # case
        res = []

    elif part_type == "GPU":
        # check compatibility with:
        # case
        res = []

    elif part_type == "CPU":
        # check compatibility with:
        # motherboard,
        # ram
        res = []

    elif part_type == "FAN":
        # check compatibility with:
        # case
        res = []

    elif part_type == "RAM":
        # check compatibility with:
        # motherboard
        # cpu
        res = []

    elif part_type == "STORAGE":
        # check compatility with 
        # motherboard
        res = []

    else:
        res = []

    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()


    query_string = f"SELECT * FROM {part_type}"
    try:
        cursor.execute(query_string)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False

    conn.close()
    return results

def delete_part(list_part_id : int) -> bool:
    """Deletes a part from the 'COMPONENT' table by key {list_part_id},
    Finds corresponding part by key {list_part_id} and deletes it from 'LIST_PART' 
    along with any components or store items 'STORE_ITEM" with the same key {list_part_id},
    Returns success or failure"""
    # open the database
    conn = sqlite3.connect("parts_picker.db")
    cursor = conn.cursor()

    # command to delete asociated store items
    query_string = f"DELETE FROM STORE_ITEM WHERE STORE_ITEM.list_part_id = {list_part_id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    

    # command to delete from build lists 
    query_string = f"DELETE FROM CONTAINS_COMPONENT WHERE CONTAINS_COMPONENT.list_part_id = {list_part_id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # loop over every part table and delete parts with this id
    output=[]
    for part_type in COMPONENT_TABLES_SYS:
        query_string = f"DELETE FROM {part_type} WHERE {part_type}.list_part_id = {list_part_id};"

        try:
            cursor.execute(query_string)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"query error: {e}")
            conn.close()
            return False
        
        if len(results) > 0:
            output = output + results
    
    # command to delete list part
    query_string = f"DELETE FROM LIST_PART WHERE LIST_PART.list_part_id = {list_part_id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    # command to delete the component base class
    query_string = f"DELETE FROM COMPONENT WHERE COMPONENT.list_part_id = {list_part_id};"
    try:
        cursor.execute(query_string)
    except sqlite3.Error as e:
        print(f"query error: {e}")
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True