"""Database models."""
from .. import db

class Simulation(db.Model):
    """Manage Simulation references."""
    __tablename__ = 'simulations'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    sim_name = db.Column(
        db.String(100),
        nullable=True,
        unique=True
    )
    days = db.Column(
        db.Integer,
        nullable=False,
        default=30,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    active = db.Column(
            db.Boolean,
            default=True
    )
    amms = db.relationship('AMM',
                            backref='simulation',
                            lazy=True)
    # markets = db.relationship('Market',
    #                         backref='simulation',
    #                         lazy=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.address,
            'user_id': self.user_id,
            'amms': len(self.amms)
            }



# class SimSettings(db.Model):
#     __tablename__ = 'sim_settings'
#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )
#     seed_ = db.Column(
#         db.Integer,
#         primary_key=True
#     )
