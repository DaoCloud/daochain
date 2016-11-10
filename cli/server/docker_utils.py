from imagetool import Client
from utils import memoize


@memoize
def docker_client():
    return Client('unix://var/run/docker.sock')
