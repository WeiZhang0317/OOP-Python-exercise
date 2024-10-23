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
        return db.session.query(Item).join(Item.inventory).filter(
            Item.type != 'premade_box',
            Inventory.quantity > 0
        ).all()

    @staticmethod
    def get_items_by_ids(item_ids):
        """通过 ID 列表获取多个商品"""
        return Item.query.filter(Item.id.in_(item_ids)).all()

    @staticmethod
    def customize_box(box, selected_items, quantities):
        """自定义 Premade Box，添加商品"""
        total_quantity = sum(quantities)
        if total_quantity > box.max_content:
            raise ValueError(f"Total items exceed the box limit! Maximum allowed: {box.max_content}")

        box.box_content = []  # 清空箱子
        for item, qty in zip(selected_items, quantities):
            box.add_content(item, qty)

        db.session.commit()  # 提交更改到数据库
        
    @staticmethod
    def remove_item_from_box(session, item_id):
        """从 Premade Box 中移除商品"""
        premade_box = session.get('premade_box', [])
        updated_box = [item for item in premade_box if item['item_id'] != item_id]
        session['premade_box'] = updated_box    
