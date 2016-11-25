import json
import os
import tarfile
import tempfile
from hashlib import md5, sha256

import gevent
from docker.client import Client as _C
from eth_abi.exceptions import DecodingError

from blockchain import DaoHubVerify
from hubclient import Client as Hub
from storage import Cache
from storage import store
from utils import gen_random_str, hex_to_uint, parse_image_name


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
        _, _, _, _tag = parse_image_name(repository)
        if not tag:
            tag = _tag
        auth_config = None
        if username and password:
            auth_config = dict(username=username, password=password)
        resp = self.pull(repository, tag, stream=True, insecure_registry=True, auth_config=auth_config)

        def iter_json():
            for i in resp:
                i = i.strip()
                if not i:
                    continue
                try:
                    j = json.loads(i)
                    yield j
                except ValueError:
                    continue

        layers = {}
        for j in iter_json():
            if j.get('status') == 'Pulling fs layer':
                layers[j.get('id')] = {}
            elif layers or j.get('status') == 'Downloading':
                break

        def iter_progress():
            for _j in iter_json():
                if _j.get('status') == 'Downloading':
                    layers[_j.get('id')] = _j.get('progressDetail')
                    total = None
                    current = None
                    if all(layers):
                        total = sum([i.get('total', 0) for i in layers.values()])
                        current = sum([i.get('current', 0) for i in layers.values()])
                    yield dict(
                        layer_count=len(layers),
                        layers=layers,
                        current=current,
                        total=total,
                        percent=current * 100 / total,
                        finished=False
                    )

        task_id = gen_random_str(8)

        def consume():
            cache = Cache()
            for i in iter_progress():
                cache.set(task_id, i)
            cache.set(task_id, {'finished': True, 'percent': 100})

        gevent.spawn(consume)
        # consume()
        return task_id

    @staticmethod
    def poll_pull_progress(task_id):
        return Cache().get(task_id) or {}

    def verify_image_hash(self, repoTag):
        _, namespace, _, _ = parse_image_name(repoTag)
        addresses = Hub().addresses(namespace).get(namespace)
        if not addresses:
            return False, False
        image_hash = self.get_image_hash_uint(repoTag)
        d = DaoHubVerify()
        signed = False
        verify = False
        for address in addresses:
            try:
                hash = d.queryImage(address, repoTag)
                if hash[0]:
                    signed = True
                if hash[0] == image_hash:
                    verify = True
            except DecodingError:
                continue
        return signed, verify


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
