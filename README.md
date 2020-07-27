simple python project template

- successor of [cookiecutter-docker-science](https://git.datagrand.com/humeng/cookiecutter-docker-science)
- keep it simple
- you can fork it and modify it
- work in process


# how to use

1. 将`src` 修改成项目的名称
2. 修改 git remote 地址 `git remote set-url origin new-git-remote-url`
3. `git add . && git commit -m "init the new project" && git push -u origin master`

# 如何设置开发环境

1. 按照你的需求修改 `./scripts/setup_venv_examples.bash`, 此脚本用来创建本地虚拟 python 环境
2. 开发时, 如果要添加依赖, 请加入到`requirements/requirements.in` 或者`./requirements/dev-requirements.in` 中, 开发时, 运行`./scripts/gen_deps.bash` 来更新依赖并安装依赖
3. 部署时, 直接`pip install requirements.txt && pip install dev-requirements.txt` 来安装依赖
4. 注意, `.envrc`中包含了一些环境变量, 此文件不会自动执行, 可以`source .envrc`  或者 使用`direnv` 来每次进入此文件夹时自动运行


# TODO
- [ ] 在线服务部分需要未测试, 需要重新写
- [ ] 持续集成, 持续部署
- [ ] 支持`setup.py`, 支持`pip install`安装项目

