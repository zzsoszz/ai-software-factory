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
