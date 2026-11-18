# rule-set

适用于 Shadowrocket 的分流规则。

## Claude

在现有配置的 `[Rule]` 里加入以下一行，按需把 `Claude-Japan` 换成你的策略组名称。

```ini
RULE-SET,https://raw.githubusercontent.com/scubers/rule-set/main/shadowrocket/claude.list,Claude-Japan
```

放在直连例外、广告拦截之后，通用 AI、代理、GEOIP 和 FINAL 之前。首页「全局路由」选择「配置」。

域名基于 v2fly 的 Anthropic 列表，并补充 Claude 使用的精确主机名。IP 段按 Anthropic 公布的 API 和 Console 入站范围整理，核对于 2026-11-18。 [v2fly Anthropic 规则](https://github.com/v2fly/domain-list-community/blob/6766d09f4a951f4f11d822891a9736606cd910ac/data/anthropic) · [上游 MIT 许可证](LICENSE.v2fly) · [Anthropic 官方 IP 列表](https://platform.claude.com/docs/zh-CN/api/ip-addresses)

### 使用 `lazy_group.conf` 的拓展配置

[下载 local-extended.conf](https://raw.githubusercontent.com/scubers/rule-set/main/shadowrocket/local-extended.conf)。将它与已有的 `lazy_group.conf` 放在同一个 Shadowrocket 配置目录，在 Shadowrocket 首页选择代理节点，`CLAUDE` 通过内置 `PROXY` 使用该节点。远程 Claude 规则指向 `CLAUDE`，`router.com` 和 `nas.com` 走直连。
