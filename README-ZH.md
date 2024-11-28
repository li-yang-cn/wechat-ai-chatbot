# 微信 AI 聊天机器人 🤖

**注意：** 本项目没有使用 Hook 技术，只是单纯的物理复制粘贴。但回复消息过快仍然可能有被封号的风险。

## 描述
这个项目是基于 Python 的微信自动化聊天机器人。它可以检测微信桌面版的新消息，提取用户的查询，并将其发送到 AI 聊天机器人 API 获取响应。机器人实时回复，为用户创造流畅的互动体验。

---

## 功能 ✨
- 📍 **自定义**：设置特定位置进行消息检测和输入。
- 🎨 **基于颜色检测**：通过屏幕像素颜色检测新消息。
- 🌐 **AI 集成**：支持自定义 AI 聊天机器人 API。
- 🔄 **自动回复**：自动回复包含 `@Libot` 的消息。

---

## 环境要求 🛠️
- Python 3.8+
- 所需 Python 库：
  - `pyautogui`
  - `requests`
  - `pyperclip`
  - `pillow`

安装依赖：
```bash
pip install -r requirements.txt
```

---

## 使用方法 🚀
1. 克隆此仓库：
   ```bash
   git clone https://github.com/li-yang-cn/wechat-ai-chatbot.git
   cd wechat-ai-chatbot
   ```
2. 编辑脚本中的配置：
   - 将 `AI_URL` 设置为你的聊天机器人 API 地址。
   - 根据微信主题调整颜色设置。
3. 运行脚本：
   ```bash
   python wechat_bot.py
   ```
4. 按屏幕提示选择消息检测位置和输入框位置。
5. 让机器人处理包含 `@Libot` 的消息。

---

## 注意 📋
- 请确保微信已在桌面打开并处于前台。
- 使用时需提供合适的权限及 AI API 凭证。

---

## 开源许可证 📜
本项目开源，遵循 MIT 许可证。

## 本项目由以下prompt生成
```text
你是一名python编程专家，请帮我实现一个微信自动聊天机器人。需要的功能如下：
1. 通过监控屏幕的特定区域，检测聊天框固定位置的颜色（白色为有消息，灰色为空白），来判断是不是收到了新的消息。如果收到了新的消息，就又击复制。
2. python脚本检测是不是新的内容，并且是不是以“@Libot”开头，如果是，则调用LLM聊天机器人的URL来获取到响应，放到剪贴板。
3. 得到响应之后，点击聊天框的位置粘贴并回车发送。发送后清空剪贴板并继续循环监控。
程序设计的函数如下：
1. funtion select_location()。
读取屏幕坐标。通过用户点击光标来实现检测位置的标记。return点坐标。
2. function detect_color(location)
输入屏幕坐标，返回此处像素点的颜色。
3. function call_ai(url,question)
输入URL和问题，调用URL得到响应。return响应的文本。添加异常处理机制，如果调用失败，return对应的错误信息文本。
4. function copy_question(location)
前往location（x,y）的位置，点击鼠标右键，光标移动x+3,y-3再点击左键来实现复制。
5. function paste_answer(answer)
光标点击输入框，点击回车，发送消息。
6. 主函数
配置环境变量到代码中。包括AI_URL，消息白色的RGB，空白灰色的RGB，获取消息的间隔。
初始化时配置读取监控问题的坐标点，输入框的坐标点。
每隔1秒获取消息位置的颜色detect_color(location)，判断是否有变化，如果有变化，则copy_question(location)。检查上一个问题是否相同，如果相同则循环监控；如果不同，则try function call_ai(url,question)，得到answer之后，paste_answer(answer)。然后循环监控。
请帮我先实现框架，再实现详细的代码设计。
```
```text
我要把这个项目发布到Github上，请帮我实现中英文双语的README.MD文档。
```