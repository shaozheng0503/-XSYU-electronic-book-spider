# 电子书网站爬虫项目

## 1 项目简介

本项目是一个用于获取电子书网站公开图书元数据的爬虫工具。**请注意，本工具仅用于获取公开的图书信息（如书名、作者、简介等），不获取受版权保护的内容。**

## 2 重要声明

### 2.1 法律合规性
- 本工具仅获取公开的图书元数据信息
- 不下载或获取受版权保护的电子书内容
- 请确保遵守目标网站的使用条款和版权法律
- 使用本工具产生的任何法律后果由使用者自行承担

### 2.2 使用限制
- 请控制爬取频率，避免对目标网站造成过大负担
- 建议在非高峰时段进行爬取
- 遵守网站的 robots.txt 规则
- 不要用于商业用途

## 3 环境要求

### 3.1 Python 版本
- Python 3.7 或更高版本

### 3.2 浏览器驱动
- Chrome 浏览器
- ChromeDriver（可通过 webdriver-manager 自动安装）

## 4 安装步骤

### 4.1 克隆项目
```bash
git clone <项目地址>
cd 图书馆电子书
```

### 4.2 安装依赖
```bash
pip install -r requirements.txt
```

### 4.3 安装 Chrome 浏览器
确保系统已安装 Chrome 浏览器，或使用以下命令安装：
```bash
# Windows (使用 Chocolatey)
choco install googlechrome

# macOS (使用 Homebrew)
brew install --cask google-chrome

# Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update
sudo apt-get install google-chrome-stable
```

## 5 使用方法

### 5.1 基本使用
```bash
python 电子书爬虫示例.py
```

### 5.2 自定义配置
修改 `电子书爬虫示例.py` 文件中的以下参数：
- `max_pages`: 最大爬取页数（默认 5 页）
- `delay`: 请求间隔时间（默认 3 秒）
- `base_url`: 目标网站地址

### 5.3 输出文件
爬取完成后会生成以下文件：
- `books_data.json`: JSON 格式的图书数据
- `books_data.csv`: CSV 格式的图书数据

## 6 数据结构

### 6.1 图书信息字段
```json
{
  "title": "图书标题",
  "author": "作者",
  "publisher": "出版社",
  "isbn": "ISBN 号",
  "description": "图书简介",
  "category": "分类",
  "cover_url": "封面图片链接",
  "detail_url": "详情页链接",
  "publish_date": "出版日期",
  "pages": "页数",
  "language": "语言",
  "table_of_contents": "目录",
  "cover_image": "封面图片"
}
```

## 7 技术架构

### 7.1 主要组件
- **Selenium WebDriver**: 处理动态 JavaScript 内容
- **BeautifulSoup**: HTML 解析
- **Requests**: HTTP 请求处理
- **JSON/CSV**: 数据存储格式

### 7.2 爬取流程
1. 初始化 WebDriver
2. 访问目标网站
3. 等待页面加载完成
4. 解析图书列表
5. 获取详细信息
6. 保存数据
7. 控制爬取频率

## 8 注意事项

### 8.1 网站结构变化
由于网站可能会更新结构，需要相应调整以下选择器：
- 图书列表选择器
- 详细信息选择器
- 分页选择器

### 8.2 反爬虫机制
如果遇到反爬虫机制，可以尝试：
- 增加请求间隔时间
- 更换 User-Agent
- 使用代理 IP
- 添加随机延迟

### 8.3 错误处理
程序包含完善的错误处理机制：
- 网络连接错误
- 页面解析错误
- 文件保存错误
- 用户中断处理

## 9 故障排除

### 9.1 WebDriver 问题
```bash
# 自动安装 ChromeDriver
pip install webdriver-manager
```

### 9.2 依赖安装问题
```bash
# 升级 pip
python -m pip install --upgrade pip

# 强制重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 9.3 权限问题
```bash
# Windows 管理员权限运行
# macOS/Linux 使用 sudo
sudo python 电子书爬虫示例.py
```

## 10 贡献指南

### 10.1 代码规范
- 遵循 PEP 8 代码规范
- 添加适当的注释和文档字符串
- 使用有意义的变量名和函数名

### 10.2 提交规范
- 使用清晰的提交信息
- 每次提交只包含一个功能或修复
- 在提交前进行代码测试

## 11 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和网站使用条款。

## 12 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 参与讨论

---

**免责声明**: 本工具仅供学习和研究使用，使用者需要自行承担使用风险，并确保遵守相关法律法规。 