---
name: shared-research-context
description: 当其他研究类 skill（industry-research、stock-fundamental、research-review）需要加载通用方法论时由 skill 内部引用，不由用户意图直接触发。
metadata:
  {"openclaw": {"emoji": "🏛️", "homepage": "https://github.com/tingbo-c/invest-research-skills"}}
---

# 共享研究方法论底座

不直接面向用户使用，作为其他研究类 skill 的方法论基础层被按需加载。

---

## 文件目录

| 文件 | 内容 | 被哪些 skill 引用 |
|---|---|---|
| `references/research-methodology.md` | DIKW 模型、假设驱动法、认知偏差清单、信息源可信度标准 | industry-research, stock-fundamental |
| `references/external-factors.md` | PEST 框架、政策信号分类、经济周期传导、Gartner 技术曲线 | industry-research |
| `references/lifecycle-framework.md` | 渗透率标尺、四阶段框架（导入/成长/成熟/衰退）、关键阈值、阶段与分析工具对应表 | industry-research, stock-fundamental |
| `references/data-quality-levels.md` | P1-P5 分级与使用规则、数据冲突处理、AI 数据幻觉提醒 | industry-research, stock-fundamental |
| `references/market-sizing-principles.md` | 双重验证原则、三种测算方法、无公开数据另类路径、常见测算错误 | industry-research |
| `references/moat-framework.md` | 护城河两大类型、强弱信号、假护城河清单、持续性判断、与生命周期关系 | industry-research, stock-fundamental |
| `references/pitfalls.md` | 十二大通用陷阱、专家访谈三步处理法 | industry-research, stock-fundamental |
| `references/time-consistency.md` | 时间口径匹配规则、输出标注要求、常见违规情形 | industry-research, stock-fundamental |
| `references/scqr-principle.md` | SCQR 汇报顺序、受众对应结构、结论质量要求、输出深度分级 | industry-research, stock-fundamental |

---

## 加载原则

- 按需加载，不批量读取
- 每个引用 skill 的 SKILL.md 里有对应的「文件加载规则」表格，按任务场景精确指向
- 本文件本身不包含分析方法，只作为路由层

---

## 设计原则

**底座稳则套件稳。**
共用逻辑集中在这里维护，避免各 skill 重复定义同一概念导致不一致。更新一处，全局生效。
