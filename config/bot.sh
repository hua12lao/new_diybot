#!/usr/bin/env bash

if [ ! -d "/ql" ];then
  root=/jd
else
  root=/ql/data
fi

dir_jbot=$root/jbot
dir_diybot=$root/repo/diybot
file_bot=$root/config/bot.json
file_botset=$root/config/botset.json
file_diybotset=$root/config/diybotset.json
url="https://github.com/hua12lao/new_diybot.git"

git_clone() {
    local url=$1
    local dir=$2
    local branch=$3
    [[ $branch ]] && local cmd="-b $branch "
    echo "开始克隆仓库 $url 到 $dir"
    git clone $cmd $url $dir
    exit_status=$?
}

backup() {
  if [ ! -d $root/repo/backup ]; then
    mkdir $root/repo/backup
  fi
  mkdir $root/repo/backup/$(date +\%m\%d\%H\%M)
  cp -rf $root/jbot/* $root/repo/backup/$(date +\%m\%d\%H\%M) 2> /dev/null
  rm -rf $root/jbot/* 2> /dev/null
  cd $root
}

env() {
  echo "1、安装bot依赖..."
  apk --no-cache add -f zlib-dev gcc jpeg-dev python3-dev musl-dev freetype-dev
  echo -e "bot依赖安装成功...\n"
  cd $root || exit
}

bot() {
  echo "2、下载bot所需文件..."
  if [ -d ${dir_diybot} ]; then
    rm -rf $dir_diybot
  fi
  git_clone ${url} ${dir_diybot} "main"
  if [ ! -d $dir_jbot ]; then
    mkdir $dir_jbot
  fi
  if [ -f $dir_jbot/diy/user.py ]; then
    mv -f $dir_jbot/diy/user.py $dir_diybot/jbot/diy/
    echo "存在user.py, 不更新user.py"
  else
    rm -f $dir_diybot/jbot/diy/user.py
    echo "不存在user.py，或是首次安装，请安装完bot再单独部署user"
  fi
  if [ -d ${dir_jbot} ]; then
    backup
  fi

  if [ -f $dir_jbot/diy/diy.py ]; then
    rm -f $dir_diybot/jbot/diy/diy.py
  fi
  cp -rf $dir_diybot/jbot/* $dir_jbot
  echo -e "bot文件下载成功...\n"
  if [[ ! -f $file_bot ]]; then
    cp -f $dir_diybot/config/bot.json $root/config
  fi
  if [[ ! -f $file_botset ]]; then
    cp -f $dir_diybot/jbot/set.json $root/config
    mv -f $root/config/set.json $root/config/botset.json
  else
    sed -i 's/user": "True"/user": "False"/' $file_botset
    echo -e "默认关闭user监控，请部署user后执行 /user 手动开启！\n"
  fi
  if [[ ! -f $file_diybotset ]]; then
    cp -f $dir_diybot/config/diybotset.json $root/config
  fi
  cd $root || exit
}

packages() {
  echo "3、安装python3依赖..."
  cd $dir_jbot || exit
  /usr/bin/python3 -m pip install --upgrade pip
  pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
  pip3 --default-timeout=100 install -r requirements.txt --no-cache-dir
  echo -e "python3依赖安装成功...\n"
  cd $root || exit
}

start() {
  echo "4、启动bot程序..." 
  dir_log=$root/log/bot
  echo "检测 $dir_log 目录"
  if [ ! -d $dir_log ]
    then echo "  └—结果：不存在，新建"
    mkdir $dir_log
  else
    echo "  └—结果：存在，跳过"
  fi
  if [[ -z $(grep -E "123456789" $file_bot) ]]; then
    if [ -d "/ql" ]; then
        ps -ef | grep "python3 -m jbot" | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null
        nohup python3 -m jbot >$root/log/bot/bot.log 2>&1 &
        echo -e "bot启动成功...\n"
    else
        cd $dir_jbot
        pm2 start ecosystem.config.js
        # cd $root
        # pm2 restart jbot
        echo -e "bot启动成功...\n"
    fi
  else
    echo "配置 $file_bot 后再次运行本程序即可启动机器人"
  fi
}

main() {
  env
  bot
  packages
  start
}

main
exit 0
