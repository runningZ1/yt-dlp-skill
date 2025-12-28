# 部署流程 - Yt Dlp

## 目标

将测试通过的实例部署到生产环境。

## 前置条件

- [ ] 已完成 [测试流程](test-workflow.md)
- [ ] 生产环境准备就绪

## 步骤

### 1. 预部署检查

运行预检脚本：

```bash
python scripts/deploy.py --pre-check
```

### 2. 部署

执行部署：

```bash
python scripts/deploy.py --env production
```

### 3. 验证部署

验证部署结果：

```bash
python scripts/deploy.py --verify
```

### 4. 监控

持续监控生产环境。

## 回滚

如果部署失败：

```bash
python scripts/deploy.py --rollback
```

## 完成

恭喜！部署完成。
