import json

import docker
from flask import request
from flask_restful import Api, Resource
from flask_restful import reqparse

from app.errors import NotFound
from blockchain import DaoHubVerify
from blockchain import NotEnoughBalance
from dockerclient import Client as docker_client
from hubclient import Client as hub_client
from localimage import get_repos
from storage import store as _S


def load_api(app):
    rest = Api(app)
    rest.add_resource(API, '/api')
    rest.add_resource(ImagesAPI, '/api/images')
    rest.add_resource(ImageVerifyAPI, '/api/verify-image')
    rest.add_resource(ImagePullAPI, '/api/pull-image')
    rest.add_resource(EstimatePull, '/api/pull-estimate')
    rest.add_resource(ImageSignAPI, '/api/sign-image')
    rest.add_resource(DefaultAccountAPI, '/api/default-account')
    rest.add_resource(AddressAPI, '/api/hub/addresses')
    rest.add_resource(DelAddressAPI, '/api/hub/addresses/<addr>')
    rest.add_resource(BoundAddressesAPI, '/api/hub/bound_addresses')
    rest.add_resource(DefaultNamespaceAPI, '/api/hub/default-namespace')


class API(Resource):
    def get(self):
        return 'Hello API'


class ImagesAPI(Resource):
    def get(self):
        return get_repos()


class ImageVerifyAPI(Resource):
    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('repo_tag', required=True) \
            .parse_args()
        signed, verify = docker_client().verify_image_hash(args['repo_tag'])
        return dict(signed=signed, verify=verify)


class ImagePullAPI(Resource):
    def get(self):
        args = reqparse.RequestParser() \
            .add_argument('task_id', required=True) \
            .parse_args()
        return docker_client().poll_pull_progress(task_id=args.get('task_id')), 200

    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('repo_tag', required=True) \
            .add_argument('username') \
            .add_argument('password') \
            .parse_args()
        task_id = docker_client().pull_image(args.get('repo_tag'),
                                             username=args.get('username'),
                                             password=args.get('password'))
        return dict(task_id=task_id), 200


class EstimatePull(Resource):
    def get(self):
        args = reqparse.RequestParser() \
            .add_argument('repo_tag', required=True) \
            .add_argument('with_cache', type=bool, default=False) \
            .parse_args()
        repo_tag = args.get('repo_tag')
        with_cache = args.get('with_cache')
        try:
            time = docker_client().estimate_image_hash_time(repo_tag, with_cache)
            return time, 200
        except docker.errors.NotFound as e:
            raise NotFound(json.loads(e.explanation))


class ImageSignAPI(Resource):
    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('repo_tag', required=True) \
            .add_argument('image_id', required=True) \
            .parse_args()
        repo_tag = args['repo_tag']
        image_id = args['image_id']
        d = DaoHubVerify()
        hash = docker_client().get_image_hash_with_cache(repo_tag)
        try:
            tx = d.registerImage(hash, repo_tag, image_id)
        except NotEnoughBalance:
            return dict(msg='not enough balance'), 402
        return dict(msg='ok', tx=tx), 200


class DefaultAccountAPI(Resource):
    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('address') \
            .parse_args()
        default_address = args['address']
        _S.set('default_address', default_address)
        return dict(default_address=default_address)

    def get(self):
        default_address = _S.get('default_address')
        return dict(default_address=default_address), 200


class AddressAPI(Resource):
    def get(self):
        args = reqparse.RequestParser() \
            .add_argument('namespace') \
            .parse_args()
        namespace = args.get('namespace')
        token = request.headers.get('Authorization')
        if not namespace:
            return hub_client(token=token) \
                       .get_all_bound_addresses(), 200
        return hub_client().addresses(namespace), 200

    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('address', required=True) \
            .add_argument('namespace') \
            .parse_args()
        token = request.headers.get('Authorization')
        return hub_client(token=token) \
                   .bind_address(args.get('address'), args.get('namespace')), 201


class DelAddressAPI(Resource):
    def delete(self, addr):
        token = request.headers.get('Authorization')
        args = reqparse.RequestParser() \
            .add_argument('namespace') \
            .parse_args()
        ok = hub_client(token=token).del_address(addr, args.get('namespace'))
        if ok:
            return None, 204
        else:
            return None, 400


class DefaultNamespaceAPI(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        return hub_client(token=token).get_default_namespace()

    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('namespace', required=True) \
            .parse_args()
        token = request.headers.get('Authorization')
        return hub_client(token=token) \
            .set_default_namespace(args.get('namespace'))


class BoundAddressesAPI(Resource):
    def get(self):
        args = reqparse.RequestParser() \
            .add_argument('local', type=bool) \
            .parse_args()
        token = request.headers.get('Authorization')
        local = args.get('local')
        if local:
            return hub_client(token=token) \
                .get_bound_orgs_with_local_eth_accounts()
        return hub_client(token=token).get_all_bound_addresses()
