# research-review

研究质量复核工具。对 industry-research、stock-fundamental 等技能产出的研究内容做结构化质量审查。

不重新做分析，只审查已有分析的质量、完整性和逻辑一致性。

---

## 三种使用方式

### Claude Skill 用户

直接触发：
> "帮我检查一下这份行业研究报告的质量"
> "这篇个股分析逻辑上有没有问题"
> "这份报告要进募资材料，做一个披露级审查"

### Coding Agent / 自动化流程

在研究生成后自动调用 research-review 做质量把关，输出结构化审查报告（JSON 或 Markdown）。

### 人工分析师

直接使用 `references/review-checklist.md` 作为人工自查清单，在提交研究报告前逐项核对。

---

## 三种审查模式

| 模式 | 适用场景 | 执行项目 |
|------|---------|---------|
| 快速检查 | 草稿、内部讨论 | 只查标注 ⚡ 的致命错误项 |
| 标准复核 | 正式报告、对外分享 | 完整清单全项检查 |
| 披露级审查 | 招股书、募资材料、审计底稿 | 标准复核 + 每个核心数字溯源 |

---

## 文件结构

```
research-review/
├── SKILL.md                        # Agent 执行流程（审查模式、加载规则、流程骨架）
├── README.md                       # 本文件
├── references/
│   └── review-checklist.md         # 分维度完整审查清单（九大维度，45+ 检查项）
└── assets/
    └── review-report-template.md   # 审查结论输出模板
```

---

## 与其他技能的关系

research-review 是整个技能套件的质量把关层：

```
industry-research  ──┐
stock-fundamental  ──┤──→  research-review  ──→  最终输出
```

所有研究类技能的输出都可以经过 research-review 复核后再对外使用。

---

## 核心设计原则

**审查逻辑，不审结论。** 结论对不对是分析师的判断；逻辑链是否完整、数据是否可靠、推演是否有跳跃，才是这个工具负责的范围。
