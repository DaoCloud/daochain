# DaoChain

[![daochain](https://ci.daocloud.io/api/badge/build/daocloud/daochain)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)
[![daochain](https://ci.daocloud.io/api/badge/test/daocloud/daochain)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)
[![daochain](https://ci.daocloud.io/api/badge/coverage/daocloud/daochain?branch=master&criteria=line-rate)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)

DaoChain is a decentralized-application (DApp) based on Ethereum, dedicated to solving the trust issues in the sharing and transaction of digital assets (including Docker image) in the Internet.

![logo](resources/DaoChain.png)

## Why

The open Internet facilitates data sharing online, but also because of its openness, it is unclear whether the data we get are maliciously tampered in transmission. The RSA and PGP guarantee the data credibility and security in peer-to-peer transmission on the internet. In the Cloud era, data spreads across the Internet by uploading to the public cloud storage，then how to publish data and verify the data acquired in a convenient way become a difficult problem.

Docker image distribution is a typical example of data dissemination via public cloud storage. The publisher builds an image on local server, pushes the image to the repository，where users then pull images from. In this process, how to make sure that the image pulled is the original version released by publisher? How to make sure that there is no modification from hosting provider or in dissemination? How to mark the ownership of the image?

**repository being hacked by hackers：**

![hack](resources/hack-flow.png)

DaoChain is developed as a solution to these problems. By storing the image verification on the decentralized block-chain network, we can eradicate the possibility of the data being easily tampered in centralized network. The offline signature and verification makes the data publishing and acquisition more convenient and secure. 

## How

**Now you know the image is hacked：**

![secure](resources/secure-flow.png)

The image publisher calculates the hash of the image on the local-server and then writes the message into the blockchain. The cryptography on the blockchain guarantees no forgery in this process, so publisher can safely share the image on public registry.

Image users can calculate the hash of the image they pulled from the public registry, and compare it with the hash that publisher stored in the blockchain. This can verify whether the image is identical to the original version from publisher.

### Project Structure

We choose Ethereum among so many blockchain implements to build the DaoChain. The [Ethereum](https://www.ethereum.org/) is a public blockchain-based distributed computing platform, featuring smart contract functionality. It provides a decentralized virtual machine, the Ethereum Virtual Machine (EVM), that can execute peer-to-peer contracts using a token called ether.

The DaoChain Project consists of four parts:：[Smart Contracts](https://github.com/DaoCloud/dao-chain/tree/master/contract)，[Ethereum Client](https://github.com/DaoCloud/dao-chain/tree/master/geth)，[Local-Server](https://github.com/DaoCloud/dao-chain/tree/master/app)，[WebUI](https://github.com/Revolution1/dao-chain/tree/master/webui)

**Project Structure:**

![structure](resources/structure.png)

### Smart Contract

The DaoChain smart contract is wiriiten in [solidity](https://github.com/ethereum/solidity), undered [truffle](https://github.com/ConsenSys/truffle) framework.

In the directory of [contract/contracts](https://github.com/DaoCloud/dao-chain/tree/master/contract/contracts), there are two smart contracts (Migrations.sol is for deployment). Currently we are using [DaoHubVerify.sol](https://github.com/DaoCloud/dao-chain/blob/master/contract/contracts/DaoHubVerify.sol)。The contract defines a data structure:

```solidity
mapping(address => mapping(bytes => Image)) ownerIdImageMap;
```

The nested mapping can store the corresponding relation between the address (the writer’s Ethereum account address), repo Tag (image url), and full description of image (including hash, image ID etc.) 
 
**Verification process：**

![flow](resources/flow.png)

The other smart contract, [DaoHubAccount.sol](https://github.com/DaoCloud/dao-chain/blob/master/contract/contracts/DaoHubAccount.sol), features functionality of mapping the account of Ethereum and image hosting provider. DaoChain will support this contract in the future updating version, to fully realize the complete decentralization and image verification offline.

### Ethereum Client

The DaoChain uses [go-ethereum](https://github.com/ethereum/go-ethereum) the official Ethereum Client 
the official Ethereum Client and [eth-net-intelligence-api](https://github.com/cubedro/eth-net-intelligence-api) for metrics collection. 

### Local-Server

The Local server written in the Python language and include two parts:

* Local Server：running in the local container, communicating with Docker and Ethereum Client via Docker API and JSONRPC respectively, and providing the RestAPI to WebUI and CLI.
* Commandline tool：providing command-line tools featuring the functionality of viewing and using DaoChain（In Develope...）。

When the Docker image is pushed to Registry, a hash will be generated but the value will not change with image content. We [calculate](https://github.com/Revolution1/dao-chain/blob/master/app/dockerclient.py#L35) sha256 hash of the tar file content saved with "docker save", which only represents the certain image.
> Ps: the current algorithm is of relatively low efficiency and will be improved later.

### WebUI

The WebUI of DaoChain depends on the AngularJS Framework and DaoStyle, the angular component library of DaoCloud.


## Goals

- [x] Content Trust Verification
- [ ] Supprot Thirdparty Registry
- [ ] Image Trade
- [ ] Decentralized Registry


## QuickStart

1.	Clone the code and start with docker-compose

    ```
    git clone https://github.com/DaoCloud/dao-chain.git
    cd dao-chain
    docker-compose up -d
    ```

2. Open WebUI (http://127.0.0.1:8000)

## TODO

* Test and Document
* Commandline Tool
* Better Image Hashing
* Peer Discovery
* Offline Verifying


## Contribution (Chinese)

Please refer to [CONTRIBUTION.md](./CONTRIBUTION.md)

## Licensing

[Apache 2](./LICENSE)