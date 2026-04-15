#########################################################################################
# Backend file for handeling the database
#########################################################################################


## DATABASE MODIFICATION FUNCTIONS ######################################################
def manuel_query(query):
    """directly passes query to the database and returns the output"""

    return 0

def add_manufacturer(name: str) -> bool:
    """add a manufacturer to the 'MANUFACTURER' table
     returns true on success """
    
    return False
def delete_manufacturer(id: int) -> bool:
    """deletes a manufacturer from 'MANUFACTURER' table,
    Note that this may delete any related items from the tables:
    'CONTAINS_COMPONENT', 'STORE_ITEM', 'COMPONENT',
    'LIST_PART' or any part table,
    Returns true on success"""

    return False


def add_part_psu(product_name: str, power_rating: int, modular: bool, length_mm: bool, connectors) -> bool:
    """adds to tables: 'LIST_PART' and 'POWER_SUPPLY_UNIT' and 'POWER_SUPPLY_CONNECTORS' returns true on success,
    connectors is an array with tuple elements {conn_type:str, num_pins:int, count:int}"""

    return False


def add_part_case(product_name: str, height: int, width: int, len_case: int, material: str, num_35_bays: int, num_25_bays:int, max_gpu_length_mm:int, max_psu_length_mm:int,max_air_cooler_height:int, radiator_spaces, io_ports, fans)->bool:
    """adds to tables: 'LIST_PART', 'PC_CASE', 'CASE_RADIATOR_SPACE', 'CASE_IO_PORT','CASE_FITS_FAN_SIZE', 'FAN_SIZE' returns true on success
    radiator_spaces is an array with tuple elements {loc_in_case:str, height:int, width:int, len_rad:int}
    io_ports is an array with tuple elements {con_version:str, generation:str, con_type:str}
    fans is an array with tuple elements {size_mm:int, num_fans:int}"""

    return False

def add_part_fan(product_name:str, fan_rpm:int, noise_level:float, size_category_mm:int)->bool:
    """adds to tables: 'LIST_PART' and 'FAN' and 'FAN_SIZE'returns true on success'"""

    return False

def add_part_ethernetcontroller(product_name:str)->bool:
    """adds to tables: 'LIST_PART' and 'ETHERNET_CONTROLLER' returns true on success'"""

    return False

def add_part_motherboard(product_name:str, num_ram_slots:int, chipset_name:str, num_sata_conn:int, num_fan_headers:int, form_factor:str, socket_type:str, ram_type:str, eth_controller:str,io_ports, pci_slots)->bool:
    """adds to tables: 'LIST_PART', 'MOTHERBOARD', 'MOTHERBOARD_IO_PORTS', 'MOTHERBOARD_PCI_SLOT','PCI_SLOT','ETHERNET_CONTROLLER' returns true on success
    io_ports is an array with tuple elements {version:str, generation:str, con_type:str,count:int}
    pci_slots is an array with tuple elements {pci_version:str, pin_count:int, num_slots:int}'"""

    return False

def add_part_air_cooler(product_name:str, noise_level:int, fan_rpm:int, height:int)->bool:
    """adds to tables: 'LIST_PART' and 'AIR_COOLER','CPU_COOLER' returns true on success'"""

    return False

def add_part_liquid_cooler(product_name:str, noise_level:int,num_fans:int, len_cool:int, width:int, height:int, fan_rpm:int, cooling_tube_length:int)->bool:
    """adds to tables: 'LIST_PART' and 'LIQUID_COOLER','CPU_COOLER' returns true on success'"""

    return False

def add_part_m2storage(product_name:str, capacity:int, read_speed:int, write_speed:int, form_factor:str, pci_version:str)->bool:
    """adds to tables: 'LIST_PART','STORAGE', 'M2_STORAGE' returns true on success'"""

    return False

def add_part_hhdstorage(product_name:str, capacity:int, read_speed:int, write_speed:int, form_factor:str, pci_version:str)->bool:
    """adds to tables: 'LIST_PART','STORAGE', 'HHD_STORAGE' returns true on success'"""

    return False

def add_part_satastorage(product_name:str, capacity:int, read_speed:int, write_speed:int, form_factor:str, pci_version:str)->bool:
    """adds to tables: 'LIST_PART','STORAGE', 'SATA_STORAGE' returns true on success'"""

    return False


def add_part_gpu(product_name:str, series:str, architecture:str, base_clock:int, boost_clock:int, memory_size:int, memory_type:int, num_cores:int, power_cons:int, pci_version:str)->bool:
    """adds to tables: 'LIST_PART','GPU','PCI_SLOT' returns true on success'"""

    return False

def add_part_ram(product_name:str, capacity:int, max_freq:int, ram_ddr_type:int)->bool:
    """adds to tables: 'LIST_PART' and 'RAM', 'RAM_TYPE' returns true on success'"""

    return False

def add_part_cpu(product_name:str, chip_family:str, series:str, tdp:int, base_clock:int, boost_clock:int, l1_cache:int, l2_cache:int, l3_cache:int, num_cores:int, num_threads:int, architecture:str, socket_type:str, ram_ddr_type:int)->bool:
    """adds to tables: 'LIST_PART','CPU', 'RAM_TYPE', 'CPU_SOCKET_TYPE' returns true on success"""

    return False


def add_part_wifimodule(product_name:str, pci_version:str, pin_count:int)->bool:
    """adds to tables: 'LIST_PART' and 'WIFI_MODULE' and 'PCI_SLOT' returns true on success'"""

    return False



def delete_part(part_id : int, manufacturer_id : int) -> bool:
    """Deletes a part from the 'COMPONENT' table by key {part_id, manufacturer_id},
    Finds corresponding part by key {list_part_id} and deletes it from 'LIST_PART' 
    along with any components or store items 'STORE_ITEM" with the same key {list_part_id},
    Returns success or failure"""

    return False


def add_supplier(name:str)->bool:
    """add a supplier to the 'SUPPLIER' table
     returns true on success"""
    return False

def add_store_item(list_part_id:int, supplier_id:int, price:int)->bool:
    """add a store item to 'STORE_ITEM' that corresponds to part with key 'list_part_id'
    returns true on success"""

def delete_store_item(item_number : int, supplier_id : int) -> bool:
    """Deletes a part from the 'STORE_ITEM' table by key {item_number, supplier_id},
    Does not modify any other table
    Returns success or failure"""

    return False


def add_customer(first_name:str, middle_name:str, last_name:str, postal_code:str, street_no:str, city:str, province:str, country:str)->bool:
    """Add a customer to table 'CUSTOMER' returns true on success"""
    return False


def delete_customer(customer_id:int)->bool:
    """Delete a customer from table 'CUSTOMER', modifies tables 'BUILD_LIST' and 'CONTAINS_COMPONENT' returns true on success"""
    return False

def create_build_list(customer_id:int)->bool:
    """add a build list to 'BUILD_LIST' returns true on success"""

    return False

def add_to_build_list(list_id:int, list_part_id:int)->bool:
    """add a list part to a build list, modifies table 'CONTAINS_COMPONENT' returns true on success"""

    return False

## DATABASE MODIFICATION FUNCTIONS ######################################################

def get_parts_of_manufacturer(manufacturer_id:int):
    """returns a list of all the parts bellonging to a manufacturer"""
    dummy = [(0, 'part1', 'property1'),(0, 'part2', 'property2')]

    return dummy


def get_parts_sold_by_supplier(supplier_id:int):
    """returns a list of all parts sold by a supplier"""
    dummy = [(0, 'part1', 'cost1'),(0, 'part2', 'cost2')]

    return dummy

def get_parts_in_build_list(customer_id:int, build_list_id:int):
    """returns a list of all parts in a build list"""
    dummy = [(0, 'part1', 'cost1'),(0, 'part2', 'cost2')]

    return dummy

PART_TYPES=["psu", "case", "air_cooler", "liquid_cooler", "gpu", "ram", "cpu", "motherboard", "m2_storage", "sata_storage", "hhd_storage", "wifi_module"]
def list_all_parts_of_type(part_type:str):
    """returns a list of all parts of one of the types: ["psu", "case", "air_cooler", "liquid_cooler", "gpu", "ram", "cpu", "motherboard", "m2_storage", "sata_storage", "hhd_storage", "wifi_module"]"""

    dummy = [(0, 'part1', 'property1', 'height1'),
             (1, 'part2', 'property2', 'height2'),
             (2, 'part2', 'property3', 'height3')]

    return dummy

def get_compatible_part(build_list:int, customer_id:int, part_type:str):
    """returns all components of type 'part_type' that are compatible with all components in the give build list"""

    dummy = [(0, 'part1', 'property1', 'height1'),
             (1, 'part2', 'property2', 'height2'),
             (2, 'part2', 'property3', 'height3')]

    return dummy

