# 安装来源与验证范围

引擎来源为 [EricTechPro/super-board](https://github.com/EricTechPro/super-board)，版本 3.3.0，提交 `d0b7d5a6850614ca809477c1af43d5d7da408726`。
使用其 `install.sh --hosts codex --protect-main` 安装到本仓库。
引擎文件按安装器布局提交，便于新 worktree 使用同一套脚本。

额外的 `verification-before-completion` 来自本机已缓存的 Superpowers 插件。
`testing-strategy` 来自 `anthropics/knowledge-work-plugins`。
其他 worker 技能由本机用户目录提供，使用引擎的技能就绪检查逐项解析。迁移机器时需重新验证这些依赖。

本机引擎原始离线测试的 64 个测试组已通过。该结果适用于上述引擎提交，不是业务任务验收。
本仓库另有安装检查与策略测试，覆盖缺少验证命令时拒绝执行、人工合并默认值以及敏感变更审核规则。
GitHub 权限、Codex 模型可用性和真实任务交付还需在线检查。

Claude 的 protected-push hooks 已安装。Codex 不运行 Claude hooks；Codex worker 使用引擎设置的文件权限和 merge gate。
本次没有配置 GitHub 服务器端分支保护。人工通过 GitHub 合并 PR 时，应先检查 CI 和审查证据。
