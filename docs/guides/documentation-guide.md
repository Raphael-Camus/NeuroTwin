# 文档规范

## 目标

确保项目在研究、实现、实验和展示阶段都具有连续、可追踪、可复现的文档支撑。

## 建议维护的文档

1. `README.md`
   用于说明项目定位、目标、目录结构和总体进展。

2. `docs/PROJECT_LOG.md`
   用于记录日常推进过程、阶段成果、问题和后续计划。

3. `docs/RESEARCH_PLAN.md`
   用于维护研究目标、技术路线、任务拆解和阶段安排。

4. 后续可新增文档
   - `docs/LITERATURE_REVIEW.md`
   - `docs/DATASET_NOTES.md`
   - `docs/MODEL_DESIGN.md`
   - `docs/EXPERIMENT_LOG.md`
   - `docs/DEMO_PLAN.md`

## Git 使用建议

1. 每完成一个相对独立的工作单元就提交一次。
2. 提交信息尽量准确描述变更内容。
3. 文档更新应与代码修改同步提交，避免代码和记录脱节。

## 推荐提交信息风格

- `docs: initialize project documentation`
- `docs: add literature review notes`
- `data: add dataset inventory`
- `feat: implement fmri preprocessing pipeline`
- `exp: record functional connectivity baseline`

## 工作原则

1. 所有关键决策要留下文字依据。
2. 所有实验要能追溯输入、方法与结果。
3. 所有阶段成果要能服务于最终汇报、论文或答辩展示。
