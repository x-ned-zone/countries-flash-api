from flask_restful import Resource, reqparse, fields, marshal_with
from CountryService import CountryService

# RestController: Handles mapped API routings to process requests.


class Country(Resource):
    def __init__(self):
        self.countryService = CountryService()
        self.country_add_params = reqparse.RequestParser()
        self.country_add_params.add_argument(
            "name", type=str, help="Name of the country is required", required=True)
        self.country_add_params.add_argument(
            "alpha2code", type=str, help="alpha 2 code of the country is required", required=True)
        self.country_add_params.add_argument(
            "alpha3code", type=str, help="alpha 3 code of the country is required", required=True)
        self.country_add_params.add_argument(
            "currency", type=str, help="currency of the country is required", required=True)
        self.country_update_params = reqparse.RequestParser()
        self.country_update_params.add_argument(
            "name", type=str, help="Name of the country is required", required=True)
        self.country_update_params.add_argument(
            "alpha2code", type=str, help="alpha 2 code of the country")
        self.country_update_params.add_argument(
            "alpha3code", type=str, help="alpha 3 code of the country")
        self.country_update_params.add_argument(
            "currency", type=str, help="currency of the country")
        self.country_delete_params = reqparse.RequestParser()
        self.country_delete_params.add_argument(
            "bit", type=int, help="Bit to indicate soft(0) or hard(1) deletion of country", required=True)

    # Used to serialize python objects that are returned as responses to api requests ...
    #   Just as like we have jackson in SpringBoot.
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'alpha2code': fields.String,
        'alpha3code': fields.String,
        'currency': fields.String
    }

    @marshal_with(resource_fields)
    def get(self, request):
        rsp = self.countryService.get(request)
        return rsp

    @marshal_with(resource_fields)
    def post(self, request):
        params = self.country_add_params.parse_args()
        rsp = self.countryService.add(request, params)
        return rsp

    @marshal_with(resource_fields)
    def put(self, request):
        params = self.country_update_params.parse_args()
        rsp = self.countryService.update(request, params)
        return rsp

    @marshal_with(resource_fields)
    def delete(self, request):
        rsp = self.countryService.delete(request)
        return rsp
