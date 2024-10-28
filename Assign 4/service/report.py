from datetime import datetime, timedelta
from sqlalchemy import func, desc, asc
from datetime import datetime, timezone
from models import Order, db, Item, OrderLine, OrderStatus


class SalesReportService:

    @staticmethod
    def get_sales_total(days: int, customer_id=None) -> float:
        """
        获取过去指定天数的总销售额。
        @param customer_id: 用户id。
        @param days: 查询的天数，例如7天，30天，365天。
        @return: 总销售额，float类型。
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)

        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")

        # 查询指定时间区间内的总销售额
        total_query = db.session.query(func.sum(Order.total_cost)) \
            .filter(Order.order_date >= start_date, Order.order_date <= end_date,
                    Order.order_status == OrderStatus.PAID)
        if customer_id:
            total_query = total_query.filter(Order.customer_id == customer_id)
        total_sales = total_query.scalar()
        return total_sales if total_sales else 0.0

    @staticmethod
    def get_weekly_sales(customer_id=None) -> float:
        """
        获取最近一周的总销售额。
        @return: 一周的总销售额。
        """
        return SalesReportService.get_sales_total(7, customer_id)

    @staticmethod
    def get_monthly_sales(customer_id=None) -> float:
        """
        获取最近一个月的总销售额。
        @return: 一个月的总销售额。
        """
        return SalesReportService.get_sales_total(30, customer_id)

    @staticmethod
    def get_yearly_sales(customer_id=None) -> float:
        """
        获取最近一年的总销售额。
        @return: 一年的总销售额。
        """
        return SalesReportService.get_sales_total(365, customer_id)


class PopularItemReportService:

    @staticmethod
    def get_most_sold_item() -> dict:
        """
        按销售数量获取最受欢迎的商品。
        @return: 字典，包含商品名称及销售总数量。
        """
        most_sold = db.session.query(
            Item.name, func.sum(OrderLine.quantity).label("total_quantity")
        ).join(OrderLine.item).group_by(Item.id).order_by(desc("total_quantity")).first()

        return {
            "item_name": most_sold.name,
            "total": most_sold.total_quantity
        } if most_sold else {}

    @staticmethod
    def get_highest_revenue_item() -> dict:
        """
        按销售金额获取最受欢迎的商品。
        @return: 字典，包含商品名称及总销售金额。
        """
        highest_revenue = db.session.query(
            Item.name, func.sum(OrderLine.line_total).label("total_revenue")
        ).join(OrderLine.item).group_by(Item.id).order_by(desc("total_revenue")).first()

        return {
            "item_name": highest_revenue.name,
            "total": highest_revenue.total_revenue
        } if highest_revenue else {}

    @staticmethod
    def get_most_frequent_item() -> dict:
        """
        按购买频次获取最受欢迎的商品。
        @return: 字典，包含商品名称及订单出现次数。
        """
        most_frequent = db.session.query(
            Item.name, func.count(OrderLine.order_id).label("frequency")
        ).join(OrderLine.item).group_by(Item.id).order_by(desc("frequency")).first()

        return {
            "item_name": most_frequent.name,
            "total": most_frequent.frequency
        } if most_frequent else {}

    @staticmethod
    def get_popular_items_summary() -> dict:
        """
        综合获取最受欢迎的商品的分析结果。
        @return: 一个字典，包含销量最高、销售额最高和购买频次最高的商品信息。
        """
        return {
            "most_sold_item": PopularItemReportService.get_most_sold_item(),
            "highest_revenue_item": PopularItemReportService.get_highest_revenue_item(),
            "most_frequent_item": PopularItemReportService.get_most_frequent_item()
        }

    @staticmethod
    def get_least_sold_item() -> dict:
        """
        按销售数量获取最不受欢迎的商品。
        @return: 字典，包含商品名称及销售总数量。
        """
        most_sold = db.session.query(
            Item.name, func.sum(OrderLine.quantity).label("total_quantity")
        ).join(OrderLine.item).group_by(Item.id).order_by(asc("total_quantity")).first()

        return {
            "item_name": most_sold.name,
            "total": most_sold.total_quantity
        } if most_sold else {}

    @staticmethod
    def get_lower_revenue_item() -> dict:
        """
        按销售金额获取最不受欢迎的商品。
        @return: 字典，包含商品名称及总销售金额。
        """
        highest_revenue = db.session.query(
            Item.name, func.sum(OrderLine.line_total).label("total_revenue")
        ).join(OrderLine.item).group_by(Item.id).order_by(asc("total_revenue")).first()

        return {
            "item_name": highest_revenue.name,
            "total": highest_revenue.total_revenue
        } if highest_revenue else {}

    @staticmethod
    def get_least_frequent_item() -> dict:
        """
        按购买频次获取最受不欢迎的商品。
        @return: 字典，包含商品名称及订单出现次数。
        """
        most_frequent = db.session.query(
            Item.name, func.count(OrderLine.order_id).label("frequency")
        ).join(OrderLine.item).group_by(Item.id).order_by(asc("frequency")).first()

        return {
            "item_name": most_frequent.name,
            "total": most_frequent.frequency
        } if most_frequent else {}

    @staticmethod
    def get_least_popular_items_summary() -> dict:
        """
        综合获取最受欢迎的商品的分析结果。
        @return: 一个字典，包含销量最高、销售额最高和购买频次最高的商品信息。
        """
        return {
            "least_sold_item": PopularItemReportService.get_least_sold_item(),
            "lower_revenue_item": PopularItemReportService.get_lower_revenue_item(),
            "least_frequent_item": PopularItemReportService.get_least_frequent_item()
        }
