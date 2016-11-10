from datetime import datetime

from server.docker_utils import docker_client


def repo_name(repoTag):
    return repoTag.split('/')[-1].split(':')[0]


def repo_url(repoTag):
    return repoTag.split(':')[0]


def author_name(repoTag):
    split = repoTag.split('/')
    if len(split) == 3:
        return split[1]
    else:
        return 'library'


def blockchain_verified(repoTag):
    # return docker_client().verify_image_hash(repoTag)
    return

def blockchain_stat(repoTag):
    return {
        # 'confirm': 5,
        # 'transaction_id': '0x15527ae6a5e3c075cde6821aa5b6de5a326c5ac09fd71121f0d20f9b9e6a68d0',
        'imageHash': '0x921fdcfd91e4237afaaf63bc3010e0993e012f816a409ee705f3db3b65fa274b',
        'owner': '0xc268f55467127b94879a032093ded4c95cc511c1'
    }


def timestamp_to_iso(t):
    return datetime.fromtimestamp(int(t)).isoformat()


def remove_head_sha256(hash):
    return hash.split(':')[-1]


def tag(repoTag):
    return repoTag.split(':')[-1]


def get_repos():
    _images = docker_client().images()
    # repos = {}
    # for _i in _images:
    #     rt = _i.get('RepoTags', [])
    #     if not rt:
    #         continue
    #     for _t in rt:
    #         if _t.count('<none>') != 0:
    #             continue
    #         repo = repo_name(_t)
    #         if not repos.get(repo):
    #             repos[repo] = []
    #         repos[repo].append({
    #             'blockchain_verified': blockchain_verified(_t),
    #             'created_at': timestamp_to_iso(_i['Created']),
    #             'repo_tag': _t,
    #             'tag': tag(_t),
    #             'image_id': remove_head_sha256(_i['Id']),
    #             'author': author_name(_t),
    #             'blockchain_stat': blockchain_stat(_t)
    #         })
    # return repos
    repo_tags = {}
    for _i in _images:
        rt = _i.get('RepoTags', [])
        if not rt:
            continue
        for _t in rt:
            if _t.count('<none>') != 0:
                continue
            repo_tags[_t] = {
                'blockchain_verified': blockchain_verified(_t),
                'created_at': timestamp_to_iso(_i['Created']),
                'repo_tag': _t,
                'tag': tag(_t),
                'image_id': remove_head_sha256(_i['Id']),
                'author': author_name(_t),
                'blockchain_stat': blockchain_stat(_t)
            }
    return repo_tags.values()


import re

DEFAULT_REGISTRY_NAMESPACE = 'library'
DEFAULT_IMAGE_TAG = 'latest'
DEFAULT_REGISTRY_URL = 'registry-1.docker.io'
IS_REGISTRY = re.compile('')
IS_NONE_PRIVATE_REGISTRY = re.compile('')


def parse_image_name(raw_name):
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


_IMAGE_NAME_TEST_DATA = \
    '''
    python                                              ,registry-1.docker.io,library,python,latest
    python:1.1                                          ,registry-1.docker.io,library,python,1.1
    revol/python                                        ,registry-1.docker.io,revol  ,python,latest
    revol/python:1.1                                    ,registry-1.docker.io,revol  ,python,1.1
    revol/python@sha256:5a35100239643bfe                ,registry-1.docker.io,revol  ,python,sha256:5a35100239643bfe

    daocloud.io/python                                  ,daocloud.io         ,library,python,latest
    daocloud.io/python:1.1                              ,daocloud.io         ,library,python,1.1
    daocloud.io/revol/python                            ,daocloud.io         ,revol  ,python,latest
    daocloud.io/revol/python:1.1                        ,daocloud.io         ,revol  ,python,1.1
    daocloud.io/revol/python@sha256:5a35100239643bfe    ,daocloud.io         ,revol  ,python,sha256:5a35100239643bfe

    localhost/python                                    ,localhost           ,       ,python,latest
    localhost/python:1.1                                ,localhost           ,       ,python,1.1
    localhost/revol/python                              ,localhost           ,revol  ,python,latest
    localhost/revol/python:1.1                          ,localhost           ,revol  ,python,1.1
    localhost/revol/python@sha256:5a35100239643bfe      ,localhost           ,revol  ,python,sha256:5a35100239643bfe

    localhost:5000/python                               ,localhost:5000      ,       ,python,latest
    localhost:5000/python:1.1                           ,localhost:5000      ,       ,python,1.1
    localhost:5000/revol/python                         ,localhost:5000      ,revol  ,python,latest
    localhost:5000/revol/python:1.1                     ,localhost:5000      ,revol  ,python,1.1
    localhost:5000/revol/python@sha256:5a35100239643bfe ,localhost:5000      ,revol  ,python,sha256:5a35100239643bfe

    10.0.0.1/python                                     ,10.0.0.1            ,       ,python,latest
    10.0.0.1/python:1.1                                 ,10.0.0.1            ,       ,python,1.1
    10.0.0.1/revol/python                               ,10.0.0.1            ,revol  ,python,latest
    10.0.0.1/revol/python:1.1                           ,10.0.0.1            ,revol  ,python,1.1
    10.0.0.1/revol/python@sha256:5a35100239643bfe       ,10.0.0.1            ,revol  ,python,sha256:5a35100239643bfe

    aaa:5000/python                                     ,aaa:5000            ,       ,python,latest
    aaa:5000/python:1.1                                 ,aaa:5000            ,       ,python,1.1
    aaa:5000/revol/python                               ,aaa:5000            ,revol  ,python,latest
    aaa:5000/revol/python:1.1                           ,aaa:5000            ,revol  ,python,1.1
    aaa:5000/revol/python@sha256:5a35100239643bfe       ,aaa:5000            ,revol  ,python,sha256:5a35100239643bfe
    '''.strip().replace(' ', '').splitlines()
IMAGE_NAME_TEST_DATA = (x.split(',') for x in _IMAGE_NAME_TEST_DATA if x)


def test_parse_image_name():
    for line in IMAGE_NAME_TEST_DATA:
        _input = line[0]  # raw_name
        _output = tuple(line[1:])  # registry, namespace, name, tag
        if parse_image_name(_input) != _output:
            print(parse_image_name(_input))
            print(_output)
            assert False


if __name__ == '__main__':
    test_parse_image_name()
