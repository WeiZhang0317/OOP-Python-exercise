import tkinter as tk
from tkinter import messagebox, ttk
from controller import Company

import tkinter as tk

class ToolTip:
    def __init__(self, widget, text, bg="#ffffe0", fg="black", font=("Arial", 10, "normal"), wraplength=150):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.font = font
        self.wraplength = wraplength
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, 
            text=self.text, 
            justify='left', 
            background=self.bg, 
            foreground=self.fg, 
            relief=tk.SOLID, 
            borderwidth=1,
            font=self.font, 
            wraplength=self.wraplength
        )
        label.pack(ipadx=5, ipady=5)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lincoln Office Supplies Order App")
        self.geometry("800x600")
        
        # Create an instance of Company
        self.company = None

        # UI Components
        self.create_widgets()
    



    def create_widgets(self):
        # Customer Information Frame
        tk.Label(self, text="Customer Information", font=('Helvetica', 14, 'bold')).pack(pady=10)
        customer_info_frame = tk.Frame(self, bd=2, relief="groove")
        customer_info_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(customer_info_frame, text="Select Customer:").grid(row=0, column=0)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(customer_info_frame, textvariable=self.customer_var, state="readonly")
            
        self.customer_combo.grid(row=0, column=1)
  
        # Adding tooltip for customer combobox

        self.customer_combo_tooltip = ToolTip(self.customer_combo, text="Select a customer and click on 'New Order' button")

        
        self.customer_combo.bind("<<ComboboxSelected>>", self.display_customer_info)

        self.customer_info_text = tk.Text(customer_info_frame, height=4, width=50)
        self.customer_info_text.grid(row=0, column=2, padx=10)
        self.update_customer_list()

        tk.Button(customer_info_frame, text="New Order", command=self.create_order).grid(row=0, column=3)

        # Process Order Frame
        tk.Label(self, text="Process Order", font=('Helvetica', 14, 'bold')).pack(pady=10)
        process_order_frame = tk.Frame(self, bd=2, relief="groove")
        process_order_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(process_order_frame, text="Select Product:").grid(row=0, column=0)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(process_order_frame, textvariable=self.product_var, state="readonly")
        self.product_combo.grid(row=0, column=1)
        # Adding tooltip for product combobox
        self.product_combo_tooltip = ToolTip(self.product_combo, text="Select a product and its quantity, then click on 'Add Product'button.")
        self.update_product_list()

      
        tk.Label(process_order_frame, text="Quantity:").grid(row=0, column=2)
        self.quantity_var = tk.StringVar(value="1")  # default is 1
        self.quantity_combo = ttk.Combobox(process_order_frame, textvariable=self.quantity_var, state="readonly")
        self.quantity_combo['values'] = [str(i) for i in range(1, 1001)] 
        self.quantity_combo.grid(row=0, column=3)


        tk.Button(process_order_frame, text="Add Product", command=self.add_order_item).grid(row=0, column=4)

        # Order Details Frame
        tk.Label(self, text="Order Details", font=('Helvetica', 14, 'bold')).pack(pady=10)
        order_details_frame = tk.Frame(self, bd=2, relief="groove")
        order_details_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        self.order_details_text = tk.Text(order_details_frame, height=10)
        self.order_details_text.pack(fill=tk.BOTH, expand=True)

        # Subtotal Frame
        subtotal_frame = tk.Frame(order_details_frame, bg="white", relief=tk.SOLID, borderwidth=1)
        subtotal_frame.pack(fill=tk.X, pady=5)

        # Subtotal Label
        self.subtotal_var = tk.StringVar(value="Subtotal: $0.00")
        self.subtotal_label = tk.Label(subtotal_frame, textvariable=self.subtotal_var, bg="white", font=("Arial", 10, "bold"))
        self.subtotal_label.pack(padx=10, pady=10)

        tk.Button(order_details_frame, text="Submit Order", command=self.submit_order).pack(pady=5)

        # Process Payment Frame
        tk.Label(self, text="Process Payment", font=('Helvetica', 14, 'bold')).pack(pady=10)
        process_payment_frame = tk.Frame(self, bd=2, relief="groove")
        process_payment_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(process_payment_frame, text="Payment Amount:").grid(row=0, column=0)
        self.payment_var =  tk.StringVar()
 
        tk.Entry(process_payment_frame, textvariable=self.payment_var).grid(row=0, column=1)


        tk.Button(process_payment_frame, text="Pay", command=self.create_payment).grid(row=0, column=2)
    
        # Reports Frame
        reports_frame = tk.Frame(self)
        reports_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(reports_frame, text="List Customer Orders", command=self.list_customer_orders).grid(row=0, column=0)
        tk.Button(reports_frame, text="List Customer Payments", command=self.list_customer_payments).grid(row=0, column=1)
        tk.Button(reports_frame, text="List All Customers", command=self.list_all_customers).grid(row=0, column=2)
        tk.Button(reports_frame, text="List All Orders", command=self.list_all_orders).grid(row=0, column=3)
        tk.Button(reports_frame, text="List All Payments", command=self.list_all_payments).grid(row=0, column=4)

    def update_customer_list(self):
        if self.company:
            customers = [customer.customerName for customer in self.company.get_all_customers()]
            self.customer_combo['values'] = customers
            print(f"Customers in dropdown: {customers}")
        else:
            print("self.company is None in update_customer_list")

    def update_product_list(self):
        if self.company:
            products = [product.productName for product in self.company.products]
            self.product_combo['values'] = products
            print(f"Products in dropdown: {products}")
        else:
            print("self.company is None in update_product_list")

    def display_customer_info(self, event):
        selected_customer_name = self.customer_var.get()
        customer = self.company.find_customer(selected_customer_name)
        if customer:
            self.customer_info_text.delete(1.0, tk.END)
            self.customer_info_text.insert(tk.END, f"Customer ID: {customer.customerID}\n")
            self.customer_info_text.insert(tk.END, f"Customer Name: {customer.customerName}\n")
            self.customer_info_text.insert(tk.END, f"Balance: ${customer.customerBalance:.2f}\n")

    def create_order(self):
        selected_customer_name = self.customer_var.get()
        if not selected_customer_name:
            messagebox.showerror("Error", "Please select a customer to create an order")
            return
        customer = self.company.find_customer(selected_customer_name)
        if customer:
            self.current_order = self.company.create_order(customer)
            self.order_details_text.delete(1.0, tk.END)
            self.order_details_text.insert(tk.END, f"Order for {customer.customerName}\n")

    def add_order_item(self):
   
        if not self.product_var.get():
            messagebox.showerror("Error", "Please select a product")
            return
        if not hasattr(self, 'current_order'):
            messagebox.showerror("Error", "Please create an order for the customer first")
            return
        product_name = self.product_var.get()
        quantity = int(self.quantity_var.get())
        if hasattr(self, 'current_order'):
            self.company.add_order_item(self.current_order, product_name, quantity)
            product = self.company.find_product(product_name)
            self.order_details_text.insert(tk.END, f"{product.productName} x {quantity} = ${product.productPrice * quantity:.2f}\n")
            subtotal = self.current_order.calculate_subtotal()
            self.subtotal_var.set(f"Subtotal: ${subtotal:.2f}")
        else:
            messagebox.showerror("Error", "No order started. Please create an order first.")

    def submit_order(self):
        if hasattr(self, 'current_order'):
            self.company.submit_order(self.current_order)
            messagebox.showinfo("Order Submitted", "The order has been submitted successfully!")
            self.display_customer_info(None)  # Update customer balance
        else:
            messagebox.showerror("Error", "No order to submit.")

    def create_payment(self):
        selected_customer_name = self.customer_var.get()
        customer = self.company.find_customer(selected_customer_name)
        amount = self.payment_var.get()
        try:
            amount = float(amount)
            if customer and amount > 0:
                self.company.create_payment(customer, amount)
                messagebox.showinfo("Payment Processed", "Payment has been processed successfully!")
                self.display_customer_info(None)  # Update customer balance
            else:
                messagebox.showerror("Error", "Invalid payment amount or customer.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            
    def list_customer_orders(self):
        selected_customer_name = self.customer_var.get()
        customer = self.company.find_customer(selected_customer_name)
        if customer:
            orders = customer.orders
            self.show_list("Customer Orders", orders)
        else:
            messagebox.showerror("Error", "Customer not found.")

    def list_customer_payments(self):
        selected_customer_name = self.customer_var.get()
        customer = self.company.find_customer(selected_customer_name)
        if customer:
            payments = customer.payments
            self.show_list("Customer Payments", payments)
        else:
            messagebox.showerror("Error", "Customer not found.")

    def list_all_customers(self):
        customers = self.company.get_all_customers()
        self.show_list("All Customers", customers)

    def list_all_orders(self):
        orders = self.company.get_all_orders()
        self.show_list("All Orders", orders)

    def list_all_payments(self):
        payments = self.company.get_all_payments()
        self.show_list("All Payments", payments)

    def show_list(self, title, items):
        list_window = tk.Toplevel(self)
        list_window.title(title)
        list_text = tk.Text(list_window, height=20, width=50)
        list_text.pack(fill=tk.BOTH, expand=True)
        for item in items:
            list_text.insert(tk.END, str(item) + "\n")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
