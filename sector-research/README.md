# Industry Research Skill

一个面向行业研究与投资判断的通用技能包，不依赖单一平台运行机制。

适用对象：

- Claude Code / Claude Skills
- ChatGPT / Gemini /豆包/openclaw/deepseek等 其他支持读文件与运行脚本的 coding agent
- 人类分析师

核心目标：

- 结构化完成行业研究
- 在没有官方总量数据时做合理推导
- 在公开披露场景下提升来源可信度与可复核性
- 用轻量脚本降低测算与口径错误

---

## 目录结构

```text
industry-research/
├── SKILL.md
├── README.md
├── references/
├── scripts/
│   ├── calc.py
│   └── examples/
└── assets/
```

- `SKILL.md`
  主文件，负责说明做什么、什么时候读哪份 reference、什么时候跑脚本

- `references/`
  方法论、数据源、估值、阶段分析、披露核查、时间口径、轻量复核等文档

- `scripts/`
  可执行计算工具

- `assets/`
  预留给模板、案例、报告样式等资源

---

## 使用方式

### 方式一：给支持 skill 的 agent 使用

让 agent 先读 `SKILL.md`，再按加载规则进入对应 `references/` 或 `scripts/`。

适合：
- Claude Code
- 其他支持目录式技能包的 agent

### 方式二：给普通 coding agent 使用

如果 agent 不支持官方 skill runtime，也可以这样用：

1. 先读 `SKILL.md`
2. 根据任务类型读取对应 `references/`
3. 遇到多变量测算、分层加总、时间口径检查时运行 `scripts/calc.py`
4. 输出正式结论前读取 `references/analysis-review-checklist.md`

### 方式三：给人类分析师使用

可以把它当成“行业研究操作手册 + 计算工具”：

1. 用 `SKILL.md` 看流程
2. 用 `references/` 查方法和口径
3. 用 `scripts/calc.py` 执行测算
4. 用 `analysis-review-checklist.md` 做输出前复核

---

## 任务到文件的映射

| 任务 | 优先读取 |
|---|---|
| 行业定界 | `SKILL.md` |
| 市场规模测算 | `references/formulas.md` + `scripts/calc.py` |
| 没有官方总量数据 | `references/no-official-data-sizing.md` |
| 数据来源分级 | `references/data-sources.md` |
| 估值判断 | `references/valuation-multiples.md` + `scripts/calc.py` |
| 生命周期、竞争格局、景气度 | `references/stage-analysis.md` |
| 时间口径不一致 | `references/time-consistency.md` |
| 输出前轻量复核 | `references/analysis-review-checklist.md` |
| 公开披露场景 | `references/disclosure-grade-checklist.md` |
| 报告结构与输出深度 | `references/output-structure.md` |

---

## 输出模式

这套 skill 默认支持 3 档输出深度：

- 快速判断版
  适合“分析一下”“研究一下”“值不值得看”

- 标准报告版
  适合“完整分析”“详细报告”“按行业研究报告结构输出”

- 披露/底稿版
  适合“招股书”“募资材料”“公开披露”“可追溯”

如果用户没有明确要求篇幅，默认用快速判断版。

---

## 计算脚本

脚本位置：

- `scripts/calc.py`

支持 3 类计算：

- `sizing`
  市场规模、情景分析、分层加总

- `cycle`
  产能周期、资金占用能力、集中度

- `valuation`
  相对估值等基础计算

示例命令：

```bash
python scripts/calc.py sizing scripts/examples/sizing-input.json --pretty
python scripts/calc.py cycle scripts/examples/cycle-input.json --pretty
python scripts/calc.py valuation scripts/examples/valuation-input.json --pretty
```

脚本职责：

- 负责计算
- 负责时间口径 warning
- 负责阈值判断

不负责：

- 自动找数据
- 自动判断行业阶段
- 自动生成最终投资结论

这些仍由分析者或 agent 根据 `SKILL.md` 与 `references/` 完成。

---

## 使用原则

- 先定界，再判断阶段，再测算，再下结论
- 当前判断优先用最近一个完整年度或最近可得时点
- P5 数据只能做旁证，不能承担主证据角色
- 没有官方总量时可以估算，但高可信度场景下最底层锚点必须“硬”
- 输出正式结论前，先做轻量复核

---

## 平台兼容说明

本项目按 Claude Skill 目录规范组织，但不依赖 Claude 才能使用。

只要一个 agent 能：

- 读取 Markdown 文件
- 理解文件映射关系
- 执行 Python 脚本

就可以使用这套 skill。

也就是说，这更像一个“通用行业研究 toolkit”，而不只是某个平台专用插件。
