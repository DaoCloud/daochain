from flask_restful import Api, Resource

from server.docker_utils import docker_client


def load_api(app):
    rest = Api(app)
    rest.add_resource(API, '/api')
    rest.add_resource(ImagesAPI, '/api/images')
    rest.add_resource(ImageVerifyAPI, '/api/images/<int:image_id>/verify')
    # rest.add_resource(UserListAPI, '/api/user')
    # rest.add_resource(UserAPI, '/api/user/<int:uid>')


class API(Resource):
    def get(self):
        return 'Hello API'

class ImagesAPI(Resource):
    def get(self):
        return docker_client().images()

class ImageVerifyAPI(Resource):
    def get(self, image_id):
        return

