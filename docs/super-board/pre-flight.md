# 启动检查

1. 确认初始化 PR 已审核，工厂文件已进入远端 main。
2. 从项目目录运行 `python3 scripts/check_factory.py` 和 `python3 -m unittest discover -s tests -v`。
3. 运行 `python3 .agents/bin/super-board-setup.py check --root . --host codex --pack /home/qingtian/ai-factory/super-board --text`。
4. 确认 GitHub 登录、Projects 访问、Codex 登录及所需模型可用。
5. 为任务填写可验证的验收条件，检查依赖后再移入 Ready。
6. 在新的 Codex 会话运行 `$super-board lint`，然后运行 `$super-board run ai-software-factory`。

当前采用人工合并。Ready 为空时不派发任务。
首个真实任务尚未完成端到端验收。安装自检通过仅代表可以进入任务验收阶段。
