# ChatMenu - 轻量级聊天栏菜单插件

## 插件简介

ChatMenu 是一个专为 MCDR 设计的轻量级聊天栏菜单插件。它允许玩家通过简单的聊天命令快速访问各种功能，无需复杂的GUI界面，直接在聊天栏中提供丰富的交互体验。

![ChatMenu-Survival](https://github.com/JunjunSub/ChatMenu/blob/main/images/Survival.png)

## 反馈与支持

1. 如果您遇到任何BUG，欢迎在此项目的 Issues 页面提交，我会及时跟进并修复
2. 若有新的功能建议或希望与其他用户交流，欢迎加入QQ群 961111747 进行反馈

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
- [daycount_nbt ](https://github.com/alex3236/daycount-NBT/) >= 2.2.1

### 安装步骤
1. 将插件 `chat_menu.mcdr` 放入 MCDR 的 `plugins` 文件夹中
2. 确保已安装 [daycount_nbt ](https://github.com/alex3236/daycount-NBT/)
3. 重启 MCDR 或使用 `!!MCDR plugin load chat_menu.mcdr` 加载插件
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

### message支持的标签:

| 值               | 含义           | 支持的属性                           |
|-----------------|--------------|---------------------------------|
| `text`、`t`      | 直接发送文本       | `hover`:设置悬浮文本                  |
| `url`、`u`       | 打开给定链接       | `hover`:设置悬浮文本,`value`:设置要访问的网址 |
| `copy`、`c`      | 将给定文本复制到剪切板  | `hover`:设置悬浮文本,`value`:设置被复制的文本 |
| `command`、`cmd` | 将给定的文本作为指令运行 | `hover`:设置悬浮文本,`value`:设置要执行的指令 |
| `fill`、`f`      | 使用给定的文本填充聊天栏 | `hover`:设置悬浮文本,`value`:设置被填充的文本 |
## 注意事项

⚠️ **注意**：  

若无法与聊天栏中的菜单项进行点击交互，您可能需要安装 [LetMeClickAndSend](https://github.com/Fallen-Breath/LetMeClickAndSend) 客户端模组。

对 `command` 标签在不同 Minecraft 版本中的行为说明：

- **Minecraft < 1.19.1**  
  如果给定的文本不以 `"/"` 开头，文本将被当作聊天信息发送至服务端。借此，玩家点击后可以自动执行 MCDR 指令。

- **Minecraft >= 1.19.1**  
  只有以 `"/"` 开头的字符串（即标准指令格式）才能用作 `run_command` 动作的值。  
  对于其他不以 `"/"` 开头的字符串，客户端将拒绝发送对应的聊天消息。<sub>[[Issue #203](https://github.com/Fallen-Breath/MCDReforged/issues/203)]</sub>

### message支持的变量:

| 值 | 含义 |
|----|------|
| `{player}` | 获取玩家名称 |
| `{date}` | 获取服务器自建立以来已经运行了多少天（基于配置中的 `server_start_date`） |
| `{date_nbt}` | 获取当前世界已经运行了多少天（需要 [daycount-NBT](https://github.com/alex3236/daycount-NBT) 插件） |
| `{random_text}` | 匹配random_text中的键，在对应的值(list)中随机选择一项（注：list中的文本不支持message标签，仅可使用纯文本和颜色/格式化代码） |
### message支持的颜色/格式化代码:

[表格来源](https://minecraft.fandom.com/zh/wiki/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81)

| 代码 | 名称 |
|-------------|------------------|
| §0 | 黑色 |
| §1 | 深蓝色 |
| §2 | 深绿色 |
| §3 | 湖蓝色 |
| §4 | 深红色 |
| §5 | 紫色 |
| §6 |金色 |
| §7 |灰色 |                  
| §8 |深灰色 |                  
| §9 |蓝色 |                  
| §a |绿色 |                 
| §b |天蓝色 |                  
| §c |红色 |                  
| §d |粉红色 |                 
| §e |黄色 |                  
| §f |白色 |                  
| §g |硬币金[仅BE] |

| 代码 | 	格式效果        |
|----|--------------|
| §k | 	随机字符        |
| §l | 	粗体          |
| §m | 	删除线[仅Java版] |
| §n | 	下划线[仅Java版] |
| §o | 	斜体          |
| §r | 	重置文字样式      |


## 配置文件说明

![ChatMenu-default](https://github.com/JunjunSub/ChatMenu/blob/main/images/default.png)

### 默认配置
```json
{
    "trigger_command": "w",  # 触发命令，默认为w，即!w
    "message": [  # 主菜单
        "<text>§a哔哩哔哩关注：角落里的菌，谢谢喵</text>",
        "<text>§b这是随机文本喵→ {random_text} {random_text_1} </text>",
        "<url(v=https://space.bilibili.com/591893685)(h=快关注!)>§c点我打开哔哩主页喵</url>",
        "<copy(v=https://github.com/JunjunSub/ChatMenu)(h=快Star!)>§d点我复制插件链接到剪贴板喵</copy>",
        "<command(v=/ping)(h=查看连接延迟)>§e点我运行指令喵</command>",
        "<fill(v=猪务器已存活 {date} 游戏已运行 {date_nbt} 天!)(h=泰铢勒弥)>§f点我填充当前服务器运行天数瞄</fill>"
    ],
    "sub_menus": {  # 子菜单组
        "ms1": {
            "message": [  # 子菜单1
                "<text>这是子菜单1</text>"
            ],
            "comment": "这是子菜单1的介绍喵"
        },
        "ms2": {
            "message": [  # 子菜单2
                "<text>这是子菜单2</text>"
            ],
            "comment": "这是子菜单2的介绍喵"
        }
    },
    "random_text": {  # 随机文本组
        "random_text": [  # 随机子文本组
            "旮旯game不是这样的！",
            "咕咕嘎嘎"
        ],
        "random_text_1": [  # 随机子文本组1
            "阿巴阿巴",
            "摩西摩西"
        ]
    },
    "server_start_date": "2023-11-04",  # 服务器启动日期
    "nbt_mode": true,  # 是否启用NBT模式
    "nbt_file": "server/world/level.dat"  # NBT数据文件路径
}
