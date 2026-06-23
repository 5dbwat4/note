【本文由人类撰写】

把公司的API反代到本地来用。

使用的是经典cloudflared。

以下是踩坑：
1. 要配hostname。

只有这里有高级配置，
https://dash.cloudflare.com/:user/one/networks/connectors/

而networking->tunnel（https://dash.cloudflare.com/:user/tunnels）里面可以添加tunnel，但是没有高级配置。

这个很重要，因为有的时候对方会有Host验证，然后你自己的host过不了，会被nginx拦下来

2. 别的配置照着操作即可