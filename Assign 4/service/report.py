from datetime import datetime, timedelta
from sqlalchemy import func, desc, asc
from datetime import datetime, timezone
from models import Order, db, Item, OrderLine, OrderStatus


class SalesReportService:

    @staticmethod
    def get_sales_total(days: int, customer_id=None) -> float:
        """
        Retrieve the total sales for a specified number of past days.
        @param customer_id: ID of the customer (optional).
        @param days: Number of days to look back, e.g., 7 days, 30 days, 365 days.
        @return: Total sales as a float.
        """
        end_date = datetime.now().astimezone()
        start_date = end_date - timedelta(days=days)

        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")

        # Query the total sales within the specified date range
        total_query = db.session.query(func.sum(Order.total_cost)) \
            .filter(Order.order_date >= start_date, Order.order_date <= end_date,
                    Order.order_status.in_([OrderStatus.PAID.value, OrderStatus.SHIPPED.value]))
        if customer_id:
            total_query = total_query.filter(Order.customer_id == customer_id)
        total_sales = total_query.scalar()
        return total_sales if total_sales else 0.0

    @staticmethod
    def get_weekly_sales(customer_id=None) -> float:
        """Retrieve total sales for the last week."""
        return SalesReportService.get_sales_total(7, customer_id)

    @staticmethod
    def get_monthly_sales(customer_id=None) -> float:
        """Retrieve total sales for the last month."""
        return SalesReportService.get_sales_total(30, customer_id)

    @staticmethod
    def get_yearly_sales(customer_id=None) -> float:
        """Retrieve total sales for the last year."""
        return SalesReportService.get_sales_total(365, customer_id)


class PopularItemReportService:

    @staticmethod
    def get_most_sold_item() -> dict:
        """Retrieve the item with the highest sales volume by quantity."""
        most_sold = db.session.query(
            Item.name, func.sum(OrderLine.quantity).label("total_quantity")
        ).join(OrderLine.item).group_by(Item.id).order_by(desc("total_quantity")).first()

        return {
            "item_name": most_sold.name,
            "total": most_sold.total_quantity
        } if most_sold else {}

    @staticmethod
    def get_highest_revenue_item() -> dict:
        """Retrieve the item with the highest total sales revenue."""
        highest_revenue = db.session.query(
            Item.name, func.sum(OrderLine.line_total).label("total_revenue")
        ).join(OrderLine.item).group_by(Item.id).order_by(desc("total_revenue")).first()

        return {
            "item_name": highest_revenue.name,
            "total": highest_revenue.total_revenue
        } if highest_revenue else {}

    @staticmethod
    def get_most_frequent_item() -> dict:
        """Retrieve the item that appears most frequently in orders."""
        most_frequent = db.session.query(
            Item.name, func.count(OrderLine.order_id).label("frequency")
        ).join(OrderLine.item).group_by(Item.id).order_by(desc("frequency")).first()

        return {
            "item_name": most_frequent.name,
            "total": most_frequent.frequency
        } if most_frequent else {}

    @staticmethod
    def get_popular_items_summary() -> dict:
        """Generate a summary of the most popular items by quantity, revenue, and frequency."""
        return {
            "most_sold_item": PopularItemReportService.get_most_sold_item(),
            "highest_revenue_item": PopularItemReportService.get_highest_revenue_item(),
            "most_frequent_item": PopularItemReportService.get_most_frequent_item()
        }

    @staticmethod
    def get_least_sold_item() -> dict:
        """Retrieve the item with the lowest sales volume by quantity."""
        least_sold = db.session.query(
            Item.name, func.sum(OrderLine.quantity).label("total_quantity")
        ).join(OrderLine.item).group_by(Item.id).order_by(asc("total_quantity")).first()

        return {
            "item_name": least_sold.name,
            "total": least_sold.total_quantity
        } if least_sold else {}

    @staticmethod
    def get_lower_revenue_item() -> dict:
        """Retrieve the item with the lowest total sales revenue."""
        lower_revenue = db.session.query(
            Item.name, func.sum(OrderLine.line_total).label("total_revenue")
        ).join(OrderLine.item).group_by(Item.id).order_by(asc("total_revenue")).first()

        return {
            "item_name": lower_revenue.name,
            "total": lower_revenue.total_revenue
        } if lower_revenue else {}

    @staticmethod
    def get_least_frequent_item() -> dict:
        """Retrieve the item that appears least frequently in orders."""
        least_frequent = db.session.query(
            Item.name, func.count(OrderLine.order_id).label("frequency")
        ).join(OrderLine.item).group_by(Item.id).order_by(asc("frequency")).first()

        return {
            "item_name": least_frequent.name,
            "total": least_frequent.frequency
        } if least_frequent else {}

    @staticmethod
    def get_least_popular_items_summary() -> dict:
        """Generate a summary of the least popular items by quantity, revenue, and frequency."""
        return {
            "least_sold_item": PopularItemReportService.get_least_sold_item(),
            "lower_revenue_item": PopularItemReportService.get_lower_revenue_item(),
            "least_frequent_item": PopularItemReportService.get_least_frequent_item()
        }
