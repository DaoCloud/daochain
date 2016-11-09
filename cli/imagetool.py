from hashlib import sha256

from docker.client import Client as _C


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
