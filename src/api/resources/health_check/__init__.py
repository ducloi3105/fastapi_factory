from src.bases.api.resource import Resource


class HealthCheckResource(Resource):
    auth_required = False
    endpoint = '/health-check'
