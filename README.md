# DaoChain

[![daochain](https://ci.daocloud.io/api/badge/build/daocloud/daochain)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)
[![daochain](https://ci.daocloud.io/api/badge/test/daocloud/daochain)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)
[![daochain](https://ci.daocloud.io/api/badge/coverage/daocloud/daochain?branch=master&criteria=line-rate)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)

DaoChain is a decentralized application (Dapp) based on Ethereum, dedicated to solving the trust issues during sharing and trading of the digital assets (including Docker images) on the Internet.

![logo](resources/DaoChain.png)

## Why

The open Internet allows us to share data online so freely that it is unclear whether the data we got is maliciously tampered during data transmission. Although we could use RSA and PGP to guarantee the data credibility and security in peer-to-peer transmission on the internet, for most of time data is stored on public clouds. How to publish data and verify the data acquired in a convenient way become a problem.

Docker image distribution is a typical example of data dissemination via repository. The publisher builds an image on local machine, pushes the image to the remote repository，where other users can then pull the image. In this process, how to make sure that the image pulled is the original version released by publisher? How to make sure that there is no revision from hosting provider or in dissemination? How to mark the ownership of property?

**Repository being hacked by hacker：**

![hack](resources/hack-flow.png)

DaoChain is developed as a solution to these problems. By storing the information on a decentralized blockchain network, we can eliminate the possibility of the data being easily tampered in a centralized network. The offline signature and verification makes the data publishing and acquisition more convenient and secure. 

## How

**Now you know the image is hacked：**

![secure](resources/secure-flow.png)

The image publisher calculates the hash of the image on the local machine and then writes the message into the blockchain. The cryptography on the blockchain guarantees no forgery in this process, so publisher can safely share the image on public registry.

Image users can calculate the hash of the image they pulled from the public registry, and compare it with the hash that publisher stored in the blockchain. This can verify whether the image is identical to the original version from publisher.

### Project Structure

We choose Ethereum among so many blockchain implements to build the DaoChain. The [Ethereum](https://www.ethereum.org/) is a public blockchain-based distributed computing platform that supports Smart Contract. It provides a decentralized virtual machine called Ethereum Virtual Machine (EVM) that can execute peer-to-peer contracts. 

DaoChain consists of four parts:

- [Smart Contract](https://github.com/DaoCloud/dao-chain/tree/master/contract)
- [Ethereum Client](https://github.com/DaoCloud/dao-chain/tree/master/geth)
- [Local Server & Client](https://github.com/DaoCloud/dao-chain/tree/master/app)
- [WebUI](https://github.com/Revolution1/dao-chain/tree/master/webui)

**Project Structure:**

![structure](resources/structure.png)

### Smart Contract

DaoChain’s Smart Contract is written in [solidity](https://github.com/ethereum/solidity) using [truffle](https://github.com/ConsenSys/truffle) framework.

In the directory of [contract/contracts](https://github.com/DaoCloud/dao-chain/tree/master/contract/contracts), there are two smart contracts (Migrations.sol is for deploying contracts). Currently we are using [DaoHubVerify.sol](https://github.com/DaoCloud/dao-chain/blob/master/contract/contracts/DaoHubVerify.sol). The contract defines a data structure:

```solidity
mapping(address => mapping(bytes => Image)) ownerIdImageMap;
```

**Verification process：**

![flow](resources/flow.png)

The other smart contract, [DaoHubAccount.sol](https://github.com/DaoCloud/dao-chain/blob/master/contract/contracts/DaoHubAccount.sol), features functionality of mapping the account of Ethereum and image hosting provider. DaoChain will support this contract in the future version, to fully support the complete decentralization and the image offline verification.

### Ethereum Client

DaoChain uses the official Ethereum client [go-ethereum](https://github.com/ethereum/go-ethereum), and [eth-net-intelligence-api](https://github.com/cubedro/eth-net-intelligence-api) for metrics collection. 

### Local Server 

The Local server is written in Python and includes two parts:

* Local Server：running in the local container, communicating with Docker and Ethereum Client via Docker API and JSONRPC respectively, and providing the REST API to WebUI and CLI.
* Command-line tool：A CLI tool to use DaoChain（WIP）.

When the Docker image is pushed to Registry, a hash will be generated but the value will not change with image content. We [calculate](https://github.com/Revolution1/dao-chain/blob/master/app/dockerclient.py#L35) SHA256 hash of the `tar` file content saved with `docker save`, which only represents the certain image.
> Note: the current algorithm is relatively low efficiency and will be improved in the future.

### WebUI

DaoChain’s WebUI uses AngularJS and DaoStyle – a Angular component library by [DaoCloud](www.daocloud.io).


## Goals

- [x] Content Trust Verification
- [ ] Support Third-party Registry
- [ ] Image Trade
- [ ] Decentralized Registry


## QuickStart

1.	Clone the repo and run with docker-compose

    ```
    git clone https://github.com/DaoCloud/daochain.git
    cd daochain
    docker-compose up -d
    ```

2. Open WebUI (`http://127.0.0.1:8000`)

## TODO

* Tests and Documentation
* Command-Line Tool
* Better Image Hashing
* Peer Discovery
* Offline Verifying


## Contribution (Chinese)

Please refer to [CONTRIBUTION.md](./CONTRIBUTION.md)

## License

[Apache License 2.0](./LICENSE)
