"""Database models."""
from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..simulator.models import Simulation

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    simulations = db.relationship('Simulation',
                            backref='user',
                            lazy=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def active_sim(self):
        return Simulation.query.filter_by(active=True).first()

    def __repr__(self):
        return '<User {}>'.format(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.address,
            'addresses': len(addresses),
            }
