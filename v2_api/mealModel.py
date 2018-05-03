from datetime import datetime
from userModel import db


class Meal(db.Model):
    """The model for a meal
    """
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(128))
    description = db.Column(db.String)
    caterer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    caterer = db.relationship('User',
                              backref=db.backref('meals', lazy=True))
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)

    def save(self):
        """Save and commit meal to storage
        """
        db.session.add(self)
        db.session.commit()

    order_meals = db.Table('order_meals',
                           db.Column('order_id', db.Integer,
                                     db.ForeignKey('orders.id')),
                           db.Column('meal_id', db.Integer,
                                     db.ForeignKey('meal.id')),
                           db.Column('quantity', db.Integer, default=1))


class Order(db.Model):
    """The model for an order
    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('orders', lazy=True))
    meals = db.relationship('Meal',
                            secondary=order_meals,
                            lazy='subquery',
                            backref=db.backref('orders', lazy=True))

    time_ordered = db.Column(db.DateTime,
                             nullable=False,
                             default=datetime.utcnow
                             )
    delivered = db.Column(db.Boolean, default=False)

    def save(self):
        """Save and commit order to storage
        """
        db.session.add(self)
        db.session.commit()


class Menu(db.Model):
    """The model for a menu
    """
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))

    # Owner
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    meal = db.relationship('Meal')
    day = db.Column(db.Date,
                    nullable=False,
                    default=datetime.today())

    date_created = db.Column(db.Date,
                             nullable=False,
                             default=datetime.utcnow)
