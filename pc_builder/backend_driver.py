import database_api

database_api.create_tables()

"""
# TESTING OF MANUFACTURER
print(database_api.get_manufacturers())

database_api.add_manufacturer("AMC")
print(database_api.get_manufacturers())


database_api.delete_manufacturer(13)

print(database_api.get_manufacturers())
"""

"""
# testing of supplier
print(database_api.get_suppliers())

database_api.add_supplier("acme")

print(database_api.get_suppliers())

database_api.delete_supplier(5)

print(database_api.get_suppliers())

database_api.add_store_item(4, 1, 120)
database_api.add_store_item(4, 2, 120)
database_api.add_store_item(4, 3, 33)
database_api.add_store_item(4, 4, 52)
database_api.add_store_item(5, 1, 345)
database_api.add_store_item(5, 2, 54)
database_api.add_store_item(6, 3, 12)
database_api.add_store_item(6, 4, 11234)
database_api.add_store_item(7, 1, 124)
database_api.add_store_item(7, 2, 1234)

res = database_api.get_suppliers_of_part(520)
for r in res:
    print(r)
"""
"""
# testing of customer

print(database_api.get_customers())

database_api.add_customer("Art",
                           "george",
                           "Vandaley",
                           "THX1138",
                           "42 walaby way",
                           "sidny",
                           "new south whales",
                            "australia")

print(database_api.get_customers())

database_api.delete_customer(2)
print(database_api.get_customers())
"""

"""
# testing store items
print(database_api.get_suppliers())
print("before modification")
parts = database_api.get_parts_sold_by_supplier(2)
for p in parts:
    print(p)

print("\nafter modification")
database_api.add_store_item(3,2,100)
parts = database_api.get_parts_sold_by_supplier(2)
for p in parts:
    print(p)

print("\nafter deletion")
database_api.delete_store_item(6)
print(database_api.get_suppliers())
parts = database_api.get_parts_sold_by_supplier(2)
for p in parts:
    print(p)
"""
"""
print(database_api.get_customers())
database_api.create_build_list(1)
database_api.add_to_build_list(1, 2, 42)
database_api.add_to_build_list(1, 3, 43)
database_api.add_to_build_list(1, 5, 44)

database_api.add_to_build_list(2, 5, 42)
database_api.add_to_build_list(2, 6, 43)
database_api.add_to_build_list(2, 7, 44)

database_api.add_to_build_list(4, 2, 42)
database_api.add_to_build_list(1, 45, 43)
database_api.add_to_build_list(1, 5, 44)


res = database_api.display_all_build_lists()
for r in res:
    print(r)
print("\nlist 1\n")
res = database_api.get_parts_in_build_list(1)
for r in res:
    print(r)
print("\ndelete part\n")
database_api.delete_part_in_build_list(1, 3)

res = database_api.get_parts_in_build_list(1)
for r in res:
    print(r)

print("\ndelete entire list\n")
database_api.delete_build_list(2)
res = database_api.display_all_build_lists()
for r in res:
    print(r)
"""

# testing add parts
print("parts:\n")
res = database_api.get_parts_of_manufacturer(0)
res += database_api.get_parts_of_manufacturer(1)
res += database_api.get_parts_of_manufacturer(2)
res += database_api.get_parts_of_manufacturer(3)
res += database_api.get_parts_of_manufacturer(4)
for r in res:
    print(r)

database_api.delete_part(0)
database_api.delete_part(1)
database_api.delete_part(2)
database_api.delete_part(3)
database_api.delete_part(4)
database_api.delete_part(5)
database_api.delete_part(6)
database_api.delete_part(7)
database_api.delete_part(8)
database_api.delete_part(9)
database_api.delete_part(10)
database_api.delete_part(11)
database_api.delete_part(12)


print("parts:\n")
res = database_api.get_parts_of_manufacturer(0)
res += database_api.get_parts_of_manufacturer(1)
res += database_api.get_parts_of_manufacturer(2)
res += database_api.get_parts_of_manufacturer(3)
res += database_api.get_parts_of_manufacturer(4)
for r in res:
    print(r)

database_api.add_part_psu(9, "power supply", 10, False, 100, [('conn', 4,5)])
res = database_api.get_parts_of_manufacturer(9)
for r in res:
    print(r)


database_api.add_part_case(9, "case 9000", 600, 400, 600, "steel", 4,3,300, 200, 150, [(1,2,3)], [(1,2,3)], [(120, 3), (140, 2)], ["ATX", "Micro ATX"])
database_api.add_part_fan(9, "flowx4000", 3600, 29.5, 130)
database_api.add_part_ethernetcontroller(9, "vrt2290a")
database_api.add_part_motherboard(9, "X870 wifi 6", 4, "X870", 4, 1, 6, "Mini ATX", "AM5", 5, 4, [(1,2)], [(4,5)])
database_api.add_part_air_cooler(9, "breezeMAX", 32.4, 3400, 120)
database_api.add_part_liquid_cooler(9, "Arctic Cool pro III", 33.4, 3, 280, 120, 50, 3500, 300)
database_api.add_part_m2storage(9, "m2storage", 2000, 6000, 3000, "form", "4.0")
database_api.add_part_hhdstorage(9, "hhd storage", 2000, 6000, 3000, "form", "something")
database_api.add_part_satastorage(9, "sata storage", 2000, 6000, 3000, "form", "other thing")
database_api.add_part_gpu(9, "9060xt", "9000", "architecture", 3000, 4000, 16, 6, 2048, 170, 5)
database_api.add_part_ram(9, "vengence", 32, 6400, 5)
database_api.add_part_cpu(9, "9950x3d", "ryzen", "9000", 170, 4300, 5700, 1280, 16, 64, 16, 32, "zen-5", "AM5", 5)
database_api.add_part_wifimodule(9, "wifi6", 5, 4)
res = database_api.get_parts_of_manufacturer(9)
for r in res:
    print(r)

res = database_api.list_all_parts_of_type("MOTHERBOARD")
for r in res:
    print(r)