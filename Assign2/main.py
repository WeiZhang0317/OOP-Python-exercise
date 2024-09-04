import os
from controller import Company
from views import Application

def load_customers(company, filepath):
    """Load customers from a file and add them to the company."""
    with open(filepath, 'r') as file:
        for line in file:
            name = line.strip()
            if name:
                company.create_customer(name)
    print(f"Loaded customers: {[customer.customerName for customer in company.customers]}")  

def load_products(company, filepath):
    """Load products from a file and add them to the company."""
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip():
                name, price = line.strip().rsplit(',', 1)
                company.create_product(name.strip(), float(price.strip()))
    print(f"Loaded products: {[product.productName for product in company.products]}")  


def main():
    company = Company("Lincoln Office Supplies")

    base_dir = os.path.dirname(__file__)
    customer_file = os.path.join(base_dir, 'data', 'customer.txt')
    product_file = os.path.join(base_dir, 'data', 'product.txt')

    load_customers(company, customer_file)
    load_products(company, product_file)

   
    app = Application()
    

    app.company = company

    app.update_customer_list()
    app.update_product_list()

    app.mainloop()


if __name__ == "__main__":
    main()
