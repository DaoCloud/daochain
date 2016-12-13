# DaoChain

[![daochain](https://ci.daocloud.io/api/badge/build/daocloud/daochain)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)
[![daochain](https://ci.daocloud.io/api/badge/test/daocloud/daochain)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)
[![daochain](https://ci.daocloud.io/api/badge/coverage/daocloud/daochain?branch=master&criteria=line-rate)](https://dashboard.daocloud.io/orgs/daocloud/build-flows/b63b9fb5-d3d4-404b-8699-548910d87e51)

DaoChain 是 DaoCloud 自安全扫描，安全构建镜像等功能之后隆重推出的分布式镜像校验系统。
DaoChain 结合了区块链的去中心化特性与镜像加密校验技术，实现了不依赖中心化 docker registry 的安全验证功能。
用户可通过加密本地镜像并与区块链上的发布者发布的 hash 值对比，确认本地镜像与发布者发布的内容一致，保障镜像端到端的安全性。

## QuickStart

1. clone the repo and compose up 

    ```
    git clone https://github.com/DaoCloud/daochain.git
    cd daochain
    docker-compose up -d
    ```

2. open webui (http://127.0.0.1:8000)

## 使用说明

### 获取安全签名的镜像

* 请您登陆 DaoCloud 账号
* 点击账户详情选择您的组织，并填写密码生成钱包地址（请务必保证密码的安全！）
* 选择“账户信息”，打开挖矿开关，系统会在后台启动以太坊客户端，开始同步所有验证数据，同步完成后会进行挖矿，过一段时间会获取账户余额
* 点击“镜像市场”，可以看到拥有区块链验证的公开镜像，点击拉取并在“本地镜像”查看，若通过验证则证明本地镜像与发布者提交的一致

### 发布镜像并签名

* 选择“云端镜像”，这里是您保存在 DaoCloud 上的镜像。
* 拉取您需要签名的镜像。
* 点击签名，后台会计算校验码并以您当前使用的区块链钱包地址发布签名，系统会等待区块被确认所以会等待一段时间
* 完成后签名后登录 DaoCloud 选择公开镜像，可以在 DaoChain “镜像市场” 看到

申请测试代币或咨询请联系 support@daocloud.io

## TODO

* Command Line Tool
* Better image Hashing
* Offline verifying
* Better peer discovery

## 贡献指南

请参考[CONTRIBUTION.md](./CONTRIBUTION.md)

## 开源许可证

[Apache 2 license](./LICENSE)
