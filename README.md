# ChatMenu - 轻量级聊天栏菜单插件

## 插件简介

ChatMenu 是一个专为 MCDR 设计的轻量级聊天栏菜单插件。它允许玩家通过简单的聊天命令快速访问各种功能，无需复杂的GUI界面，直接在聊天栏中提供丰富的交互体验。

## 核心特性

### 🎯 轻量高效
- 不占用额外界面资源，直接在聊天栏显示菜单
- 响应迅速，对服务器性能影响极小
- 兼容性优秀，支持各种MC版本

### 🎨 高度可定制
- 完全可自定义的菜单内容和格式
- 支持 Minecraft 颜色代码和格式代码
- 灵活的触发命令配置

### 🔗 丰富的交互功能
- **文本显示** - 普通文本和信息展示
- **链接打开** - 直接打开网页链接
- **命令执行** - 运行服务器命令
- **文本复制** - 复制内容到剪贴板
- **聊天栏填充** - 预填充聊天栏内容

### 📱 智能菜单系统
- **主菜单** - 主要功能入口
- **子菜单系统** - 支持无限层级子菜单
- **动态内容** - 支持变量和随机文本
- **权限管理** - 基于MCDR权限系统的访问控制

## 安装说明

### 前置要求
- MCDReforged >= 2.2.0
- [daycount_nbt 插件](https://github.com/alex3236/daycount-NBT/) (>=2.2.1)

### 安装步骤
1. 将插件文件夹 `chat_menu` 放入 MCDR 的 `plugins` 文件夹中
2. 确保已安装 [daycount_nbt 插件](https://github.com/alex3236/daycount-NBT/)
3. 重启 MCDR 或使用 `!!MCDR plugin load chat_menu` 加载插件
4. 插件会自动生成配置文件 `config/chat_menu.json`

## 游戏内指令

以下是 ChatMenu 插件提供的所有游戏内命令（**注意：以下命令中的 `w` 部分可在配置文件中修改为其他字符**）：

### 基础菜单命令
- **`!w`** - 打开主菜单
- **`!w <子菜单名>`** - 打开指定子菜单
- **`!wl`** - 列出所有可用子菜单

### 配置管理命令（需要3级权限）
- **`!wr`** - 重新加载配置文件
- **`!w add <子菜单名>`** - 添加新子菜单
- **`!w del <子菜单名>`** - 删除子菜单
- **`!w addrt <文本组名>`** - 添加随机文本组
- **`!w delrt <文本组名>`** - 删除随机文本组

### 自定义触发命令
所有命令中的 `w` 部分都可以通过在配置文件中修改 `trigger_command` 字段来自定义。例如，如果设置为 `menu`，则命令变为：
- `!menu` - 打开主菜单
- `!menul` - 列出子菜单
- `!menur` - 重载配置
- 等等...

## 配置文件说明

### 默认配置结构
```json
{
  "trigger_command": "w",
  "message": [
    "<text>§a哔哩哔哩关注：角落里的菌，谢谢喵</text>",
    "<text>§b这是随机文本喵→ {random_text} {random_text_1} </text>",
    "<url(v=https://space.bilibili.com/591893685 h=快关注！)>§c点我打开哔哩主页喵</url>",
    "<copy(v=https://github.com/JunjunSub/ChatMenu h=点我复制链接)>§d点我复制插件链接到剪贴板喵</copy>",
    "<command(v=/ping h=查看连接延迟)>§e点我运行指令喵~</command>",
    "<fill(v=猪务器已存活 {date} 游戏已运行 {date_nbt} 天！ h=泰铢勒弥)>§f点我填充当前服务器运行天数瞄</fill>"
  ],
  "sub_menus": {
    "ms1": {
      "message": [
        "<text>这是子菜单1</text>"
      ],
      "comment": "这是子菜单1的介绍喵~"
    },
    "ms2": {
      "message": [
        "<text>这是子菜单2</text>"
      ],
      "comment": "这是子菜单2的介绍喵~"
    }
  },
  "random_text": {
    "random_text": [
      "旮旯game不是这样的！",
      "咕咕嘎嘎~"
    ],
    "random_text_1": [
      "阿巴阿巴",
      "摩西摩西"
    ]
  },
  "server_start_date": "2023-11-04",
  "nbt_mode": true,
  "nbt_file": "server/world/level.dat"
}
