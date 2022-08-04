from flask_restful import abort
from CountryModel import CountryModel

# REST microservice: Process API controller requests.
# Receives requests, performs all the logic, and produces responses with status code.


class CountryService:
    def get(self, request):
        if request == "all":
            country_list = CountryModel.query.filter_by(active=1).all()
        elif request.isnumeric():
            country_list = CountryModel.query.filter_by(
                id=request, active=1).all()
        else:
            country_list = CountryModel.query.filter_by(
                currency=request, active=1).all()
        if not country_list:
            abort(404, message=f"Fetching: No countries exist!")

        return country_list, 200

    def add(self, id, params):
        if not CountryModel.query.filter_by(id=id, active=1).first():
            country = CountryModel(id=id, name=params["name"],
                                   alpha2code=params["alpha2code"],
                                   alpha3code=params["alpha3code"],
                                   currency=params["currency"],
                                   active=1)
            CountryModel.add(country)
            CountryModel.commit()
        elif CountryModel.query.filter_by(id=id, active=0).first():
            self.update(id, params)
        else:
            abort(
                406, message=f"Creating: Country with this id='{id}' already exists!")
        return country, 201

    def update(self, id, params):
        country = CountryModel.query.filter_by(id=id).first()
        if country:
            if params["name"] is not None:
                country.name = params["name"]
            if params["alpha2code"] is not None:
                country.alpha2code = params["alpha2code"]
            if params["alpha3code"] is not None:
                country.alpha3code = params["alpha3code"]
            if params["currency"] is not None:
                country.currency = params["currency"]
            country.active = 1
        else:
            abort(
                404, message=f"Updating: Country with this id='{id}' does not exist!")

        CountryModel.commit()
        return country, 202

    def delete(self, id):
        # forgot to add filter 'active=1' since we have solft-deleted countries in db.
        country = CountryModel.query.filter_by(id=id).first()
        if not country:
            abort(
                404, message=f"Solf-Deletion: No countries with this id='{id}' exist!")
        country.active = 0

        CountryModel.commit()
        return country, 202
