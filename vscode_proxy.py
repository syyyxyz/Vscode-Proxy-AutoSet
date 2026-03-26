import sys
import os

#用户名是 LEGION。根据你的需要改
settings_path = r"C:\Users\LEGION\AppData\Roaming\Code\User\settings.json"

# 这里需要替换为你魔法代理的 IP 和端口，通常是 127.0.0.1:xxxx
PROXY_URL = "socks5://127.0.0.1:1080" 

def modify_proxy(enable_proxy):
    if not os.path.exists(settings_path):
        print("未找到 settings.json 文件，请检查路径。")
        return

    with open(settings_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    proxy_exists = False

    for line in lines:
        # 匹配配置项，无论原来设置了什么值
        if '"http.proxy"' in line and not line.strip().startswith("//"):
            proxy_exists = True
            if enable_proxy:
                # 写入带代理的配置
                new_lines.append(f'    "http.proxy": "{PROXY_URL}",\n')
            else:
                # 写入空字符串代表关闭代理（VSCode 官方机制）
                new_lines.append(f'    "http.proxy": "",\n')
        else:
            new_lines.append(line)

    # 如果原来没有这个配置项，且本次要求开启，则插入到第一行的大括号下面
    if enable_proxy and not proxy_exists:
        new_lines.insert(1, f'    "http.proxy": "{PROXY_URL}",\n')

    # 写回文件
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    # 接收命令行参数：on 代表开启，off 代表关闭
    if len(sys.argv) > 1 and sys.argv[1].lower() == "on":
        modify_proxy(True)
        print("VSCode 代理已 [开启]")
    else:
        modify_proxy(False)
        print("VSCode 代理已 [关闭]")