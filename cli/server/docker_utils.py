from docker import Client

from utils import memoize


@memoize
def docker_client():
    return Client('http://192.168.1.30:2370')
