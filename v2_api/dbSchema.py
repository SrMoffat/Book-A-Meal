from app import ma
from v2_api.mealModel import Menu


class MealSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'category', 'price', 'image_url',
                  'description', 'date_posted', '_links')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('v2_api.mealModel', meal_id='<id>', _external=True),
        'collection': ma.URLFor('v2_api.mealModel', _external=True)
    })


class MenuSchema(ma.Schema):
    class Meta:
        fields = ('id', 'meal', 'date')

    meal = ma.Nested(MealSchema)


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'meals', 'time_ordered', 'delivered')

    meals = ma.List(ma.Nested(MealSchema))


meal_schema = MealSchema()
meals_schema = MealSchema(many=True)

menu_schema = MenuSchema(many=True)
menus_schema = MenuSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
