# AI Software Factory

本仓库管理 GitHub Projects 驱动的 Codex 开发流水线。项目范围见 `docs/super-board/PROJECT.md`。

## 验证

运行 `.claude/super-board/configs/ai-software-factory.json` 中的 `verify_commands`。
新增业务功能时，把对应的真实测试加入该配置。配置检查不能代替业务行为测试。

## 项目规则

- 默认用中文沟通。
- 在独立任务分支和 worktree 中开发，通过 PR 交付。
- 合并、数据库和运行参数以工厂配置为准。修改这些参数时展示差异与测试证据供人工审核。
- 工厂引擎位于 `.agents/`，`.claude/` 和 `.codex/` 使用相对链接。
- 升级引擎时保留来源与版本记录，重新运行策略测试及技能就绪检查。
- 安装了 Claude hooks 不代表 Codex 会执行这些 hooks。
- 密钥保存在认证工具中，不写入仓库、任务或证据。
- 接入业务应用时先读取该应用的规则与测试，不把工厂自检冒充应用验收。

<!-- super-board:begin v3.3.0 (managed; edits inside are overwritten on upgrade) -->
## Super Board

配置：`.claude/super-board/configs/ai-software-factory.json`。权限与合并决策以此配置为准。

| 操作 | Codex 技能 |
|---|---|
| 安装或修复 | `$super-board onboard` |
| 检查任务验收条件 | `$super-board lint` |
| 运行流水线 | `$super-board run ai-software-factory` |
| 查看或停止 | `$super-board status`、`$super-board stop` |

任务按 Backlog、Ready、Building、QA、Review、Blocked、Done 流转。
`qa` 标签直接进入 QA，其他任务先开发。每个任务使用独立 worktree 和分支。
调度会话只负责派发，开发、QA 和 Review 由对应 worker 执行。
Review 按配置请求人工审核，通过引擎的 merge gate 处理合并，不直接绕过检查合并。

任务格式见 `docs/agents/issue-tracker.md`。
提交与 PR 格式见 `.claude/skills/super-board/references/writing-standard.md`。
<!-- super-board:end -->
