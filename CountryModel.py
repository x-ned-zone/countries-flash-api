from flask_sqlalchemy import SQLAlchemy
# from CountryService import CountryService

db = SQLAlchemy()

# Entity class (POPO): Country information storage and ORM.


class CountryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    alpha2code = db.Column(db.String(2), nullable=False)
    alpha3code = db.Column(db.String(3), nullable=False)
    currency = db.Column(db.String(30), nullable=False)
    active = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Country(name={self.name}, alpha2code={self.alpha2code}, \
				alpha3code={self.alpha3code}, currency={self.currency}, active = {self.active})"

    def init_app(app):
        db.init_app(app)
        db.create_all(app=app)

    def add(country):
        db.session.add(country)

    def delete(country):
        db.session.delete(country)

    def commit():
        db.session.commit()
