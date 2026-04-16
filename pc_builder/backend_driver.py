import database_api


def run_demo():
    # WARNING:
    # This resets the whole database every time you run this file directly.
    # Do NOT call this from Django views or on import.
    database_api.create_tables()

    print("Initial parts:")
    for manufacturer_id in range(0, 13):
        rows = database_api.get_parts_of_manufacturer(manufacturer_id)
        if rows:
            for row in rows:
                print(row)

    print("\nDeleting a few parts...")
    for list_part_id in [1, 2, 3]:
        ok = database_api.delete_part(list_part_id)
        print(f"delete_part({list_part_id}) -> {ok}")

    print("\nAfter deletion:")
    for manufacturer_id in range(0, 13):
        rows = database_api.get_parts_of_manufacturer(manufacturer_id)
        if rows:
            for row in rows:
                print(row)

    print("\nAdding new PSU...")
    ok = database_api.add_part_psu(
        manufacturer_id=9,
        product_name="power supply",
        power_rating=10,
        modular=False,
        length_mm=100,
        connectors=[("conn", 4, 5)],
    )
    print("add_part_psu ->", ok)

    print("\nManufacturer 9 parts:")
    rows = database_api.get_parts_of_manufacturer(9)
    if rows:
        for row in rows:
            print(row)

    print("\nSuppliers:")
    print(database_api.get_suppliers())

    print("\nCustomers:")
    print(database_api.get_customers())

    print("\nAll build lists:")
    print(database_api.display_all_build_lists())


if __name__ == "__main__":
    run_demo()