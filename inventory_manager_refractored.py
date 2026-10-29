import json
import os
from product import Product
from inventory import Inventory

FILE_NAME = "inventory.json"


def load_inventory(inventory_obj):
    """Loads inventory from JSON file if present; otherwise loads default products."""
    if os.path.exists(FILE_NAME):
        print(f"{FILE_NAME} found.")
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                for item in data:
                    # Reconstruct Product objects from stored dictionary data
                    prod = Product(item["id"], item["name"], item["price"], item["stock"])
                    inventory_obj.add_product(prod)
            print("Inventory loaded successfully.\n")
        except Exception as e:
            print(f"Error loading {FILE_NAME}: {e}. Loading default data.\n")
            load_default_data(inventory_obj)
    else:
        print(f"{FILE_NAME} not found. Creating new inventory...\n")
        load_default_data(inventory_obj)
        save_inventory(inventory_obj)


def load_default_data(inventory_obj):
    """Loads default product objects into the inventory."""
    default_products = [
        Product("8001", "Sweet Madame", "$9.50", 1659),
        Product("8002", "Lavender Melon", "$8.00", 11),
        Product("8003", "Ghost Pie", "$15.00", 3172),
        Product("8004", "Beetle Soup", "$5.00", 456),
        Product("8005", "The Flood", "$3.43", 343),
    ]
    for prod in default_products:
        inventory_obj.add_product(prod)


def save_inventory(inventory_obj):
    """Saves the current inventory collection to inventory.json."""
    data = []
    for prod in inventory_obj.products:
        data.append({
            "id": prod._product_id,
            "name": prod.name,
            "price": prod._price,
            "stock": prod.stock
        })
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def add_product_workflow(inventory_obj):
    """Handles user input and creates a new Product object to add to inventory."""
    # Auto-generate next ID based on highest current numeric ID
    max_id = 8000
    for prod in inventory_obj.products:
        try:
            prod_num = int(prod._product_id)
            if prod_num > max_id:
                max_id = prod_num
        except ValueError:
            pass
    new_id = str(max_id + 1)

    while True:
        name = input("Enter product name: ").strip()
        if not name:
            print("Error: Product name cannot be empty. Please try again.")
        elif name.isdigit():
            print("Error: Product name cannot be just numbers. Please enter a valid name.")
        else:
            break

    while True:
        price_input = input("Enter product price ($): ").strip()
        try:
            price_val = float(price_input)
            if price_val <= 0:
                print("Error: Price must be greater than $0.00. Please try again.")
            else:
                price = f"${price_val:.2f}"
                break
        except ValueError:
            print("Error: Invalid price. Please enter a valid decimal number (e.g., 9.99).")

    while True:
        stock_input = input("Enter initial stock: ").strip()
        if stock_input.isdigit():
            stock = int(stock_input)
            break
        print("Error: Invalid stock amount. Please enter a valid integer.")

    # Create a new Product instance and add it via the Inventory object
    new_product = Product(new_id, name, price, stock)
    inventory_obj.add_product(new_product)
    print(f"Product '{name}' added successfully with ID: {new_id}.\n")


def update_stock_workflow(inventory_obj):
    """Finds a product by ID and updates its stock using its internal method."""
    prod_id = input("Enter product ID to update: ").strip()
    for prod in inventory_obj.products:
        if prod._product_id == prod_id:
            try:
                added_stock = int(input(f"Enter stock to add for {prod.name}: "))
                if added_stock < 0:
                    print("Stock cannot be negative.\n")
                    return
                # Utilizing encapsulation: calling the product's own method to manage state
                prod.update_stock(added_stock)
                print()
                return
            except ValueError:
                print("Invalid stock number.\n")
                return
    print("Product ID not found.\n")


def print_menu():
    print("---------------- MENU ----------------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------------------")


def main():
    print("=========================================")
    print("OOP INVENTORY MANAGEMENT SYSTEM")
    print("=========================================\n")

    # Initialize the Inventory object (manages the collection)
    my_inventory = Inventory()
    load_inventory(my_inventory)

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            print()
            my_inventory.display_all()
            print()
        elif choice == "2":
            print()
            add_product_workflow(my_inventory)
        elif choice == "3":
            print()
            update_stock_workflow(my_inventory)
        elif choice == "4":
            print()
            query = input("Enter Product ID or Name to search: ")
            my_inventory.search_product(query)
            print()
        elif choice == "5":
            save_inventory(my_inventory)
            print("Inventory saved to inventory.json.\n")
        elif choice == "6":
            save_inventory(my_inventory)
            print("Saving inventory before exit...\nInventory saved successfully!")
            print("Thank you for using the Inventory Management System")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.\n")


if __name__ == "__main__":
    main()