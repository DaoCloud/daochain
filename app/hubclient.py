import gevent
from requests import request

from app.blockchain import web3_client
from app.errors import BindAddressFail, NotFound, Unauthorized
from app.settings import HUB_ENDPOINT
from app.utils import memoize
from storage import store as _S


class BaseClient(object):
    base_url = ''

    def _url_join(self, u1, u2):
        if u1[-1] == '/':
            u1 = u1[:-1]
        if u2[0] == '/':
            u2 = u2[1:]
        return '/'.join([u1, u2])

    def _request(self, method, url, **kwargs):
        if self.base_url:
            url = self._url_join(self.base_url, url)
        return request(method, url, **kwargs)

    def _get(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self._request('get', url, **kwargs)

    def _head(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self._request('head', url, **kwargs)

    def _options(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self._request('options', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request('post', url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request('put', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request('delete', url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request('patch', url, **kwargs)


class Client(BaseClient):
    base_url = HUB_ENDPOINT

    def __init__(self, username=None, password=None, token=None):
        self.username = username
        self.password = password
        self.token = token

    def _request(self, method, url, **kwargs):
        headers = kwargs.get('headers', {})
        if self.token:
            headers.setdefault('Authorization', self.token)
        headers.setdefault('User-Agent',
                           'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71')
        kwargs['headers'] = headers
        resp = super(Client, self)._request(method, url, **kwargs)
        if resp.status_code == 401:
            raise Unauthorized()
        return resp

    def login(self, username=None, password=None):
        pass

    @property
    def default_namespace(self):
        return _S.get('DEFAULT_USER_NAME_SPACE')

    @default_namespace.setter
    def default_namespace(self, value):
        _S.set('DEFAULT_USER_NAME_SPACE', value)

    @property
    @memoize
    def token_info(self):
        resp = self._get('/get-token-info')
        resp.raise_for_status()
        return resp.json()

    @property
    def orgs(self):
        """
        :rtype: list(dict)
        """
        orgs = []
        for t in self.token_info['user']['tenants']:
            if t['is_org']:
                orgs.append(t)
        return orgs

    @property
    def org_names(self):
        return [t['org_name'] for t in self.orgs]

    def addresses(self, tenant=None):
        if not tenant:
            tenant = self.default_namespace
        url = '/hub/v2/blockchain/tenant/{}/addresses'.format(tenant)
        resp = self._get(url)
        if resp.status_code == 404:
            if resp.json()['error_id'] == 'tenant_not_found':
                raise NotFound(resp.json())
        addresses = [i.get('address') for i in resp.json()["results"]]
        return {tenant: addresses}

    def get_all_bound_addresses(self):
        def get_addr(org, org_addrs):
            try:
                org_addrs[org] = self.addresses(org).get(org)
            except:
                pass

        org_addrs = {}
        _t = [gevent.spawn(get_addr, o, org_addrs) for o in self.org_names]
        _ = [_i.join() for _i in _t]
        return org_addrs

    def get_bound_orgs_with_local_eth_accounts(self):
        eth_accounts = web3_client().eth.accounts
        bound_org = _S.get('BOUND_ORG')
        if bound_org and _S.get('LAST_ETH_ACCOUNTS') == eth_accounts:
            return bound_org
        bound_org = {}
        for o, addrs in self.get_all_bound_addresses().items():
            bound_addrs = []
            for a in addrs:
                if a in eth_accounts:
                    bound_addrs.append(a)
            if bound_addrs:
                bound_org[o] = bound_addrs
        if bound_org:
            _S.set('BOUND_ORG', bound_org)
            _S.set('LAST_ETH_ACCOUNTS', eth_accounts)
        return bound_org

    def bind_address(self, addr, namespace=None):
        url = '/hub/v2/blockchain/addresses'
        header = {}
        if namespace:
            header = {'UserNameSpace': namespace}
        resp = self._post(url, json={"address": addr}, headers=header)
        if resp.status_code == 500:
            raise BindAddressFail(resp.status_code, addr, namespace)
        return resp.json()

    def del_address(self, addr, namespace=None):
        url = '/hub/v2/blockchain/addresses/{}'.format(addr)
        header = {}
        if namespace:
            header = {'UserNameSpace': namespace}
        resp = self._delete(url, headers=header)
        resp.raise_for_status()
        if resp.status_code == 204:
            _S.delete('BOUND_ORG')
            return True
        return False

    def set_default_namespace(self, namespace):
        self.default_namespace = namespace
        return namespace

    def get_default_namespace(self):
        return self.default_namespace

    def list_verified_public_repos(self, query=None, page=None, pagesize=None):
        url = '/hub/v2/blockchain/verified-public-repos'
        params = {
            'q': query,
            'page': page,
            'page_size': pagesize
        }
        resp = self._get(url, params=params)
        resp.raise_for_status()
        return resp.json()
