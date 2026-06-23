# 深研卡片输出契约(统一 schema)

> **用途**:这是下游"深研层"对每只候选要回填的**一张卡**(机读键名 `deep_research_card`)。各模块产出的子块(theme-chain 的 `theme_chain`、financial-diagnostics 的 `financial_quality`、event-interpretation 的 `event_impact`、sector-research 的 `sector_context`)由 stock-fundamental 作为汇总方**并入统一结构**,供深研层解析、回流量化做回测验证。
> **总原则**:用真实材料 + 出处说话,宁可标"未知",不许编;只分析,不建议。选不选、买不买不在这层。

---

## 一、人读卡片结构(给人看的那一面)

每只一张,字段尽量结构化:

- **代码 / 名称 / 行业 / 海选得分**
- **一句话**:是什么公司 + 主营收入与利润来源
- **行业阶段**(生命周期:导入/成长/成熟/衰退)+ **核心驱动变量**(当前顺风 / 逆风 / 方向不明)
- **业绩质量评级**:真增长 / 存疑 / 疑粉饰 —— 附依据(低基数 flag、非经常占比、ROE 背离、现金流匹配)
- **题材与拥挤度**:受益类型(直接 / 间接 / 蹭概念 / 被错杀)+ 题材阶段(早期 / 中期 / 晚期 / 已透支)+ 拥挤度
- **催化剂与 priced-in**(若有近期事件):催化是否已透支
- **主要风险 / 疑点**:具体,不写"竞争加剧"这类空话
- **失效条件 + 3-5 个跟踪指标**
- **为什么入选 + 一句话结论**(只分析,先不给具体买卖建议)
- **出处清单**:URL + 日期
- **机器可读标签**(见下)

---

## 二、统一机读块(canonical schema)

放在卡片末尾。各模块按需填自己负责的子块;深研层按此结构解析。

```yaml
deep_research_card:
  # —— 身份与海选(来自下游简报) ——
  code: <6位代码>
  name: <名称>
  industry: <申万行业>
  screen_score: <海选得分,可空>
  as_of: <YYYY-MM-DD,数据/分析口径日>

  # —— 定位(stock-fundamental) ——
  one_liner: <是什么公司 + 主营收入与利润来源>
  industry_stage: 导入期 | 成长期 | 成熟期 | 衰退期 | 未知   # 来自 sector-research
  core_driver: {var: <最关键外部驱动>, direction: 顺风 | 逆风 | 不明}

  # —— 业绩质量(financial-diagnostics, C2) ——
  financial_quality:
    quality_grade: 真增长 | 存疑 | 疑粉饰 | 未知
    flags: {low_base: bool, non_recurring: bool, roe_divergence: bool, cashflow_mismatch: bool}
    note: <一句话依据>

  # —— 题材与拥挤度(theme-chain, C5) ——
  theme:
    chain_name: <题材/链名,可空>
    benefit_type: 直接受益 | 间接受益 | 蹭概念 | 被错杀 | 中性 | 未知
    theme_stage: 早期 | 中期 | 晚期 | 已透支 | 未知
    crowding: 低 | 中 | 高 | 未知

  # —— 事件/催化剂(event-interpretation, C6;无近期事件可空) ——
  event:
    latest: <事件简述,可空>
    priced_in: 已透支 | 部分定价 | 未定价 | 无法验证 | 未知
    impact: 增强 | 削弱 | 无关 | 重写 | 未知

  # —— 判断与跟踪 ——
  key_risks: [<具体风险/疑点>]
  failure_conditions: [<可观测失效信号>]
  track_indicators: [<3-5 个跟踪指标>]
  why_selected: <为什么入选,呼应海选逻辑>
  conclusion: <一句话结论,只分析不建议>

  # —— 溯源与降级 ——
  sources: [{url: <URL>, date: <YYYY-MM-DD>, tier: P1|P2|P3|P4|P5}]
  websearch_used: true | false   # false 时题材/事件/拥挤度等时效字段需标降级
```

---

## 三、字段填写规则

- **每个模块只填自己负责的子块**:身份/海选来自下游简报;`industry_stage` 来自 sector-research;`financial_quality` 来自 financial-diagnostics;`theme` 来自 theme-chain;`event` 来自 event-interpretation;判断/跟踪/结论由 stock-fundamental 汇总。
- **无法判断一律填 `未知`**,不编造、不用训练数据猜。
- **每个机读标签都要可溯源**:结论性字段对应的依据写在人读部分 + `sources` 里(URL + 日期 + P 级)。
- **时效字段**(theme_stage / crowding / priced_in / core_driver.direction)必须基于 WebSearch 最近数据;`websearch_used: false` 时这些字段标降级或填未知。
- **只分析不建议**:`conclusion` 不含仓位 / 目标价 / 买卖时点;`why_selected` 是分析性的"为什么值得深看",不是买入理由。

---

## 四、枚举取值(canonical,勿自创近义词)

| 字段 | 取值 |
|---|---|
| industry_stage | 导入期 / 成长期 / 成熟期 / 衰退期 / 未知 |
| quality_grade | 真增长 / 存疑 / 疑粉饰 / 未知 |
| benefit_type | 直接受益 / 间接受益 / 蹭概念 / 被错杀 / 中性 / 未知 |
| theme_stage | 早期 / 中期 / 晚期 / 已透支 / 未知 |
| crowding | 低 / 中 / 高 / 未知 |
| priced_in | 已透支 / 部分定价 / 未定价 / 无法验证 / 未知 |
| impact | 增强 / 削弱 / 无关 / 重写 / 未知 |
| core_driver.direction | 顺风 / 逆风 / 不明 |
| sources[].tier | P1 / P2 / P3 / P4 / P5 |

> 取值固定,便于回流量化做回测对齐。不要写"偏高估""大概率受益"这类自由文本进枚举字段。

---

## 五、被哪些模块引用

- `stock-fundamental`:汇总方,产出整张卡
- `theme-chain-context`:填 `theme` 子块
- `financial-diagnostics`(stock-fundamental reference):填 `financial_quality` 子块
- `event-interpretation`:填 `event` 子块(如有近期事件)
- `sector-research`:提供 `industry_stage`
