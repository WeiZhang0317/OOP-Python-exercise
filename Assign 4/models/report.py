from typing import List, Dict
from datetime import datetime


class Report:
    """!
    Generates various reports for the company, including sales, customer, and item popularity reports.
    """

    def __init__(self, report_data: Dict[str, List[Dict[str, any]]]) -> None:
        """!
        Constructor for the Report class.

        Initializes the report data that will be used for generating different reports.

        @param report_data: A dictionary containing all the data required for report generation.
                            Expected keys: 'sales', 'customers', 'items'.
        """
        self.report_data = report_data  # Internal data used for report generation

    def validate_report_data(self) -> bool:
        """!
        Validates the report data structure to ensure required keys and data are present.

        @return: True if the data is valid, otherwise False.
        """
        required_keys = {'sales', 'customers', 'items'}
        if not all(key in self.report_data for key in required_keys):
            print(f"Missing one or more required keys in report data: {required_keys - self.report_data.keys()}")
            return False
        return True

    def generate_sales_report(self, time_period: str) -> str:
        """!
        Generates a sales report for the specified time period (e.g., week, month, year).
        This method filters the report data based on the time period.

        @param time_period: The time period for the report (e.g., "week", "month", "year").
        @return: A string representing the sales report.
        """
        if not self.validate_report_data():
            return "Invalid report data."

        # Sample logic: Calculate total sales for the given time period
        total_sales = self.calculate_total_sales(time_period)

        report = f"Sales Report for {time_period}:\nTotal Sales: ${total_sales:.2f}\n"
        print(report)
        return report

    def calculate_total_sales(self, time_period: str) -> float:
        """!
        Calculates total sales based on the time period.

        @param time_period: The time period for which to calculate sales (e.g., "week", "month", "year").
        @return: A float representing the total sales amount.
        """
        total_sales = 0.0
        sales_data = self.report_data.get('sales', [])

        # Example filtering based on time period (adjust according to actual data structure)
        for sale in sales_data:
            sale_date = datetime.strptime(sale.get('date'), '%Y-%m-%d')
            if self.is_date_in_period(sale_date, time_period):
                total_sales += sale.get('amount', 0.0)

        return total_sales

    def is_date_in_period(self, date: datetime, time_period: str) -> bool:
        """!
        Checks if the provided date falls within the specified time period.

        @param date: The datetime object representing the date to check.
        @param time_period: The time period to check against (e.g., "week", "month", "year").
        @return: True if the date is within the period, otherwise False.
        """
        now = datetime.now()
        if time_period == "week":
            return date.isocalendar()[1] == now.isocalendar()[1]  # Check if same week of the year
        elif time_period == "month":
            return date.month == now.month and date.year == now.year  # Check if same month and year
        elif time_period == "year":
            return date.year == now.year  # Check if same year
        return False

    def generate_customer_report(self) -> str:
        """!
        Generates a report of all private and corporate customers.
        This method compiles and returns a list of customers.

        @return: A string representing the customer report.
        """
        if not self.validate_report_data():
            return "Invalid report data."

        customer_data = self.report_data.get('customers', [])
        private_customers = [c for c in customer_data if c.get('type') == 'private']
        corporate_customers = [c for c in customer_data if c.get('type') == 'corporate']

        report = (f"Customer Report:\n"
                  f"Private Customers: {len(private_customers)}\n"
                  f"Corporate Customers: {len(corporate_customers)}\n"
                  f"Total Customers: {len(customer_data)}\n")

        print(report)
        return report

    def generate_item_popularity_report(self) -> str:
        """!
        Generates a report on the most and least popular items.
        This method analyzes item data to rank items by popularity.

        @return: A string representing the item popularity report.
        """
        if not self.validate_report_data():
            return "Invalid report data."

        most_popular, least_popular = self.get_most_least_popular_items()

        report = (f"Item Popularity Report:\n"
                  f"Most Popular Item: {most_popular}\n"
                  f"Least Popular Item: {least_popular}\n")
        print(report)
        return report

    def get_most_least_popular_items(self) -> (str, str):
        """!
        Analyzes the item data to determine the most and least popular items.

        @return: A tuple containing the names of the most popular and least popular items.
        """
        items_data = self.report_data.get('items', [])
        if not items_data:
            return "No data", "No data"

        # Calculate popularity (e.g., number of sales or total quantity sold)
        item_sales = {item['name']: item.get('quantity_sold', 0) for item in items_data}

        most_popular_item = max(item_sales, key=item_sales.get)
        least_popular_item = min(item_sales, key=item_sales.get)

        return most_popular_item, least_popular_item
