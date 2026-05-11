核心流程AI都能写。这里主要是踩坑记录（虽然暂时还没有踩坑）（好吧非常顺畅，一点坑都没有）

# Nginx 无 sudo 编译安装指南

> 目标安装路径: `$HOME/nginx-app`

## 适用场景

远程服务器上没有 root/sudo 权限，需要将 nginx 安装到用户自有目录。

---

## 1. 安装依赖

编译 nginx 至少需要以下依赖的 **开发库**（需联系管理员安装，或使用已有环境）：

```bash
# Debian / Ubuntu
apt install gcc make libpcre3-dev zlib1g-dev

# CentOS / RHEL / Fedora
yum install gcc make pcre-devel zlib-devel
```

> 如果没有开发库可用，可改用 `--with-pcre=DIR` / `--with-zlib=DIR` 指定源码路径静态编译，见 [附录 A](#附录-a用源码编译依赖)。

---

## 2. 配置

在 nginx 源码根目录执行 `configure`，将全部路径指向 `$HOME/nginx-app`：

```bash
./configure \
  --prefix=$HOME/nginx-app \
  --sbin-path=$HOME/nginx-app/sbin/nginx \
  --modules-path=$HOME/nginx-app/modules \
  --conf-path=$HOME/nginx-app/conf/nginx.conf \
  --pid-path=$HOME/nginx-app/logs/nginx.pid \
  --lock-path=$HOME/nginx-app/logs/nginx.lock \
  --error-log-path=$HOME/nginx-app/logs/error.log \
  --http-log-path=$HOME/nginx-app/logs/access.log \
  --http-client-body-temp-path=$HOME/nginx-app/temp/client_body \
  --http-proxy-temp-path=$HOME/nginx-app/temp/proxy \
  --http-fastcgi-temp-path=$HOME/nginx-app/temp/fastcgi \
  --http-uwsgi-temp-path=$HOME/nginx-app/temp/uwsgi \
  --http-scgi-temp-path=$HOME/nginx-app/temp/scgi \
  --user=$(whoami) \
  --group=$(id -gn)
```

### 可选模块

| 用途         | 配置项                          |
| ------------ | ------------------------------- |
| HTTPS / TLS  | `--with-http_ssl_module`        |
| HTTP/2       | `--with-http_v2_module`         |
| Stream 代理  | `--with-stream`                 |
| 状态监控     | `--with-http_stub_status_module` |
| 编译调试版本 | `--with-debug`                  |

> 启用 SSL 需要 OpenSSL 开发库（`libssl-dev` / `openssl-devel`）或 `--with-openssl=DIR`。

---

## 3. 编译

```bash
make -j$(nproc)
```

编译产物 `objs/nginx` 即为可执行文件。

---

## 4. 安装

```bash
make install
```

安装完成后目录结构：

```
$HOME/nginx-app/
├── sbin/nginx          # 可执行文件
├── conf/nginx.conf     # 配置文件
├── modules/            # 动态模块
├── logs/               # 日志目录
│   ├── error.log
│   └── access.log
└── temp/               # 临时文件目录
```

---

## 5. 创建运行时目录

某些目录不会自动创建，手动补上：

```bash
mkdir -p $HOME/nginx-app/temp/{client_body,proxy,fastcgi,uwsgi,scgi}
```

---

## 6. 修改端口（重要）

非 root 用户无法绑定 1024 以下的端口（如 80 / 443）。

```bash
sed -i 's/listen\s*80;/listen 8080;/' $HOME/nginx-app/conf/nginx.conf
```

> 需要 HTTPS 同理，把 `listen 443 ssl;` 改为 `listen 8443 ssl;`。

---

## 7. 启动 / 管理

```bash
# 启动
$HOME/nginx-app/sbin/nginx

# 验证是否运行
curl http://localhost:8080

# 重载配置 (不停机)
$HOME/nginx-app/sbin/nginx -s reload

# 优雅停止
$HOME/nginx-app/sbin/nginx -s quit

# 立即停止
$HOME/nginx-app/sbin/nginx -s stop

# 测试配置文件语法
$HOME/nginx-app/sbin/nginx -t
```

---

## 8. 设为系统服务（需要管理员协助）

以下 systemd 用户级 service 文件，无需 sudo 即可使用：

```bash
mkdir -p $HOME/.config/systemd/user
cat > $HOME/.config/systemd/user/nginx.service << 'EOF'
[Unit]
Description=NGINX (User)
After=network.target

[Service]
Type=forking
PIDFile=%h/nginx-app/logs/nginx.pid
ExecStart=%h/nginx-app/sbin/nginx
ExecReload=%h/nginx-app/sbin/nginx -s reload
ExecStop=%h/nginx-app/sbin/nginx -s quit
PrivateTmp=true

[Install]
WantedBy=default.target
EOF

# 启用
systemctl --user daemon-reload
systemctl --user enable nginx
systemctl --user start nginx
```

> 注意：用户级 service 在用户登出后默认会停止，需管理员执行 `loginctl enable-linger <username>` 解决。

---

## 附录 A：用源码编译依赖

当系统没有 pcre / zlib / openssl 开发库时，下载源码让 nginx 静态编译：

```bash
# 下载依赖源码到 nginx 同级目录
cd $(dirname $(pwd))

wget https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.44/pcre2-10.44.tar.gz
tar xzf pcre2-10.44.tar.gz

wget https://zlib.net/zlib-1.3.1.tar.gz
tar xzf zlib-1.3.1.tar.gz

wget https://www.openssl.org/source/openssl-3.3.1.tar.gz
tar xzf openssl-3.3.1.tar.gz

# 回到 nginx 源码目录，重新 configure 加上这些参数：
cd nginx-1.30.0
./configure \
  ...
  --with-pcre=../pcre2-10.44 \
  --with-zlib=../zlib-1.3.1 \
  --with-openssl=../openssl-3.3.1 \
  --with-http_ssl_module
```

---

## 附录 B：一键脚本

源码目录已提供 `compile.sh`，直接运行即可完成配置 + 编译 + 安装全流程。

```bash
chmod +x compile.sh
./compile.sh
```
