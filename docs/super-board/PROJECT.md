# AI Software Factory

本仓库是 AI 软件工厂的控制仓库，保存流水线配置、已安装的 super-board 引擎和工厂自身的验证工具。业务应用尚未定义。

## 本地验证

在仓库根目录执行：

```bash
python3 scripts/check_factory.py
python3 -m unittest discover -s tests -v
```

第一条命令检查真实配置、Git origin、独立 worktree 的路径约定、引擎验证命令门禁以及已安装脚本的语法。它使用 Python、Bash 和 Node，不访问网络或读取用户级技能。

第二条命令调用已安装引擎的命令行接口，验证空测试命令会阻止调度、初始合并策略要求人工审核，以及显式启用自动合并后仍保留登录、资金、破坏性数据库变更和线上迁移的人工关口。

这些检查证明本地配置、引擎接口和合并策略的行为，不证明 GitHub 权限、模型可用性或真实任务全链路已经验收。

## 运行边界

初始配置使用 Codex，目标分支为 `main`，合并由人工审核。数据库自动迁移没有获准的环境。

任务通过关联的 GitHub Project 保存状态。流水线按 Building、QA 和 Review 执行，构建工作放在独立 worktree 中。工厂运行与停止遵循仓库中的 super-board 技能说明。

业务项目接入时，为该项目设置真实构建和测试命令，再用一个明确验收标准的任务验证开发、QA、Review 和 PR 交付。
