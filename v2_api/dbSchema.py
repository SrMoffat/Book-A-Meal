from app import ma
from mealModel import Menu


class MealSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'category', 'price', 'image_url',
                  'description', 'date_posted', '_links')

    _links = ma.HyperLinks({
        'self': ma.URLFor('v2_api.mealModel', meal_id='<id>', _external=True),
        'collection': ma.URLFor('v2_api.mealModel', _external=True)
    })


class MenuSchema(ma.Schema):
    class Meta:
        fields = ('id', 'meal', 'date')

    meal = ma.Nested(MealSchema)


class OrdersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'meals', 'time_ordered', 'delivered')

    meals = ma.List(ma.Nested(MealSchema))

    meal_schema = MealSchema()
    meals_schema = MealSchema(many=True)

    menu_schema = MenuSchema(many=True)
    menus_schema = MenuSchema(many=True)

    order_schema = OrdersSchema()
    orders_schema = OrdersSchema(many=True)
