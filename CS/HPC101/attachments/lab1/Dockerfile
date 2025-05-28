FROM dockerhub.zjusct.io/library/ubuntu:25.10 AS build
# 安装依赖
RUN apt-get update  && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    build-essential \
    wget \
    openssh-server \
    openmpi-bin \
    libopenmpi-dev \
    libopenblas-dev \
        iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# 安装 HPL
WORKDIR /opt
COPY ./hpl-2.3.tar.gz .
RUN tar xvf hpl-2.3.tar.gz && rm hpl-2.3.tar.gz

# 编译 HPL
WORKDIR /opt/hpl-2.3
RUN ./configure --prefix=/usr/local/hpl LDFLAGS="-lm" LIBS="-lm" 
RUN make && make install

RUN useradd -m hpl && echo "hpl:hpl" | chpasswd
RUN chown -R hpl:hpl /usr/local/hpl

# 创建工作目录
WORKDIR /home/hpl
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh #entrypoint将会处理ssh服务

COPY ./ssh /home/hpl/.ssh
RUN chmod 700 /home/hpl/.ssh && chmod 600 /home/hpl/.ssh/* && chown -R hpl:hpl /home/hpl/.ssh

EXPOSE 22
ENTRYPOINT ["./entrypoint.sh"]