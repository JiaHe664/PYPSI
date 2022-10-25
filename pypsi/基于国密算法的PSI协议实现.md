## 基于国密算法的PSI协议实现

### 理论基础

* Effificient Batched Oblivious PRF with Applications to Private Set（CCS '16: Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security）
* 参考链接

  [Mike Rosulek系列课程笔记整理(完结): 不经意传输及其优化]()

* 开源代码（python）
	[python-psi（github）](https://github.com/delta-mpc/python-psi)

### 国密算法

​	基于开源国密算法包[hggm](https://gitee.com/basddsa/hggm)实现，加速工具为numba

* SM2（使用加速版SM2实现）
  * 生成base-OT中所需的公私钥对
  * 提供密钥派生器，生成流密码中所需的随机密钥流
* SM3（使用加速版SM3实现）
  * 为cuckoo哈希（布谷鸟哈希）、编码和sm2提供支持

### 部署步骤

* 安装 [python-psi](https://github.com/delta-mpc/python-psi)
* 安装 [snowland-smx](https://github.com/ASTARCHEN/snowland-smx-python)

* 安装 [gmssl](https://github.com/duanhongyi/gmssl)

* 安装 [numba](https://numba.readthedocs.io/en/stable/user/installing.html)（需要先安装 [conda](https://zhuanlan.zhihu.com/p/459607806)）

### 运行

```bash
# 进入本项目根目录，运行安装命令
pip3 install .

# 初始化配置文件
psi_run init

# 启动PSI-Server
PSI_CONFIG=config/server.config.yaml psi_run server 127.0.0.1:2345

# 另外在项目根目录处再开一个新端口，启动PSI-Client
PSI_CONFIG=config/client.config.yaml psi_run client 127.0.0.1:1234

```

