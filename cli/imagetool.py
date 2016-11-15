import os
import tarfile
import tempfile
from hashlib import md5, sha256

import requests
from docker.client import Client as _C

from blockchain import DaoHubVerify
from server.settings import HUB_ENDPOINT
from server.storage import Storage


class Client(_C):
    def get_image_hash_with_cache(self, resource_id, *args):
        s = Storage()
        r = self.inspect_image(resource_id)
        image_id = r['Config']['Image']
        h = s.get(image_id)
        if not h:
            h = self.get_image_hash(resource_id, *args)
            s.set(image_id, h)
        return h

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
            while True:
                line = f.readline(4096)
                if not line:
                    break
                h.update(line)
            hashes.append(h.hexdigest())
        os.remove(filename)
        h = hasher()
        h.update("$".join(sorted(hashes)))
        return h.hexdigest()

    def get_image_hash_uint(self, resource_id, hasher=sha256, blocksize=4096):
        hash = self.get_image_hash_with_cache(resource_id, hasher, blocksize)
        return int(hash, 16)

    def pull_image(self, repository, tag=None, username=None, password=None):
        auth_config = None
        if username and password:
            auth_config = dict(username=username, password=password)
        self.pull(repository, tag, insecure_registry=True, auth_config=auth_config)

    def verify_image_hash(self, repoTag):
        from eth_abi.exceptions import DecodingError
        from server import imageutils
        registry, namespace, repo, tag = imageutils.parse_image_name(repoTag)
        resp = requests.get('{}/hub/v2/blockchain/tenant/{}/addresses'.format(HUB_ENDPOINT, namespace))
        try:
            resp.raise_for_status()
            addresses = resp.json()["results"]
        except:
            addresses = []
        if not addresses:
            return False, False
        image_hash = self.get_image_hash_uint(repoTag)
        d = DaoHubVerify()
        signed = False
        verify = False
        for address in addresses:
            try:
                hash = d.queryImage(address['address'], repoTag)
                if hash[0]:
                    signed = True
                if hash[0] == image_hash:
                    verify = True
            except DecodingError:
                continue
        return signed, verify


if __name__ == '__main__':
    from server.docker_utils import docker_client

    c = docker_client()
    print(c.get_image_hash('daocloud.io/library/ubuntu:latest'))
    print(c.get_image_hash_with_cache('daocloud.io/library/ubuntu:latest'))
