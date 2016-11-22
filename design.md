当区块链遇到docker 容器与区块链的美丽邂逅
=================================

这是一个文艺范十足(恶俗)的标题，试图撮合两个八杆子打不着的家伙。故事的结局一般都是按照套路出牌，两个主角愉快地在一起了。结局总是类似的，不过过程却有各自的精彩。

区块链刨底
--------

区块链（Blockchain）技术自身仍然在飞速发展中，目前还缺乏统一的规范和标准，试图给区块链下定义都是一个难题。根据 [wikipedia](https://en.wikipedia.org/wiki/Blockchain_\(database\)) 的定义

```
Blockchain is a distributed database that maintains a continuously-growing list of records called blocks.
```

越来越多的研究者、专家把区块链归类为分布式数据库的范畴，也有人把区块链定义为一种类似于链表的数据结构：
<div style="text-align: center">
  <img src="resources/block_chain.png"/>
</div>
```
区块链是一个类似于链表的数据结构，该数据结构中每一个节点记录了前节点中数据的 Hash 值、当前节点的数据。
在当前节点不变都情况下，前节点的任何改变都会使得这条链无效(invalid)。
```

笔者认为两种定义是不冲突的、可以说是相辅相成的。前者更多的强调区块链的分布式协作的集体行为，后者更多的关注这一协作群体中每一个个体——区块链本身。在大多数语境下，大家关注更多的是区块链分布式协作的集体效应，因此下文关于区块链，不特意说明的情况下，都与 wikipedia 的分布式数据库定义一致，关于区块链数据结构，推荐大家看一下一本详细讲解 bitcoin 技术书籍 [Mastering Bitcoin](http://uplib.fr/w/images/8/83/Mastering_Bitcoin-Antonopoulos.pdf)，你将看到，Bitcoin 的成功，不仅仅只有区块链的功劳，Game design 和密码学都是极其重要的部分！

提到那些号称颠覆银河系的新科技、新技术，就不得不提 Garter 技术成熟度曲线(The Garter hyper cycle)。区块链号称颠覆整个金融行业的既有规则、既有模式，Garter 2016 技术成熟度曲线中，我们可以在过高期望的峰值（Peak of Inflated Expectations）附近找到区块链，所以，各位同学冷静再冷静。并且 Garter 也在分析 2016 成熟度曲线中提到 [Bitcoin is the only proven blockchain](http://www.gartner.com/smarterwithgartner/3-trends-appear-in-the-gartner-hype-cycle-for-emerging-technologies-2016/)，注意这里的区块链指的是 wikipedia 版的定义。接下来笔者信口胡来，跟大家一起分析一下为什么 Bitcoin is the only proven blockchain。
<div style="text-align: center">
  <img src="resources/garter-2016.jpg"/>
</div>

Why Bitcoin is the only proven blockchain
-----------------------------------------

前面我们已经定义过，区块链是一个分布式数据库，维护持续增长的记录链表——被称为 blocks 的东西(神啊，原谅笔者蹩脚的汉语吧)，既然是分布式数据库，那么接下来这块由分布式数据库专家来写。

提到分布式数据库，肯定离不开 [CAP 理论](https://en.wikipedia.org/wiki/CAP_theorem)，CAP 是一个很有意思的理论，在分布式系统中有着霸主一样的地位。

CAP 理论：一个分布式系统最多只能同时满足一致性（Consistency）、可用性（Availability）和分区容忍性（Partition tolerance）这三项中的两项。

这三项看起来都是很好的东西，怎么不能同时满足呢？宝宝不开心，一定是架构师技术不好，没有找到更好的方式。但是，有一个坏人还给证明了，CAP 是正确的！

* 一致性 `All nodes see the same data at the same time`
* 可用性 `Reads and writes always succeed`
* 分区容忍性 `The system continues to operate despite arbitrary message loss or failure of part of the system`

我们根据 Blockchain 的工作方式(Bitcoin 中矿工网络所维护的 blockchain 的工作方式)，每个矿工节点独立的工作(不考虑矿池，会加入无谓的复杂度)，接收 Bitcoin 用户的转账请求，竞争寻找新的满足要求的 Hash 值，将这些交易打包到新的 block 并广播出去(Gossip 算法)，或者接收并验证收到的广播数据，在同一刻，各个矿工的数据并不是严格一致的（有些接收到了一个广播，有些还没有，有些接收到了另一个广播），但是每个用户的读写请求都是会成功的，只是有可能读到的数据并不是最新的，也可能不是最终的，因此这是一个满足最终一致性的 `AP` 的系统。

区块链(最起码 Bitcoin 用到的区块链)是一个完全副本的(每个矿工节点都维护一份完全都数据)、W=1, R=1 的单读单写的(客户端写成功一个矿工就算了，读一个矿工都数据就返回)、满足最终一致性的分布式数据库。完全副本带来的去中心化的好处，但是这是一剂很猛的药，理论上讲区块链所维护的数据量不能超过矿工参与者中磁盘容量最小值，否则这个矿工将要面临被退出的情况。另外受限于单个矿工的计算能力、全网的广播扩散速度，Bitcoin 限制了每 10min 一个 Block，每个 Block 1MB 的上限，使的 Bitcoin 网络的交易频率相对于 Visa、银联等低得多的多。

但是比特币依然是唯一被证实的区块链，那什么是`证实的区块链`呢？笔者网上找了好久也找不到答案，笔者又要信口胡来了，区块链是一个完全副本的对不对，要全网广播都对不对？

被证实的区块链(项目)指的是：

```
如果不能将这个项目中的区块链替换为分布式共享数据库，这个项目就是被证实的区块链
```

如果 Bitcoin 将区块链换成分布式共享数据库(变得易受攻击、篡改历史难度大大降低等)，Bitcoin 就不是目前大家看到的 Bitcoin，所以 Bitcoin 是被证实的区块链。

被证实的区块链的定义提醒了各位，在区块链的基础上设计合理的游戏规则、奖励规则，将区块链用成区块链，而不是把区块链仅仅用成了一个分布式共享数据库，这才是真正意义的区块链。

可惜的是，目前这样的项目真不多，笔者抱一下 Garter 的大腿，站在 Garter 战队：

```
Bitcoin is the only proven blockchain
```

Docker 镜像及分享
---------------

Blockchain 独角戏上演太久，大家应该迫不及待想要看到第二位主角出场了吧？

Docker 镜像(images)留学归来，操着一口浓重的伦敦音：

An image is an inert, immutable, file that's essentially a snapshot of a container. Images are created with the build command, and they'll produce a container when started with `docker run`. Images are stored in a Docker registry such as `hub.docker.com`. Because they can become quite large, images are designed to be composed of layers of other images, allowing a miminal amount of data to be sent when transferring images over the network.

本地的镜像可以通过 `docker images` 命令来查看，比如：

```shell
$> docker images
REPOSITORY                             TAG                 IMAGE ID            CREATED             SIZE
daocloud.io/daocloud/cockroach         v0.4                9845d5c4db1d        2 weeks ago         206.1 MB
daocloud.io/daocloud/spark-cluster     v0.6                9862ddb186a4        4 weeks ago         738.3 MB
daocloud.io/daocloud/dce-agent         2.0.3               3edfca3bd5aa        5 weeks ago         227.8 MB
daocloud.io/daocloud/dce               2.0.3               08a9b59123b5        5 weeks ago         27.08 MB
daocloud.io/daocloud/dce-controller    2.0.3               3bde2c3b0204        5 weeks ago         401 MB
daocloud.io/daocloud/sparrow           v0.1                f4040ff887c8        7 weeks ago         599.2 MB
daocloud.io/daocloud/dce-compose       2.0.3               e32a31fda169        8 weeks ago         21.08 MB
daocloud.io/daocloud/dce-swarm         2.0.3               55c1954cdfb4        8 weeks ago         19.49 MB
centos                                 6.8                 0cd976dc0a98        11 weeks ago        194.5 MB
daocloud.io/daocloud/hadoop-cluster    v0.5                db929fad9145        12 weeks ago        858.1 MB
daocloud.io/daocloud/zookeeper         v0.4                72d5965155da        3 months ago        567.2 MB
daocloud.io/daocloud/dce-etcd          2.0.3               e81032a59e55        5 months ago        32.29 MB
```

镜像存在镜像仓库里，通过 `docker pull` 的命令把它从仓库下载下来并通过 `docker run` 的方式启动容器。镜像开发者通过 `docker build` 命令把写好的 `Dockerfile` 以及一些二进制文件打包成镜像，然后 `docker push` 把镜像上传到镜像仓库，镜像可谓是容器技术的内容市场，心细的小伙伴可能已经发现 Docker 的布局 https://store.docker.com/ 俨然 Docker 在向乔帮主致敬啊。

但是，前段时间看到一个新闻，说是一家金融公司把文本数据放在公有云上，不可见部分被篡改了！！！公有云厂商不愿意背这个锅，有些人就咆哮，私下看人家数据太不好了，小白客户可能不知道什么是 `sha256`, `md5`, 不知道什么是加密，可是金融行业从业人员，难道不知道加密防他人读、校验防篡改吗？发散来讲，镜像也有被篡改的可能！算了，从业有先后、术业有专攻，你们安心做应用，剩下的我们来帮你搞定。

我们试图构建第二个能被证实的blockchain。

Daochain
--------

假设这样一种场景，仓库提供者与贵公司大哥八字不合，或者 Docker 公司有个家伙年终奖发少了？你的镜像是安全的吗？

```
> 刚才都锦囊我都知道，我自己存 hash 值
> 小红花戴起来，的确比小白上升了一个数量级的觉悟，但是你都同事想用你都镜像呢？
> 把hash值邮件给他，他自己下载镜像自己校验。
> 但是有一天老板给你好几天假期，你可以度假了，你还能(愿意)及时地处理邮件吗，或者说你在帮一个美女实习生调 bug。
> 公司内部共享一个共享数据库就好了嘛
> 但是每次上传或者更新镜像，你都会记得及时更新数据库吗？另外，企业间的共享怎么做？比如隔壁家一个叫 google 的公司做的镜像挺好用的。
> 怎么那么多但是，你说怎么办？
```

正式一点，目前的公共镜像仓库是建立在开发者对仓库维护者的信任的基础上的，开发者相信共有仓库的维护者不会改变他们的镜像，但是在一些极端的情况下这个假设是不存在的，比如商业竞争、黑客攻击、内部员工故意使坏等等。

用户有分享(有偿或者无偿)的需求，这正是 store.docker.com 正在布局的，有保证数据不被篡改的强烈需求。

**安全无小事**

Daocloud在反病毒，漏洞检查之后隆重推出了分布式镜像校验机制——基于区块链的技术。

简单来讲，用户A在上传镜像到共有仓库的同时，会将hash值上传到区块链上，DaoCloud 与众多区块链对维护者共同维护这条区块链（移除了开发者对集中化管理者的信任假设），保证任何人对区块链对非法篡改都不会得逞，正常的数据读写得到满足。用户 B 凭借对用户 A 的信任(比如声望很好的大公司，比如阿里、Google 或者公司同事)从共有仓库获取 Docker 镜像，同时从区块链中读取该镜像的 Hash 值，本地验证。

我们是不是 the second proven blockchain 呢？欢迎大家来讨论！

镜像分享经济
----------

最近火热了一把的共享经济，IT 行业又有着不重复造轮子的原则，区块链的 Hash 值标示了 Author 对该镜像对著作权，镜像的共享经济值得我们共同期待。

内测及奖励
--------

