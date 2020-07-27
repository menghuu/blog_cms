#!/usr/bin/env bash

set -e
port=52004
commit_id='no_git'
git rev-parse --short HEAD >/dev/null 2>&1 && commit_id=$(git rev-parse --short HEAD)

docker_version=${commit_id}_$(date "+%Y_%m_%d_%H")
docker_dep_version=${docker_version}_deps


datagrand_url_prefix='dockerhub.datagrand.com/shisuo/shisuo_event_extractor'
dep_datagrand_url_prefix='dockerhub.datagrand.com/shisuo/shisuo_event_extractor'

shisuo_url_prefix='hub.cloud.com/app/qbjs_shisuo_event_extractor'
dep_shisuo_url_prefix='hub.cloud.com/default/qbjs_shisuo_event_extractor'


dep_datagrand_url=${dep_datagrand_url_prefix}:${docker_dep_version}
datagrand_url=${datagrand_url_prefix}:${docker_version}

dep_shisuo_url=${dep_shisuo_url_prefix}:${docker_dep_version}
shisuo_url=${shisuo_url_prefix}:${docker_version}

dep_datagrand_docker_file='Dockerfile.deps'
datagrand_docker_file='Dockerfile.finnal'
shisuo_docker_file='Dockerfile.finnal.shisuo'


cat >${dep_datagrand_docker_file} <<EOF
FROM python:3.6
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --index https://mirrors.aliyun.com/pypi/simple/

EXPOSE 52004

EOF
echo 制作依赖镜像
docker build -t ${dep_datagrand_url} -f ./${dep_datagrand_docker_file} .
docker build -t ${dep_shisuo_url} -f ./${dep_datagrand_docker_file} .
echo 成功制作了依赖镜像 ${dep_datagrand_url} 和 ${dep_shisuo_url}
echo -n 是否push依赖镜像[y/n]:
read pushornot
if [[ $pushornot == 'y' ]]; then
  docker push ${dep_datagrand_url}
fi


cat >${datagrand_docker_file} <<EOF
FROM ${dep_datagrand_url}

COPY . .
CMD [ "bash", "./scripts/deploy_services.bash" ]
EOF
docker build -t ${datagrand_url} -f ./${datagrand_docker_file} .
echo 成功制作了应用镜像 ${datagrand_url}
echo -n 是否push应用镜像[y/n]:
read pushornot
if [[ $pushornot == 'y' ]]; then
  docker push ${datagrand_url}
fi


cat >${shisuo_docker_file} <<EOF
FROM ${dep_shisuo_url}

COPY . .
CMD [ "bash", "./scripts/deploy_services.bash" ]
EOF
echo $shisuo_url, $shisuo_docker_file
docker build -t ${shisuo_url} -f ./${shisuo_docker_file} .

echo
echo 如果没有选择push镜像, 那么, 可以自行执行下述的命令
echo docker push ${dep_datagrand_url}
echo docker push ${datagrand_url}
echo '============='
echo
echo

echo 十所内部的docker镜像永远不会被自动push, 如果有需要, 自行push下列的docker镜像
echo docker push ${dep_shisuo_url}
echo docker push ${shisuo_url}
echo
echo

echo 构建docker compose 文件

cat >/tmp/tmpdockercompose.yml <<EOF
version: '3.3'
services:
  shisuo_event_extractor:
    image: ${datagrand_url}
    #image: ${shisuo_url}
    container_name: shisuo_event_extractor
    ports:
      - $port:$port
    volumes:
      - ./configs:/usr/src/app/configs
#    network_mode: 'host'
EOF

echo 新的docker compose 文件 ./docker-compose.yml的内容应该是:
cat /tmp/tmpdockercompose.yml
echo
echo

echo -n 是否构建新的docker compose 文件[y/n]:
read rewritedockercompose

if [[ $rewritedockercompose == 'y' ]]; then
  echo 即将写入文件 ./docker-compose.yml
  cat /tmp/tmpdockercompose.yml >./docker-compose.yml
fi

echo
echo 如果没有将新的内容写入到docker compose文件中, 可以手动向
echo ./docker-compose.yml
echo
echo 中写入:
echo
cat /tmp/tmpdockercompose.yml
echo


echo -n 是否保存docker image, 只保存十所要求的镜像, 达观本地的不会保存为文件[y/n]
read writedockerimage

if  [[ $writedockerimage == 'y' ]]; then
  echo 即将将docker image保存到文件
  docker save $dep_shisuo_url | gzip > docker/images/$docker_dep_version.tar.gz
  echo success save $dep_shisuo_url into docker/images/$docker_dep_version.tar.gz

  docker save $shisuo_url | gzip > docker/images/$docker_version.tar.gz
  echo success save $shisuo_url into docker/images/$docker_version.tar.gz
fi
