# 调试工作流

## 目标

有效调试 yt-dlp 提取器、解决下载问题、分析网站变化。

## 前置条件

- [ ] 已完成 [基础下载工作流](basic-download.md)
- [ ] 熟悉 Python 调试
- [ ] 了解 HTTP 和 HTML

## 步骤

### 步骤 1: 启用详细输出

```bash
# 基础详细模式
yt-dlp -v "URL"

# 更详细的调试信息
yt-dlp -v --print-traffic "URL"

# 显示所有 HTTP 请求/响应
yt-dlp --print-traffic "URL"

# 只打印下载的网页
yt-dlp --print-traffic --write-pages "URL"
```

### 步骤 2: 分析网页结构

```bash
# 保存网页到文件
yt-dlp --write-pages "URL"
# 网页保存在 <domain>.dump 文件

# 查看网页源码
cat www_youtube_com.dump

# 使用 --dump-pages 直接打印
yt-dlp --dump-pages "URL" | head -100
```

### 步骤 3: 测试提取器

```bash
# 运行指定提取器
yt-dlp --ignore-errors --extractor-flatten "URL"

# 强制使用特定提取器
yt-dlp --extractor-key "MySite" "URL"

# 列出所有可用提取器
yt-dlp --list-extractors | grep mysite

# 跳过下载，只测试提取
yt-dlp --skip-download "URL"
```

### 步骤 4: Python 调试

```python
# 在提取器中添加断点
import pdb; pdb.set_trace()

# 使用 print 调试
self._downloader.to_screen(f'DEBUG: variable={variable}')

# 保存中间结果用于分析
self._save_webpage('debug.html', content)
```

### 步骤 5: 常见问题诊断

#### 问题: 提取器未匹配

```bash
# 检查 URL 是否匹配
yt-dlp --print-to-file "%(extractor)s" output.txt "URL"

# 查看匹配的提取器
yt-dlp --print "%(extractor)s" "URL"

# 测试正则表达式
python -c "
import re
url = 'https://www.example.com/watch/abc123'
pattern = r'https?://(?:www\.)?example\.com/watch/(?P<id>[^/]+)'
match = re.match(pattern, url)
print(match.groupdict() if match else 'No match')
"
```

#### 问题: JSON 解析失败

```bash
# 查看原始 JSON 响应
yt-dlp --print-traffic "URL" | grep -A 50 "application/json"

# 使用 jq 格式化
yt-dlp --print-traffic "URL" | jq .

# 保存响应到文件
yt-dlp --print-traffic "URL" > response.txt
```

#### 问题: 格式选择失败

```bash
# 列出所有格式
yt-dlp -F "URL"

# 打印格式字典
yt-dlp --print "%(formats)s" "URL"

# 测试格式选择
yt-dlp -f "bestvideo+bestaudio" --print "%(format)s" "URL"
```

#### 问题: 认证失败

```bash
# 测试 cookies
yt-dlp --cookies cookies.txt --print "%(title)s" "URL"

# 测试用户名密码
yt-dlp -u USERNAME -p PASSWORD --skip-download "URL"

# 检查请求头
yt-dlp --print-traffic "URL" | grep -i "authorization"
```

### 步骤 6: 使用浏览器开发者工具

```bash
# 1. 打开浏览器开发者工具 (F12)
# 2. 切换到 Network 标签
# 3. 访问目标网站
# 4. 查找视频请求
# 5. 右键 -> Copy as cURL

# 将 cURL 命令转换为 yt-dlp 参数
# 例如: cURL 中的 -H "Authorization: Bearer TOKEN"
# 转换为: yt-dlp --add-header "Authorization: Bearer TOKEN"
```

### 步骤 7: 比较正常和失败的请求

```bash
# 保存成功的请求
yt-dlp --print-traffic --write-pages "WORKING_URL" > working.txt

# 保存失败的请求
yt-dlp --print-traffic --write-pages "FAILING_URL" > failing.txt

# 对比差异
diff working.txt failing.txt
```

### 步骤 8: 监控文件变化

```bash
# 使用 entr 监控文件变化（Linux/macOS）
echo "yt_dlp/extractor/mysite.py" | entr -r python -m yt_dlp "URL"

# 或使用 watch（简单的重复测试）
watch -n 1 "yt-dlp --skip-download 'URL'"
```

### 步骤 9: 日志分析

```bash
# 保存完整日志
yt-dlp -v "URL" 2>&1 | tee debug.log

# 过滤错误
yt-dlp -v "URL" 2>&1 | grep -i error

# 过滤特定提取器
yt-dlp -v "URL" 2>&1 | grep -i "mysite"
```

### 步骤 10: 单元测试

```python
# 创建测试文件 test_mysite.py
import unittest
from yt_dlp.extractor.mysite import MySiteIE

class TestMySiteIE(unittest.TestCase):
    def test_url_matching(self):
        self.assertEqual(
            MySiteIE.suitable('https://www.mysite.com/watch/abc123'),
            True
        )

    def test_extraction(self):
        ie = MySiteIE()
        result = ie.extract('https://www.mysite.com/watch/test123')
        self.assertEqual(result['id'], 'test123')

if __name__ == '__main__':
    unittest.main()
```

## 调试技巧

### 技巧 1: 使用 --flat-playlist

```bash
# 快速测试提取器而不下载实际视频
yt-dlp --flat-playlist --print "%(id)s - %(title)s" "URL"
```

### 技巧 2: 使用 --no-download

```bash
# 只测试提取，不下载
yt-dlp --no-download "URL"
```

### 技巧 3: 使用 --print

```bash
# 打印特定字段
yt-dlp --print "%(id)s - %(title)s - %(uploader)s" "URL"

# 打印 JSON
yt-dlp --print "%(json)s" "URL" | jq .

# 打印所有可用字段
yt-dlp --print "keys" "URL"
```

### 技巧 4: 使用 --exec

```bash
# 下载后执行命令
yt-dlp --exec 'echo "Downloaded: {}"' "URL"

# 使用文件名
yt-dlp --exec 'mv {} ~/Videos/' "URL"
```

### 技巧 5: 使用配置文件

```ini
# debug.conf
-v
--print-traffic
--write-pages
--output debug/%(title)s.%(ext)s
```

```bash
yt-dlp --config debug.conf "URL"
```

## 常见调试场景

### 场景 1: 网站更新导致提取器失效

```bash
# 1. 保存旧版本工作时的网页
yt-dlp --write-pages "URL"

# 2. 等待失败后，保存新版本网页
# 手动保存或使用 wget
wget "URL" -O new_page.html

# 3. 对比差异
diff www_example_com.dump new_page.html

# 4. 定位变化，更新提取器
```

### 场景 2: API 端点变化

```bash
# 1. 查看所有网络请求
yt-dlp --print-traffic "URL" | grep "api"

# 2. 找到新端点
# 3. 更新提取器中的 URL
```

### 场景 3: 认证方式变化

```bash
# 1. 对比新旧认证请求
# 2. 找出新增的请求头/参数
# 3. 更新认证逻辑
```

### 场景 4: 视频格式变化

```bash
# 1. 列出所有格式
yt-dlp -F "URL"

# 2. 对比预期格式
# 3. 更新格式选择逻辑
```

## 调试工具

### 工具 1: jq（JSON 处理）

```bash
# 格式化 JSON 输出
yt-dlp --print "%(json)s" "URL" | jq .

# 提取特定字段
yt-dlp --print "%(json)s" "URL" | jq '.title'
```

### 工具 2: curl（测试请求）

```bash
# 模拟 yt-dlp 请求
curl -H "User-Agent: Mozilla/5.0" "URL"

# 查看响应头
curl -I "URL"
```

### 工具 3: Python REPL

```python
# 交互式测试
>>> from yt_dlp.extractor.mysite import MySiteIE
>>> ie = MySiteIE()
>>> ie.suitable('https://www.mysite.com/watch/abc123')
True
```

### 工具 4: Postman/Insomnia

```bash
# GUI 测试 API 请求
# 1. 从浏览器复制请求
# 2. 在 Postman 中重建
# 3. 测试各种参数组合
```

## 性能调试

### 检查下载速度

```bash
# 显示下载进度和速度
yt-dlp --newline "URL"

# 使用不同下载器
yt-dlp --external-downloader aria2 "URL"
```

### 检查内存使用

```bash
# 使用内存分析器
python -m memory_profiler $(which yt-dlp) "URL"
```

### 检查 CPU 使用

```bash
# 使用 top/htop
# 或使用 psrecord
psrecord -o plot.png --log log.txt "yt-dlp URL"
```

## 获取帮助

### 查看文档

```bash
# 帮助信息
yt-dlp --help

# 特定选项帮助
yt-dlp --help --format

# 查看所有选项
yt-dlp --help --all
```

### 社区资源

- GitHub Issues: https://github.com/yt-dlp/yt-dlp/issues
- Wiki: https://github.com/yt-dlp/yt-dlp/wiki
- Discord: 服务器链接在 GitHub README

## 下一步

- [提取器开发工作流](extractor-development.md) - 开发和测试提取器
- [故障排查](../references/troubleshooting.md) - 常见问题解决
- [架构参考](../references/architecture.md) - 深入理解内部机制
