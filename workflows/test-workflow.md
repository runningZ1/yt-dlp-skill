# 测试流程 - Yt Dlp

## 目标

全面测试创建的实例，确保质量。

## 前置条件

- [ ] 已完成 [创建流程](create-workflow.md)
- [ ] 测试环境准备就绪

## 步骤

### 1. 单元测试

运行单元测试：

```bash
python scripts/test.py --unit
```

### 2. 集成测试

运行集成测试：

```bash
python scripts/test.py --integration
```

### 3. 端到端测试

运行完整测试：

```bash
python scripts/test.py --e2e
```

### 4. 分析结果

查看测试报告，修复失败的测试。

## 质量标准

- [ ] 所有单元测试通过
- [ ] 集成测试通过
- [ ] 覆盖率 ≥ 80%
- [ ] 无 critical issues

## 下一步

→ [部署流程](deploy-workflow.md)
