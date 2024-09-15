import os
from controller import Company
from views import Application

def load_customers(company, filepath):
    """Load customer data from a file and add each customer to the company."""
    with open(filepath, 'r') as file:
        for line in file:
            name = line.strip()
            if name:
                company.create_customer(name)
    # Print out the loaded customer names for verification
    print(f"Loaded customers: {[customer.customerName for customer in company.customers]}")  

def load_products(company, filepath):
    """Load product data from a file and add each product to the company."""
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip():
                # Split the line by the last comma into product name and price
                name, price = line.strip().rsplit(',', 1)
                company.create_product(name.strip(), float(price.strip()))
    # Print out the loaded product names for verification
    print(f"Loaded products: {[product.productName for product in company.products]}")  


def main():
    # Initialize the company with a given name
    company = Company("Lincoln Office Supplies")

    # Get the base directory where the customer and product files are located
    base_dir = os.path.dirname(__file__)
    customer_file = os.path.join(base_dir, 'data', 'customer.txt')
    product_file = os.path.join(base_dir, 'data', 'product.txt')

    # Load customer and product data into the company
    load_customers(company, customer_file)
    load_products(company, product_file)

    # Create an instance of the Application (GUI)
    app = Application()

    # Pass the company object to the application
    app.company = company

    # Update the customer and product lists in the GUI based on the loaded data
    app.update_customer_list()
    app.update_product_list()

    # Start the Tkinter main event loop to run the application
    app.mainloop()


if __name__ == "__main__":
    # Execute the main function when the script is run directly
    main()
