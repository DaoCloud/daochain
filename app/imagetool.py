import os
import re
import tarfile
import tempfile
from hashlib import md5, sha256

import requests
from docker.client import Client as _C

from blockchain import DaoHubVerify
from settings import HUB_ENDPOINT
from storage import store
from utils import hex_to_uint


class Client(_C):
    def get_image_hash_with_cache(self, resource_id, *args):
        image_id = self.image_id(resource_id)
        h = store.get(image_id)
        if not h:
            h = self.get_image_hash(resource_id, *args)
            store.set(image_id, h)
        return h

    def image_id(self, resource_id):
        return self.inspect_image(resource_id)['Config']['Image']

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
                line = f.readline(blocksize)
                if not line:
                    break
                h.update(line)
            hashes.append(h.hexdigest())
        os.remove(filename)
        h = hasher()
        h.update("$".join(sorted(hashes)))
        rt = h.hexdigest()
        image_id = self.image_id(resource_id)
        if store.get(image_id) != rt:
            store.set(image_id, rt)
        return rt

    def get_image_hash_uint(self, resource_id, hasher=sha256, blocksize=4096):
        h = self.get_image_hash_with_cache(resource_id, hasher, blocksize)
        return hex_to_uint(h)

    def pull_image(self, repository, tag=None, username=None, password=None):
        auth_config = None
        if username and password:
            auth_config = dict(username=username, password=password)
        self.pull(repository, tag, insecure_registry=True, auth_config=auth_config)

    def verify_image_hash(self, repoTag):
        from eth_abi.exceptions import DecodingError
        registry, namespace, repo, tag = parse_image_name(repoTag)
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


def parse_image_name(raw_name):
    DEFAULT_REGISTRY_NAMESPACE = 'library'
    DEFAULT_IMAGE_TAG = 'latest'
    DEFAULT_REGISTRY_URL = 'registry-1.docker.io'
    IS_REGISTRY = re.compile(r'\.|:|localhost')
    IS_NONE_PRIVATE_REGISTRY = re.compile(DEFAULT_REGISTRY_URL + r'|daocloud.io')

    def _name_tag(n):
        s = n.split('@')
        if len(s) != 1:
            return s[0], s[1]

        s = n.split(':')
        if len(s) == 1:
            return n, DEFAULT_IMAGE_TAG
        # elif len(s) == 2:
        else:
            return s[0], s[1]

    is_registry = lambda x: bool(IS_REGISTRY.search(x))
    is_none_private_registry = lambda x: bool(IS_NONE_PRIVATE_REGISTRY.search(x))
    raw_name = raw_name.strip()
    splited_name = raw_name.split('/')
    # deal with default registry
    name, tag = _name_tag(splited_name[-1])
    if len(splited_name) == 1:
        registry = DEFAULT_REGISTRY_URL
        namespace = DEFAULT_REGISTRY_NAMESPACE
    elif len(splited_name) == 2 and not is_registry(splited_name[0]):
        registry = DEFAULT_REGISTRY_URL
        namespace = splited_name[0]
    # deal with none private
    elif len(splited_name) == 2 and is_none_private_registry(splited_name[0]):
        registry = splited_name[0]
        namespace = DEFAULT_REGISTRY_NAMESPACE
    elif len(splited_name) == 3 and is_none_private_registry(splited_name[0]):
        registry = splited_name[0]
        namespace = splited_name[1]
    # deal with private registry
    elif len(splited_name) == 2 and is_registry(splited_name[0]):
        registry = splited_name[0]
        namespace = ''
    # elif len(splited_name) == 2 and is_registry(splited_name[0]):
    else:
        registry = splited_name[0]
        namespace = splited_name[1]
    return registry, namespace, name, tag


if __name__ == '__main__':
    from app import docker_client
    from time import time

    c = docker_client()
    t1 = time()
    print(c.get_image_hash('daocloud.io/revolution1/ethereum_geth:latest'))
    t2 = time()
    # print(c.get_image_hash('daocloud.co/eric/d2053:latest'))
    print(c.get_image_hash_with_cache('daocloud.io/revolution1/ethereum_geth:latest'))
    t3 = time()

    print('hash: %ss   cache: %ss' % (t2 - t1, t3 - t2))
