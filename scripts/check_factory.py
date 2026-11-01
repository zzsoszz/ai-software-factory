#!/usr/bin/env python3
"""Check this factory's configuration and installed engine without network access."""
import argparse
import ast
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / '.claude/super-board/configs/ai-software-factory.json'
COLUMNS = ['Backlog', 'Ready', 'Building', 'QA', 'Review', 'Blocked', 'Done']
CORE = [
    'super-board-verification-ready.py', 'super-board-merge-policy.py',
    'super-board-merge-gate.sh', 'super-board-codex-wave.sh',
    'super-board-lane.sh', 'super-board-status.py', 'super-board-github-read.py',
    'super-board-skills-ready.py',
]


def github_repo(remote):
    match = re.fullmatch(
        r'(?:https?://github\.com/|git@github\.com:|ssh://git@github\.com/)'
        r'([\w.-]+/[\w.-]+?)(?:\.git)?/?', remote, re.IGNORECASE)
    return match[1].lower() if match else None


def command(args, source=None):
    result = subprocess.run(args, cwd=ROOT, input=source, text=True,
                            capture_output=True, timeout=30)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"{' '.join(map(str, args))}: {detail or '检查失败'}")
    return result.stdout.strip()


def check(config_path):
    cfg = json.loads(config_path.read_text(encoding='utf-8'))
    if not isinstance(cfg, dict):
        raise ValueError('配置必须是 JSON 对象')
    if cfg.get('host') != 'codex':
        raise ValueError('本工厂的 host 必须是 codex')
    if cfg.get('columns') != COLUMNS:
        raise ValueError('columns 必须按顺序包含 Backlog、Ready、Building、QA、Review、Blocked、Done')
    labels = cfg.get('labels')
    if not isinstance(labels, list) or sorted(labels) != ['bug', 'feature', 'qa']:
        raise ValueError('labels 必须恰好包含 bug、feature、qa')
    repo = cfg.get('repo')
    if not isinstance(repo, dict) or repo.get('path') != '.':
        raise ValueError('repo.path 必须是 .，使独立 worktree 使用自己的项目根目录')
    remote = repo.get('remote')
    if not isinstance(remote, str) or not github_repo(remote):
        raise ValueError('repo.remote 必须是有效的 GitHub HTTPS 或 SSH 仓库地址')
    actual = command(['git', 'remote', 'get-url', 'origin'])
    if github_repo(remote) != github_repo(actual):
        raise ValueError('配置的 repo.remote 与当前 origin 不一致')
    project = cfg.get('project')
    if (not isinstance(project, dict) or not isinstance(project.get('owner'), str)
            or not project['owner'].strip() or type(project.get('number')) is not int
            or project['number'] < 1):
        raise ValueError('project 必须包含非空 owner 和正整数 number')
    if cfg.get('merge_policy', {}).get('default') not in ('human', 'auto'):
        raise ValueError('merge_policy.default 必须明确为 human 或 auto')
    engine = ROOT / '.agents/bin'
    missing = [name for name in CORE if not (engine / name).is_file()]
    if missing:
        raise ValueError('引擎安装不完整：' + ', '.join(missing))
    command([sys.executable, str(engine / CORE[0]), '--config', str(config_path)])
    scripts = sorted((ROOT / '.agents/bin').glob('*'))
    scripts += sorted((ROOT / '.agents/hooks').glob('*.py'))
    scripts += sorted((ROOT / '.agents/workflows').glob('*.js'))
    counts = {'.py': 0, '.sh': 0, '.js': 0}
    for path in scripts:
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        elif path.suffix == '.sh':
            command(['bash', '-n', str(path)])
        elif path.suffix == '.js':
            source = path.read_text(encoding='utf-8').replace('export const meta', 'const meta')
            command(['node', '--check', '--input-type=module'], '(async function(){\n' + source + '\n})')
        else:
            continue
        counts[path.suffix] += 1
    if not counts['.js']:
        raise ValueError('缺少已安装的工作流 JavaScript 文件')
    print('PASS: 配置、origin、worktree 路径和引擎验证命令门禁')
    print('PASS: 引擎语法检查 ' + ', '.join(f'{count} {kind}' for kind, count in counts.items()))
    print('检查范围为本地配置与引擎，不代表 GitHub 权限或真实任务已完成端到端验收。')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=CONFIG)
    args = parser.parse_args()
    try:
        check(args.config.resolve())
    except (OSError, ValueError, SyntaxError, TypeError, AttributeError,
            subprocess.SubprocessError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
