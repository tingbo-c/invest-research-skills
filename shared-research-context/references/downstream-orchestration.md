# 深研层编排契约(下游调用方说明)

> **用途**:描述这套 A股投研 skill 套件如何被下游"深研层"批量调用——喂什么、按什么顺序跑、产出什么、怎么复用。面向编排 agent 或需要理解调用链的开发者。

---

## 背景

本套件将被 **A股 CAN SLIM 选股项目的「深研层」** 调用:
1. 量化海选层先筛出约 30 只候选,每只带 point-in-time 财务简报
2. 深研层对每只候选调用本套件做深研,产出一张「深研卡片」
3. 深研卡片机读字段回流量化层做回测验证

---

## 输入契约 C1(每只候选的喂入物)

来自项目 DuckDB,满足「披露日 ≤ 选股日」防未来函数:

**财务简报字段**
- `code` / `name` / `industry`(申万)
- 29 季度的 `stat_date`(报告期)、`pub_date`(披露日)
- `eps_ttm`、`net_profit`(绝对值)、`roe_avg`、`revenue`、`yoy_ni`

**海选侧信息**
- 距 52 周高点 %、RS 评级、量价信号
- 通过的海选条件(C/A/RS/N 等)、`screen_score`

---

## 编排顺序

```
行业分组
  └─ sector-research(每个行业跑一次,产出 sector_context,同行业复用/缓存)
       └─ 逐只并行
            ├─ stock-fundamental(主干,吃 C1 简报)
            │    ├─ financial-diagnostics(C2 财务质量甄别,嵌入调用)
            │    ├─ theme-chain-context(题材链,按需嵌入)
            │    └─ event-interpretation(近期事件,按需嵌入)
            └─ 汇总 → deep_research_card(每只一张)
```

**关键原则**:
- `sector-research` 同行业只跑一次,结果缓存复用,不对每只重跑
- `stock-fundamental` 以 C1 简报为口径基准,**不重复抓数、不与简报打架**;简报未覆盖的科目再补查
- 题材链/事件解读按需嵌入,无近期事件时 `event` 子块可为空
- 每只可独立调用(单只深研时跳过行业批量逻辑)

---

## 输出契约 C8(深研卡片机读块)

每只产出一张 `deep_research_card`,canonical schema 见 [deep-research-card.md](deep-research-card.md)。

核心机读字段:
- `quality_grade`:真增长 / 存疑 / 疑粉饰 / 未知
- `benefit_type`:直接受益 / 间接受益 / 蹭概念 / 被错杀 / 中性 / 未知
- `theme_stage`:早期 / 中期 / 晚期 / 已透支 / 未知
- `leading_signals`:领先信号类型 + 强度(来自 financial-diagnostics 第六层)

这些字段供回流量化做回测对齐。**枚举取值固定,不得自创近义词。**

---

## 各模块职责速查

| 模块 | 职责 | 产出子块 |
|---|---|---|
| `sector-research` | 行业阶段/竞争格局/估值中枢 | `sector_context` / `industry_stage` |
| `stock-fundamental` | 主干汇总,业务定位,驱动变量;汇总各子块成整张卡 | `deep_research_card` 汇总方 |
| └ `financial-diagnostics`(stock-fundamental 的 C2 reference,非独立模块) | 财务质量甄别 + 领先信号 | `financial_quality` |
| `theme-chain-context` | 题材链,受益类型,拥挤度 | `theme` |
| `event-interpretation` | 近期事件,Priced-in 检验 | `event` |
| `research-review` | 质控,审查以上所有输出 | 不填卡片,负责审查 |

> 6 个模块各有 SKILL.md;`financial-diagnostics` 是 stock-fundamental 在 C2 阶段加载的 reference(`references/financial-diagnostics.md`),不是第 7 个独立模块。

---

## 一句话原则

用真实材料 + 出处说话,宁可标「未知」,不许编;只分析,不建议。选不选、买不买不在这层。
