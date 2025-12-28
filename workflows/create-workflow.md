# 创建流程 - Yt Dlp

## 目标

从零开始创建一个完整的 yt-dlp 实例。

## 前置条件

- [ ] 环境准备完成
- [ ] 依赖已安装
- [ ] 了解基本概念

## 步骤

### 1. 初始化

运行初始化脚本：

```bash
python scripts/init.py --name <project-name>
```

这将创建基础结构。

### 2. 配置

编辑配置文件，根据需求调整参数。

### 3. 实现核心逻辑

按照模板实现核心功能。

参考: [templates/basic-template.md](../templates/basic-template.md)

### 4. 验证

运行验证脚本确保正确性：

```bash
python scripts/validate.py
```

### 5. 测试

继续到 [测试流程](test-workflow.md)

## 常见问题

- **问题 1**: 初始化失败
  - 解决: 检查权限和依赖

- **问题 2**: 配置错误
  - 解决: 参考 [best-practices.md](../references/best-practices.md)

## 下一步

→ [测试流程](test-workflow.md)
