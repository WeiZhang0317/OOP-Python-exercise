# services/premade_box_service.py

from models.item import PremadeBox, Item, Inventory
from models import db

class PremadeBoxService:

    @staticmethod
    def get_box_by_id(box_id):
        """通过 ID 获取 Premade Box"""
        return PremadeBox.query.get(box_id)

    @staticmethod
    def get_available_items():
        """获取可以添加到 Premade Box 的所有商品"""
        # 使用 join 和 Inventory.quantity 进行过滤
        return db.session.query(Item).join(Inventory).filter(
            Item.type != 'premade_box',
            Inventory.quantity > 0
        ).all()
        
    @staticmethod
    def get_items_by_ids(item_ids):
        """通过 ID 列表获取多个商品"""
        return Item.query.filter(Item.id.in_(item_ids)).all()
    
    @staticmethod
    def customize_box(box: PremadeBox, selected_items: list, quantities: list):
        """
        定制 Premade Box，添加蔬菜到箱子中。

        :param box: PremadeBox 对象
        :param selected_items: 用户选择的商品列表
        :param quantities: 每个商品对应的数量
        :raises ValueError: 如果超过了箱子的容量限制
        """
        total_quantity = sum(quantities)
        
        # 检查总数量是否超过箱子的最大容量
        if total_quantity > box.max_content:
            raise ValueError(f"Total items exceed the box limit! Maximum allowed: {box.max_content}")

        # 清空当前的箱子内容
        box.box_content = []

        # 添加新内容
        for item, qty in zip(selected_items, quantities):
            if qty > 0:
                for _ in range(qty):
                    if len(box.box_content) >= box.max_content:
                        raise ValueError(f"The {box.box_size} box can only contain {box.max_content} items.")
                    box.add_items_to_box(item, qty)

        # 保存到数据库
        db.session.commit()
    
    @staticmethod
    def get_box_details(box: PremadeBox):
        """
        获取 Premade Box 的详细信息，包括当前的内容。

        :param box: PremadeBox 对象
        :return: 箱子内的物品信息
        """
        return box.get_box_details()

    @staticmethod
    def remove_item_from_box(session, item_id):
        """从 Premade Box 中移除商品"""
        premade_box = session.get('premade_box', [])
        session['premade_box'] = [item for item in premade_box if item['item_id'] != item_id]
