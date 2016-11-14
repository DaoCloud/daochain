import os
import tarfile
import tempfile
from hashlib import md5, sha256

import requests
from docker.client import Client as _C

from blockchain import DaoHubVerify

hub_endpoint = os.getenv('HUB_ENDPOINT', 'http://api.daocloud.co')


class Client(_C):
    def get_image_hash(self, resource_id, hasher=sha256, blocksize=4096):
        image = self.get_image(resource_id)
        f_handler, filename = tempfile.mkstemp(suffix='.tar', text=False)
        with open(filename, 'wb') as f:
            f.write(image.data)
        tar_file = tarfile.open(fileobj=open(filename))
        members = tar_file.getmembers()
        hashes = []
        for m in members:
            f = tar_file.extractfile(m)
            if f is None:
                continue
            h = md5()
            h.update(f.read())
            hashes.append(h.hexdigest())
        os.remove(filename)
        h = hasher()
        h.update("$".join(sorted(hashes)))
        return h.hexdigest()

    def get_image_hash_uint(self, resource_id, hasher=sha256, blocksize=4096):
        hash = self.get_image_hash(resource_id, hasher, blocksize)
        return int(hash, 16)

    def pull_image(self, repository, tag=None, username=None, password=None):
        auth_config = None
        if username and password:
            auth_config = dict(username=username, password=password)
        self.pull(repository, tag, insecure_registry=True, auth_config=auth_config)

    def verify_image_hash(self, repoTag):
        from server import imageutils
        registry, namespace, repo, tag = imageutils.parse_image_name(repoTag)
        resp = requests.get('{}/hub/v2/blockchain/tenant/{}/addresses'.format(hub_endpoint, namespace))
        try:
            resp.raise_for_status()
            addresses = resp.json()["results"]
        except:
            addresses = []
        image_hash = addresses and self.get_image_hash_uint(repoTag)
        d = DaoHubVerify()
        signed = False
        verify = False
        for address in addresses:
            hash = d.queryImage(address['address'], repoTag)
            if hash[0]:
                signed = True
            if hash[0] == image_hash:
                verify = True
        return signed, verify


if __name__ == '__main__':
    from server.docker_utils import docker_client

    c = docker_client()
    print(c.get_image_hash('daocloud.io/library/ubuntu:latest'))
    print(c.get_image_hash('daocloud.io/library/ubuntu:latest'))
