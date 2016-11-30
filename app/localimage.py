from app.utils import parse_image_name, timestamp_to_iso, remove_head_sha256
from dockerclient import Client


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


def get_repos():
    _images = Client().images()
    repo_tags = {}
    for _i in _images:
        rt = _i.get('RepoTags', [])
        if not rt:
            continue
        for _t in rt:
            if _t.count('<none>') != 0:
                continue
            registry, namespace, name, tag = parse_image_name(_t)
            repo_tags[_t] = {
                # 'blockchain_verified': blockchain_verified(_t),
                'created_at': timestamp_to_iso(_i['Created']),
                'repo_tag': _t,
                'tag': tag,
                'namespace': namespace,
                'registry': registry,
                'name': name,
                'image_id': remove_head_sha256(_i['Id']),
                # 'author': author_name(_t),
                # 'blockchain_stat': blockchain_stat(_t)
            }
    return repo_tags.values()
