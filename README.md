# rule-set

适用于 Shadowrocket 的分流规则。

## Claude

在现有配置的 `[Rule]` 里加入以下一行，按需把 `Claude-Japan` 换成你的策略组名称。

```ini
RULE-SET,https://raw.githubusercontent.com/scubers/rule-set/main/shadowrocket/claude.list,Claude-Japan
```

放在直连例外、广告拦截之后，通用 AI、代理、GEOIP 和 FINAL 之前。首页「全局路由」选择「配置」。也可将 [claude.conf](shadowrocket/claude.conf) 的规则合并到现有配置。

域名基于 v2fly 的 Anthropic 列表，并补充 Claude 使用的精确主机名。IP 段按 Anthropic 公布的 API 和 Console 入站范围整理，核对于 2026-11-18。 [v2fly Anthropic 规则](https://github.com/v2fly/domain-list-community/blob/6766d09f4a951f4f11d822891a9736606cd910ac/data/anthropic) · [上游 MIT 许可证](LICENSE.v2fly) · [Anthropic 官方 IP 列表](https://platform.claude.com/docs/zh-CN/api/ip-addresses)
