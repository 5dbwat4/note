#!/bin/bash

# 生成 SSH 密钥
# if [ ! -f ~/.ssh/id_rsa ]; then
#     ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
#     cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
#     chmod 600 ~/.ssh/authorized_keys
# fi

# 更新 hosts 文件
echo "127.0.0.1 localhost" > /etc/hosts
echo "$(hostname -i) $(hostname)" >> /etc/hosts

# 添加其他节点
if [ -n "$HOSTS" ]; then
    echo "$HOSTS" >> /etc/hosts
fi

# 启动 SSH 服务
service ssh start -D  

bash