# rule-set

适用于 Shadowrocket 的分流规则。

## OpenAI

在现有配置的 `[Rule]` 里加入以下一行，按需把 `PROXY` 换成你的策略组名称。

```ini
RULE-SET,https://raw.githubusercontent.com/scubers/rule-set/main/shadowrocket/openai.list,PROXY
```

放在通用 AI、代理、GEOIP 和 FINAL 之前。首页「全局路由」选择「配置」。

包含 ChatGPT、Codex、API、Sora 及登录验证域名。核心域名参考 [OpenAI 网络建议](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)，动态 CDN 使用关键字规则，共享服务仅保留精确主机名。

## Claude

在现有配置的 `[Rule]` 里加入以下一行，按需把 `Claude-Japan` 换成你的策略组名称。

```ini
RULE-SET,https://raw.githubusercontent.com/scubers/rule-set/main/shadowrocket/claude.list,Claude-Japan
```

放在直连例外、广告拦截之后，通用 AI、代理、GEOIP 和 FINAL 之前。首页「全局路由」选择「配置」。

域名基于 v2fly 的 Anthropic 列表，并补充 Claude 使用的精确主机名。IP 段按 Anthropic 公布的 API 和 Console 入站范围整理，核对于 2026-11-18。 [v2fly Anthropic 规则](https://github.com/v2fly/domain-list-community/blob/6766d09f4a951f4f11d822891a9736606cd910ac/data/anthropic) · [上游 MIT 许可证](LICENSE.v2fly) · [Anthropic 官方 IP 列表](https://platform.claude.com/docs/zh-CN/api/ip-addresses)

## Shadowrocket 场景配置

先在 Shadowrocket 中保留名为 `lazy_group.conf` 的[底层配置](https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/lazy_group.conf)，再导入两份扩展配置。两份都直接引用 `lazy_group.conf`，共用 DNS、Claude、OpenAI 和普通流量规则。

| 场景 | 配置 | 家庭网络 |
|---|---|---|
| 家庭 Wi‑Fi | [extended-home.conf](shadowrocket/extended-home.conf) | `jr-router.com` 和 `jr-nas.com` 直连 |
| 默认、蜂窝 | [extended-outside.conf](shadowrocket/extended-outside.conf) | `jr-router.com`、`jr-nas.com` 和 `192.168.18.0/24` 通过 `WIREGUARD-HOME` |

在「首页 → 全局路由 → 场景设置」将家庭 Wi‑Fi 绑定家庭版，将默认场景和已有的蜂窝场景绑定外出版。保存后将全局路由选为「场景」。外出版需要已有的 `WIREGUARD-HOME` 节点或策略组。

共用配置只改 `extended-home.conf`，然后在仓库根目录运行 `python3 shadowrocket/generate-outside.py` 更新外出版。用 `python3 shadowrocket/generate-outside.py --check` 检查两份是否同步。维护外出专用的回家规则和旁路设置时，在生成器中修改。更新底层配置后，核对它的 `skip-proxy` 和 `tun-excluded-routes` 是否有变化。
