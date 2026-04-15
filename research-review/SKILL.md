---
name: research-review
description: 用户要审查外部研究报告质量、检查别人的分析逻辑是否自洽、或研究内容将用于招股书和公开披露材料时使用。不用于当次生成内容的日常自检（已内嵌在各研究类 skill 输出流程中）。
metadata:
  {"openclaw": {"emoji": "✅", "homepage": "https://github.com/tingbo-c/invest-research-skills"}}
---

# 研究质量复核

对研究内容做显式的结构化质量审查，输出完整审查报告。主要用于：审查外部研究、用户主动要求深度质检、披露级材料的合规核查。

日常自检（当次生成内容的关键项静默核查）已内嵌在 industry-research 和 stock-fundamental 的输出流程中，无需单独触发本 skill。

---

## 核心原则

1. 审查的是逻辑，不是结论。结论对不对不是这里判断的，逻辑链是否成立才是。
2. 每个问题必须定位到具体位置，不能只说"数据来源不足"，要说第几章哪个数据缺少来源。
3. 严重问题（影响结论有效性）和建议性问题（可改善但不影响核心）必须区分标注。
4. 不同输出场景的审查标准不同——内部参考和公开披露的要求差距很大。

---

## 三种审查模式

| 模式 | 适用场景 | 审查深度 |
|------|---------|---------|
| **快速检查** | 草稿阶段、内部讨论 | 只查致命错误：定义口径、逻辑断层、结论空洞 |
| **标准复核** | 正式报告、对外分享 | 完整清单全项检查，标注严重/建议 |
| **披露级审查** | 招股书、募资材料、审计底稿 | 标准复核 + 每个核心数字溯源，来源/时间/口径/计算链路全部可复核 |

---

## References 加载规则

| 审查维度 | 加载文件 |
|---------|---------|
| 数据质量检查 | `shared-research-context/references/data-quality-levels.md` |
| 时间口径检查 | `shared-research-context/references/time-consistency.md` |
| 常见陷阱排查 | `shared-research-context/references/pitfalls.md` |
| 结论结构检查 | `shared-research-context/references/scqr-principle.md` |
| 生命周期判断检查 | `shared-research-context/references/lifecycle-framework.md` |
| 护城河逻辑检查 | `shared-research-context/references/moat-framework.md` |
| 完整审查清单 | `references/review-checklist.md` |
| 输出审查报告 | `assets/review-report-template.md` |

---

## 审查流程

### 第一步：确认审查范围和模式

- 被审查的是什么类型的研究（行业 / 个股）？
- 用于什么场景（内部参考 / 对外报告 / 披露材料）？
- 由此确定审查模式（快速 / 标准 / 披露级）

### 第二步：加载审查清单

加载 `references/review-checklist.md`，按研究类型选择对应维度。

### 第三步：逐维度审查

按清单逐项检查，每项记录：
- ✅ 通过
- ⚠️ 建议改善（不影响核心结论）
- ❌ 严重问题（影响结论有效性，必须修改）

### 第四步：输出审查报告

加载 `assets/review-report-template.md`，填写：
- 严重问题列表（必须修改）
- 建议改善列表（可选）
- 总体评级
- 修改优先级建议

---

## 输出要求

- 每个问题必须注明：所在章节/位置 + 具体问题描述 + 修改建议
- 严重问题和建议性问题分开列示
- 不重写原文，只标注问题和给出修改方向
- 快速检查模式下，只输出严重问题，不展开建议性问题
