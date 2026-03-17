# Telegram Info Seeker

一个基于 Telegram Bot API 的群聊消息爬虫机器人，支持实时监听和关键词过滤，消息存储在本地 SQLite 数据库中。

## 功能

- 实时监听群组新消息并保存到 SQLite
- 关键词过滤（只保存包含指定关键词的消息）
- `/stats` 命令查看统计信息
- `/keywords` 命令查看当前关键词配置

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 从 @BotFather 获取
BOT_TOKEN=your_bot_token_here

# 关键词过滤（逗号分隔，留空则保存所有消息）
KEYWORDS=比特币,以太坊

# 数据库路径
DB_PATH=messages.db
```

### 3. 获取 Bot Token

1. 在 Telegram 中找到 `@BotFather`
2. 发送 `/newbot`，按提示创建机器人
3. 将获得的 Token 填入 `.env`

### 4. 将机器人加入群组

将你的机器人添加为群管理员（或普通成员），机器人需要读取消息的权限。

### 5. 启动

```bash
python main.py
```

## 数据库结构

消息保存在 `messages.db` 的 `messages` 表中：

| 字段 | 说明 |
|------|------|
| message_id | Telegram 消息 ID |
| chat_id | 群组 ID |
| chat_title | 群组名称 |
| sender_id | 发送者 ID |
| sender_name | 发送者姓名 |
| sender_username | 发送者用户名 |
| text | 消息内容 |
| date | 消息发送时间 |
| saved_at | 本地保存时间 |

## 注意事项

- Bot API 只能读取机器人**所在群组**的消息
- 机器人需要在群组中具有读取消息的权限
- 如果群组开启了隐私模式，需要将机器人设为管理员或通过 `@BotFather` 关闭隐私模式
