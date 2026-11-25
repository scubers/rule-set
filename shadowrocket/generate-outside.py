import argparse
import re
from pathlib import Path


CONFIG_DIR = Path(__file__).resolve().parent
BASE_INCLUDE = 'include = lazy_group.conf\n'

# 192.168.0.0/16 扣除家庭网段 192.168.18.0/24。
OTHER_LAN_RANGES = (
    '192.168.0.0/20,192.168.16.0/23,192.168.19.0/24,192.168.20.0/22,'
    '192.168.24.0/21,192.168.32.0/19,192.168.64.0/18,192.168.128.0/17'
)
OUTSIDE_BYPASS = (
    '\n# 外出时让家庭网段进入规则匹配，其余地址沿用底层配置的旁路范围。\n'
    f'skip-proxy = {OTHER_LAN_RANGES},10.0.0.0/8,172.16.0.0/12,localhost,*.local,'
    'captive.apple.com,*.ccb.com,*.abchina.com.cn,*.psbc.com,www.baidu.com,www.163.com\n'
    'tun-excluded-routes = 10.0.0.0/8,127.0.0.0/8,169.254.0.0/16,172.16.0.0/12,'
    f'192.0.0.0/24,192.0.2.0/24,192.88.99.0/24,{OTHER_LAN_RANGES},'
    '198.51.100.0/24,203.0.113.0/24,224.0.0.0/4,255.255.255.255/32,239.255.255.250/32,ff02::fb/128\n'
)


def replace_line(config, line, replacement):
    lines = config.splitlines(keepends=True)
    if lines.count(line) != 1:
        raise SystemExit(f'extended-home.conf 应恰好包含一行 {line.strip()}')
    lines[lines.index(line)] = replacement
    return ''.join(lines)


def main():
    parser = argparse.ArgumentParser(description='从通用配置生成 Shadowrocket 外出配置。')
    parser.add_argument('--check', action='store_true', help='检查外出配置是否与生成结果一致')
    args = parser.parse_args()

    general = (CONFIG_DIR / 'extended-home.conf').read_text(encoding='utf-8')
    if len(re.findall(r'(?im)^\s*include\s*=', general)) != 1:
        raise SystemExit('extended-home.conf 应只引用 lazy_group.conf')
    if re.search(r'(?im)^\s*(skip-proxy|tun-excluded-routes)\s*=', general):
        raise SystemExit('通用配置改了旁路列表，请同步核对生成器中的外出旁路设置')

    outside = replace_line(general, '[General]\n', '[General]\n# 由 generate-outside.py 生成。\n')
    outside = replace_line(outside, BASE_INCLUDE, BASE_INCLUDE + OUTSIDE_BYPASS)
    outside = replace_line(outside, 'DOMAIN-SUFFIX,jr-router.com,DIRECT\n', 'DOMAIN-SUFFIX,jr-router.com,WIREGUARD-HOME\n')
    outside = replace_line(
        outside,
        'DOMAIN-SUFFIX,jr-nas.com,DIRECT\n',
        'DOMAIN-SUFFIX,jr-nas.com,WIREGUARD-HOME\nIP-CIDR,192.168.18.0/24,WIREGUARD-HOME,no-resolve\n',
    )

    output = CONFIG_DIR / 'extended-outside.conf'
    if args.check:
        if not output.is_file() or output.read_bytes() != outside.encode('utf-8'):
            raise SystemExit('外出配置有差异，请运行 python3 shadowrocket/generate-outside.py')
    else:
        output.write_text(outside, encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
