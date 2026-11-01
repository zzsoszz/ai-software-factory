# AI Software Factory

把 GitHub Projects 中的任务交给 Codex，经过开发、QA 和 Review，以 PR 交付。
本仓库是工厂控制仓库，使用 super-board 3.3.0。业务应用尚未定义。

[任务看板](https://github.com/users/zzsoszz/projects/1) · [项目范围](docs/super-board/PROJECT.md) · [安装来源](docs/super-board/INSTALLATION.md)

## 验证安装

需要 Python 3.10+、Bash、Node.js、Git、jq、GitHub CLI 和已登录的 Codex CLI。

```bash
python3 scripts/check_factory.py
python3 -m unittest discover -s tests -v
python3 .agents/bin/super-board-skills-ready.py --root . --host codex --profile setup
```

前两条命令离线运行，也由 CI 和合并验证配置执行。
第三条检查本机实际可用的 worker 技能。缺失项需安装到项目或用户技能目录。

## 运行任务

初始化 PR 合并后，在本仓库的新 Codex 会话执行：

```text
$super-board lint
$super-board run ai-software-factory
```

任务进入 Ready 前，按 [任务格式](docs/agents/issue-tracker.md) 写清验收条件。
流水线采用单任务并发。当前每次合并均需人工审核，数据库迁移不自动执行。
完整启动检查见 [pre-flight.md](docs/super-board/pre-flight.md)。

查看状态：

```bash
python3 .agents/bin/super-board-status.py ai-software-factory
```

停止运行使用 `$super-board stop`。进度保存在 GitHub 看板，恢复使用同一个 run 命令。
