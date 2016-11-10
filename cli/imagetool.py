from hashlib import sha256

from docker.client import Client as _C
import requests
import os
from blockchain import DaoHubVerify

hub_endpoint = os.getenv('HUB_ENDPOINT')


class Client(_C):
    def get_image_hash(self, resource_id, hasher=sha256, blocksize=4096):
        hash = hasher()
        with self.get_image(resource_id) as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hash.update(block)
        return hash.hexdigest()

    def get_image_hash_uint(self, resource_id, hasher=sha256, blocksize=4096):
        hash = self.get_image_hash(resource_id, hasher, blocksize)
        return int(hash, 16)

    def pull_image(self, repository, tag=None, username=None, password=None):
        auth_config = None
        if username and password:
            auth_config = dict(username=username,password=password)
        self.pull(repository,tag,insecure_registry=True,auth_config=auth_config)

    def verify_image_hash(self, repoTag, auth_token=None, usernamespace=None):
        resp = requests.get('{}/hub/v2/blockchain/addresses'.format(hub_endpoint),
                            headers={'Authorization': auth_token, 'UserNameSpace': usernamespace})
        resp.raise_for_status()
        addresses = resp.json()["results"]
        image_hash = addresses and self.get_image_hash(repoTag)
        d = DaoHubVerify()
        for address in addresses:
            hash = d.queryImage(address['address'], repoTag)
            if hash == image_hash:
                return True
        return False
