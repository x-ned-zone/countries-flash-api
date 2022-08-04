# Country API application:

from flask import Flask
from flask_restful import Api
from Country import Country
from CountryModel import CountryModel


def create_app():
    api = Api()
    # register country resources as endpoints / accessible api.
    api.add_resource(Country, "/country/<string:request>")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Country.db'
    api.init_app(app)
    CountryModel.init_app(app)

    return app


def main():
    flaskApp = create_app()
    # db.create_all(app=flaskApp)
    flaskApp.run(debug=True)


if __name__ == "__main__":
    main()
