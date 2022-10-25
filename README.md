# PYPSI
We have implemented the PSI application based on national secrets based on the [KKRT16](https://eprint.iacr.org/2016/799) protocol
## 源码基础
本项目基于[Delta PSI - github](https://github.com/delta-mpc/python-psi)以及国密开源算法库[hggm](https://gitee.com/basddsa/hggm/tree/master)进行开发，诚挚对他们表示感谢。
## 部署流程
* 进入`pypsi`文件夹，按照md文件所写完成`pypsi`库的安装，若要测试的话，可以按照md文件的指引进行测试。
* 进入`app`文件夹，运行`python3 manage.py runserver`可以启动web应用，并在网址`http://127.0.0.1:8000/client`访问主应用。
## 运行依赖
* 安装pypsi的依赖库在对应的md文件中介绍
* 运行web应用时，须先安装`django`和`mysql`
