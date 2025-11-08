import os
import random
import re
import json
import importlib
from datetime import datetime
from typing import List, Dict
from mcdreforged.api.all import *

# 插件服务器接口实例
__mcdr_server: PluginServerInterface
CONFIG_FILE = os.path.join('config', 'chat_menu.json')  # 配置文件路径

nbtlib = None  # 用于加载NBT数据的库

# 默认配置内容
default_config = {
    "trigger_command": "w",  # 触发命令，默认为w，即!w
    "message": [
        "<text>§a哔哩哔哩关注：角落里的菌，谢谢喵</text>",
        "<text>§b这是随机文本喵→ {random_text} {random_text_1} </text>",
        "<url(v=https://space.bilibili.com/591893685)(h=快关注!)>§c点我打开哔哩主页喵</url>",
        "<copy(v=https://github.com/JunjunSub/ChatMenu)(h=快Star!)>§d点我复制插件链接到剪贴板喵</copy>",
        "<command(v=/ping)(h=查看连接延迟)>§e点我运行指令喵</command>",
        "<fill(v=猪务器已存活 {date} 游戏已运行 {date_nbt} 天!)(h=泰铢勒弥)>§f点我填充当前服务器运行天数瞄</fill>"
    ],
    "sub_menus": {
        "ms1": {
            "message": [
                "<text>这是子菜单1</text>"
            ],
            "comment": "这是子菜单1的介绍喵"
        },
        "ms2": {
            "message": [
                "<text>这是子菜单2</text>"
            ],
            "comment": "这是子菜单2的介绍喵"
        }
    },
    "random_text": {
        "random_text": [
            "旮旯game不是这样的！",
            "咕咕嘎嘎"
        ],
        "random_text_1": [
            "阿巴阿巴",
            "摩西摩西"
        ]
    },
    "server_start_date": "2023-11-04",  # 服务器启动日期
    "nbt_mode": True,  # 是否启用NBT模式
    "nbt_file": "server/world/level.dat"  # NBT数据文件路径
}

# 全局变量
config = {}
main_menu_info = []
sub_menus_info = {}
trigger_command = "w"  # 默认触发命令

# 发送消息给玩家或全体玩家
def send_message(server: PluginServerInterface, messages: RTextList, scope: str, player: str = None):
    if scope == "player":
        server.tell(player, messages)  # 发送给单个玩家
    elif scope == "all":
        server.say(messages)  # 发送给所有玩家

# 获取服务器运行的天数
def get_day_count() -> int:
    global nbtlib
    try:
        if config["nbt_mode"]:
            if nbtlib is None:
                nbtlib = importlib.import_module("nbtlib")  # 导入NBT库
            # 通过NBT文件获取服务器运行的时间（单位为天）
            return int(nbtlib.load(config["nbt_file"])["Data"]["Time"] / 1728000)
        # 如果没有启用NBT模式，通过启动日期计算天数
        return (datetime.now() - datetime.strptime(config["server_start_date"], r"%Y-%m-%d")).days
    except Exception as e:
        print(e)
        return -1

# 格式化消息，将占位符替换为实际内容
def format_message(message: str, player: str) -> str:
    if message is not None:
        placeholders = re.findall(r'\{(\w+)}', message)  # 查找所有占位符
        for placeholder in placeholders:
            if placeholder == "player":
                value = player
            elif placeholder == "date":
                value = str((datetime.now() - datetime.strptime(config["server_start_date"], "%Y-%m-%d")).days)
            elif placeholder == "date_nbt":
                value = str(get_day_count())
            elif placeholder in config["random_text"]:
                value = random.choice(config["random_text"][placeholder])  # 从随机文本中选择一项
            else:
                value = f"{{{placeholder}}}"  # 保留未识别的占位符
            message = message.replace("{" + placeholder + "}", value)  # 替换占位符
    return message

# 将消息转换为RTextList格式
def msg_to_rtextlist(row: List[Dict], player: str) -> RTextList:
    rtextlist = RTextList()

    for unit in row:
        tag_type = unit.get('tag_type')  # 标签类型
        content = unit.get('content')  # 内容
        value = unit.get('value')  # 值
        hover = unit.get('hover')  # 悬停文本
        content = format_message(content, player)  # 格式化内容
        value = format_message(value, player)  # 格式化值
        hover = format_message(hover, player)  # 格式化悬停文本
        # 根据标签类型创建不同的RText对象
        if tag_type == "url" or tag_type == "u":
            rtext = RText(content).c(RAction.open_url, value)
        elif tag_type == "copy" or tag_type == "c":
            rtext = RText(content).c(RAction.copy_to_clipboard, value)
        elif tag_type == "command" or tag_type == "cmd":
            rtext = RText(content).c(RAction.run_command, value)
        elif tag_type == "fill" or tag_type == "f":
            rtext = RText(content).c(RAction.suggest_command, value)
        else:
            rtext = RText(content)
        if hover is not None:
            rtext.h(hover)  # 添加悬停文本
        rtextlist += rtext  # 将RText添加到RTextList
    return rtextlist

# 创建并发送消息
def create_and_send_message(server: PluginServerInterface, message_list: List[List[Dict]], scope: str, player: str):
    for row in message_list:
        rtextlist = msg_to_rtextlist(row, player)  # 转换为RTextList格式
        send_message(server, rtextlist, scope, player)  # 发送消息

# 打开菜单（主菜单或子菜单）
def open_menu(source: CommandSource, sub_menu_name: str = None):
    if source.is_console:
        source.reply("该指令只能由玩家执行")  # 控制台不可执行
        return
    server = source.get_server()
    if sub_menu_name:
        if sub_menu_name not in sub_menus_info:
            source.reply(f"子菜单 '{sub_menu_name}' 不存在")  # 子菜单不存在
            return
        create_and_send_message(server.as_plugin_server_interface(),
                                sub_menus_info[sub_menu_name],
                                "player",
                                source.player)  # 发送子菜单
    else:
        create_and_send_message(server.as_plugin_server_interface(),
                                main_menu_info,
                                "player",
                                source.player)  # 发送主菜单

# 列出所有子菜单
def list_sub_menus(source: CommandSource):
    if source.is_console:
        source.reply("该指令只能由玩家执行")
        return
    server = source.get_server()
    sub_menu_list = []
    if sub_menus_info:
        sub_menu_list.append([{"tag_type": "text", "content": "§7---------- §eSubmenu list §r§7----------"}])
        for submenu_name, submenu_info in sub_menus_info.items():
            comment = config["sub_menus"].get(submenu_name, {}).get("comment", "")
            sub_menu_list.append([{"tag_type": "cmd", "content": f"§b[{submenu_name}] §7注释:{comment}", "value": f"!{trigger_command} {submenu_name}"}])
    create_and_send_message(server.as_plugin_server_interface(),
                            sub_menu_list,
                            "player",
                            source.player)

# 添加子菜单
def add_sub_menu(source: CommandSource, sub_menu_name: str, comment: str = ""):
    if not source.has_permission(3):
        source.reply("你没有权限使用此命令")  # 权限不足
        return
    if source.is_console:
        source.reply("该指令只能由玩家执行")
        return
    if sub_menu_name in config["sub_menus"]:
        source.reply(f"子菜单 '{sub_menu_name}' 已存在")  # 子菜单已存在
        return

    config["sub_menus"][sub_menu_name] = {"message": ["<text>§e新子菜单内容</text>"], "comment": comment}
    write_config()  # 保存配置
    update_config(source)  # 更新配置
    source.reply(f"成功添加子菜单 '{sub_menu_name}'")  # 回复添加成功

# 删除子菜单
def remove_sub_menu(source: CommandSource, sub_menu_name: str):
    if not source.has_permission(3):
        source.reply("你没有权限使用此命令")  # 权限不足
        return
    if source.is_console:
        source.reply("该指令只能由玩家执行")
        return
    if sub_menu_name not in config["sub_menus"]:
        source.reply(f"子菜单 '{sub_menu_name}' 不存在")  # 子菜单不存在
        return

    del config["sub_menus"][sub_menu_name]  # 删除子菜单
    write_config()  # 保存配置
    update_config(source)  # 更新配置
    source.reply(f"成功删除子菜单 '{sub_menu_name}'")  # 回复删除成功

# 添加随机文本组
def add_random_text_group(source: CommandSource, group_name: str):
    if not source.has_permission(3):
        source.reply("你没有权限使用此命令")
        return
    placeholder = f"random_text_{group_name}"
    if placeholder in config["random_text"]:
        source.reply(f"随机文本组 '{group_name}' 已存在")  # 随机文本组已存在
        return

    config["random_text"][placeholder] = ["新随机文本"]
    write_config()  # 保存配置
    update_config(source)  # 更新配置
    source.reply(f"成功添加随机文本组 '{group_name}'。使用 {{{placeholder}}} 来引用")  # 回复成功

# 删除随机文本组
def remove_random_text_group(source: CommandSource, group_name: str):
    if not source.has_permission(3):
        source.reply("你没有权限使用此命令")
        return
    placeholder = f"random_text_{group_name}"
    if placeholder not in config["random_text"]:
        source.reply(f"随机文本组 '{group_name}' 不存在")  # 随机文本组不存在
        return

    del config["random_text"][placeholder]  # 删除随机文本组
    write_config()  # 保存配置
    update_config(source)  # 更新配置
    source.reply(f"成功删除随机文本组 '{group_name}'")  # 回复删除成功

# 提取标签信息并转化为结构化格式
def extract_tag_info(cfg_msg) -> List[List[Dict]]:
    messages = []
    for message in cfg_msg:
        rows = re.findall(r'<(\w+)\s*(.*?)>(.*?)</\1>', message)  # 匹配标签及其内容
        row_info = []
        for unit in rows:
            unit_dict = {"tag_type": unit[0], "content": unit[2], "value": None, "hover": None}
            if unit[1] != "":
                attributes = re.findall(r'\((\w+)=(.*?)\)', unit[1])  # 匹配标签属性
                for attribute in attributes:
                    if attribute[0] == "v":
                        unit_dict["value"] = attribute[1]
                    elif attribute[0] == "h":
                        unit_dict["hover"] = attribute[1]
                    else:
                        unit_dict[attribute[0]] = attribute[1]
            row_info.append(unit_dict)
        messages.append(row_info)
    return messages

# 更新配置文件内容
def update_config(source: CommandSource = None):
    global config, main_menu_info, sub_menus_info, trigger_command
    server = __mcdr_server
    config = server.load_config_simple(file_name=CONFIG_FILE, default_config=default_config, in_data_folder=False)
    trigger_command = config["trigger_command"]  # 更新触发命令
    main_menu_info = extract_tag_info(config["message"])  # 提取主菜单信息
    sub_menus_info = {k: extract_tag_info(v["message"]) for k, v in config["sub_menus"].items()}  # 提取子菜单信息
    if source:
        source.reply("配置文件重载中...")  # 回复配置重载提示

# 写入配置文件
def write_config():
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

# 重载配置
def reload_config(source: CommandSource):
    if not source.has_permission(3):
        source.reply("你没有权限使用此命令")
        return
    update_config(source)  # 更新配置
    source.reply("重载完成!")  # 回复重载成功

# 插件加载时的初始化操作
def on_load(server: PluginServerInterface, old_module):
    global __mcdr_server
    __mcdr_server = server
    if server:
        update_config()  # 初始化配置，必须先调用以获取trigger_command
        
        # 使用配置中的触发命令注册帮助信息和命令
        server.register_help_message(f'!{trigger_command}', '打开菜单')  # 注册帮助信息
        
        # 注册主命令
        server.register_command(
            Literal(f"!{trigger_command}").runs(lambda src: open_menu(src)).  # 注册主命令
            then(
                Literal("add").requires(lambda src: src.has_permission(3)).then(
                    QuotableText("sub_menu_name").then(
                        QuotableText("comment").runs(lambda src, ctx: add_sub_menu(src, ctx['sub_menu_name'], ctx['comment']))
                    ).runs(lambda src, ctx: add_sub_menu(src, ctx['sub_menu_name'], ""))
                )
            ).then(
                Literal("del").requires(lambda src: src.has_permission(3)).then(
                    QuotableText("sub_menu_name").runs(lambda src, ctx: remove_sub_menu(src, ctx['sub_menu_name']))
                )
            ).then(
                QuotableText("sub_menu_name").runs(lambda src, ctx: open_menu(src, ctx['sub_menu_name']))
            ).then(
                Literal("addrt").requires(lambda src: src.has_permission(3)).then(
                    QuotableText("group_name").runs(lambda src, ctx: add_random_text_group(src, ctx['group_name']))
                )
            ).then(
                Literal("delrt").requires(lambda src: src.has_permission(3)).then(
                    QuotableText("group_name").runs(lambda src, ctx: remove_random_text_group(src, ctx['group_name']))
                )
            )
        )
        
        # 注册列表命令
        server.register_command(
            Literal(f"!{trigger_command}l").runs(lambda src: list_sub_menus(src))  # 注册列表命令
        )
        
        # 注册重载命令
        server.register_command(
            Literal(f"!{trigger_command}r").requires(lambda src: src.has_permission(3)).runs(lambda src: reload_config(src))  # 注册重载命令
        )

# 启动插件
on_load(None, None)