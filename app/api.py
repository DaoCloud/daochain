from flask_restful import Api, Resource
from flask_restful import reqparse
from storage import store as _S

from blockchain import DaoHubVerify
from blockchain import NotEnoughBalance
from imagetool import Client
from imageutils import get_repos


def load_api(app):
    rest = Api(app)
    rest.add_resource(API, '/api')
    rest.add_resource(ImagesAPI, '/api/images')
    rest.add_resource(ImageVerifyAPI, '/api/verify-image')
    rest.add_resource(ImagePullAPI, '/api/pull-image')
    rest.add_resource(ImageSignAPI, '/api/sign-image')
    rest.add_resource(DefaultAccountAPI, '/api/default-account')


class API(Resource):
    def get(self):
        return 'Hello API'


class ImagesAPI(Resource):
    def get(self):
        return get_repos()


class ImageVerifyAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('repo_tag', type=str, required=True, help='No task title provided', location='json')
        super(ImageVerifyAPI, self).__init__()

    def post(self):
        from imagetool import Client
        c = Client()
        args = self.reqparse.parse_args()
        signed, verify = c.verify_image_hash(args['repo_tag'])
        return dict(signed=signed, verify=verify)


class ImagePullAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('repo_tag', type=str, required=True, help='No task title provided', location='json')
        self.reqparse.add_argument('username', type=str, required=False, help='No task title provided', location='json')
        self.reqparse.add_argument('password', type=str, required=False, help='No task title provided', location='json')
        super(ImagePullAPI, self).__init__()

    def post(self):
        from imagetool import Client
        c = Client()
        args = self.reqparse.parse_args()
        c.pull_image(args['repo_tag'], username=args.get('username'), password=args.get('password'))
        return dict(pull=True)


class ImageSignAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('repo_tag', type=str, required=True, help='No task title provided', location='json')
        self.reqparse.add_argument('image_id', type=str, required=True, help='No task title provided', location='json')
        super(ImageSignAPI, self).__init__()

    def post(self):
        c = Client()
        args = self.reqparse.parse_args()
        repo_tag = args['repo_tag']
        image_id = args['image_id']
        d = DaoHubVerify()
        hash = c.get_image_hash_with_cache(repo_tag)
        try:
            tx = d.registerImage(hash, repo_tag, image_id)
        except NotEnoughBalance:
            return dict(msg='not enough balance'), 402
        return dict(msg='ok', tx=tx), 200


class DefaultAccountAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('address', type=str, required=False, help='No task title provided', location='json')
        super(DefaultAccountAPI, self).__init__()

    def post(self):
        from storage import Storage
        s = Storage()
        args = self.reqparse.parse_args()
        default_address = args['address']
        s.set('default_address', default_address)
        return dict(default_address=default_address)

    def get(self):
        default_address = _S.get('default_address')
        return dict(default_address=default_address)
