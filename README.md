# Hub Blockchain Verify

[![blockchain-hub](https://ci.daocloud.io/api/badge/build/daocloud/daochain)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)
[![blockchain-hub](https://ci.daocloud.io/api/badge/test/daocloud/daochain)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)
[![blockchain-hub](https://ci.daocloud.io/api/badge/coverage/daocloud/daochain?branch=master&criteria=line-rate)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)

DaoChain 是 DaoCloud 自安全扫描，安全构建镜像等功能之后隆重推出的分布式镜像校验系统。
DaoChain 结合了区块链的去中心化特性与镜像加密校验技术，实现了不依赖中心化 docker registry 的安全验证功能。
用户可通过加密本地镜像并与区块链上的发布者发布的 hash 值对比，确认本地镜像与发布者发布的内容一致，保障镜像端到端的安全性。

## QuickStart

1. clone the repo and compose up 

    ```
    git clone https://github.com/DaoCloud/blockchain-hub.git
    cd blockchain-hub
    docker-compose up -d
    ```

2. open webui (http://127.0.0.1:8000)

## 使用说明

http://docs.daocloud.io/dao-chain
