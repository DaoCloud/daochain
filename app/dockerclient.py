import json
import os
import tarfile
import tempfile
from hashlib import md5, sha256
from time import time

import gevent
from docker.client import Client as _C
from eth_abi.exceptions import DecodingError

from app.settings import RECENT_HASH_TIME_BUCKET_SIZE
from blockchain import DaoHubVerify
from hubclient import Client as Hub
from storage import Cache
from storage import store as _S
from thirdparty.purepythonpolyfit.purePythonPolyFit import PolyFit
from utils import Bucket
from utils import gen_random_str, hex_to_uint, parse_image_name


class Client(_C):
    def get_image_hash_with_cache(self, resource_id, *args):
        image_id = self.image_id(resource_id)
        h = _S.get(image_id)
        if not h:
            h = self.get_image_hash(resource_id, *args)
            _S.set(image_id, h)
        return h

    def image_id(self, resource_id):
        return self.inspect_image(resource_id)['Id']

    def get_image_hash(self, resource_id, hasher=sha256, blocksize=4096):
        start_t = time()
        image_detail = self.inspect_image(resource_id)
        image_id = image_detail['Id']
        size = image_detail['Size']
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
                buf = f.readline(blocksize)
                if not buf:
                    break
                h.update(buf)
            hashes.append(h.hexdigest())
        os.remove(filename)
        h = hasher()
        h.update("$".join(sorted(hashes)))
        rt = h.hexdigest()
        end_t = time()
        b = Bucket(_S.get('RECENT_HASH_TIME', []), RECENT_HASH_TIME_BUCKET_SIZE)
        b.push((size, (end_t - start_t)))
        _S.set('RECENT_HASH_TIME', b)
        if _S.get(image_id) != rt:
            _S.set(image_id, rt)
        return rt

    def estimate_image_hash_time(self, resource_id, with_cache=False):
        b = _S.get('RECENT_HASH_TIME', [])
        if with_cache and _S.has(self.image_id(resource_id)):
            return 0
        if b:
            size = self.inspect_image(resource_id)['Size']
            points = {}
            for i in b:
                if i[0] in points:
                    points[i[0]] = (points[i[0]] + i[1]) / 2.0
                else:
                    points[i[0]] = i[1]
            x = points.keys()
            y = points.values()
            if len(x) > 2:
                predict = PolyFit(x, y)[size]
                if predict < 0:
                    return 0
                return predict
            else:
                efficiency = sum(x) / sum(y)
                return size / efficiency
        return -1

    def get_image_hash_uint(self, resource_id, hasher=sha256, blocksize=4096):
        h = self.get_image_hash_with_cache(resource_id, hasher, blocksize)
        return hex_to_uint(h)

    # TODO: make it better using websocket
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

        task_id = 'p_%s' % gen_random_str(8)

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
    c = Client()
    repo_tag = 'debian:latest'
    print('repo_tag:                   %s' % repo_tag)
    print('estimate:                   %ss' % c.estimate_image_hash_time(repo_tag))
    t1 = time()
    print('get_image_hash:             %s' % c.get_image_hash(repo_tag))
    t2 = time()
    print('get_image_hash_with_cache:\t%s' % c.get_image_hash_with_cache(repo_tag))
    t3 = time()
    print('hash: %ss   cache: %ss\n' % (t2 - t1, t3 - t2))
