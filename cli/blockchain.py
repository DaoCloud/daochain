# import web3patch
#
# web3patch.patch_all()
from web3 import RPCProvider, Web3

from utils import load_json_from
from utils import memoize


@memoize
def contract_deployed():
    return load_json_from('deployed_contract.json')


@memoize
def web3_client():
    return Web3(RPCProvider())


class DaoHubVerify(object):
    def __init__(self):
        data = contract_deployed()
        self.abi = data['DaoHubVerify']['abi']
        self.address = data['DaoHubVerify']['address']
        self._client = web3_client()
        self._eth = self._client.eth
        self._contract = self._eth.contract(self.abi, address=self.address)
        self.trans_filter = self._contract.on('regImage')

    def registerImage(self, imageHash, repoTag, imageId):
        return self._contract.transact().registerImage(imageHash, repoTag, imageId)

    def queryImage(self, owner, repoTag):
        return self._contract.call().queryImage(owner, repoTag)

    def regImage(self, callback):
        """
        callback receive a dict:
        [{'address': u'0x8a1e16278f7695823962ada686ca13a202ee97d1',
          'args': {u'imageHash': u'123123da\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
           u'imageId': u'123123\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
           u'owner': u'0x79eacb37490b7aa319b0bc405f2110c3b36259a9',
           u'repoTag': u'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80'},
          'blockHash': u'0x61cb83263400c11477edfcbaf637e55910038865b80009082b51460e38aa13fc',
          'blockNumber': 8,
          'event': u'regImage',
          'logIndex': 0,
          'transactionHash': u'0xfe0309c12fe33ce1b6c79bd6c5045e9ca16ae0d3d0799db86f2f5f90d44f4862',
          'transactionIndex': 0}]
        """
        self.trans_filter.watch(callback)


if __name__ == '__main__':
    d = DaoHubVerify()
    print(d.registerImage(0x921fdcfd91e4237afaaf63bc3010e0993e012f816a409ee705f3db3b65fa274d,
                          'daocloud.io/daocloud/dao-2048',
                          0x067c8da9d5abd40c3f2aaf58bef8412cd42b535b847483837152fb877f1f15de))
    print(d.queryImage(web3_client().eth.coinbase, 'daocloud.io/daocloud/dao-2048'))
