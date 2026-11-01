"""Observable policy decisions from the installed super-board command interfaces."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / '.agents/bin'


class FactoryPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        config = ROOT / '.claude/super-board/configs/ai-software-factory.json'
        self.config = copy.deepcopy(json.loads(config.read_text(encoding='utf-8')))

    def write_config(self, config):
        path = self.work / 'config.json'
        path.write_text(json.dumps(config), encoding='utf-8')
        return path

    def ready(self, commands):
        config = dict(self.config, verify_commands=commands)
        return subprocess.run([
            sys.executable, str(ENGINE / 'super-board-verification-ready.py'),
            '--config', str(self.write_config(config)),
        ], capture_output=True, text=True, timeout=10)

    def policy(self, config=None, path='docs/guide.md', added='A useful clarification.', labels=()):
        cfg = config if config is not None else self.config
        meta = self.work / 'meta.json'
        meta.write_text(json.dumps({
            'files': [{'path': path, 'additions': 1, 'deletions': 0}],
            'labels': [{'name': label} for label in labels], 'body': '',
            'additions': 1, 'deletions': 0,
        }), encoding='utf-8')
        diff = self.work / 'change.diff'
        diff.write_text(f'--- a/{path}\n+++ b/{path}\n@@ -0,0 +1 @@\n+{added}\n', encoding='utf-8')
        result = subprocess.run([
            sys.executable, str(ENGINE / 'super-board-merge-policy.py'),
            '--config', str(self.write_config(cfg)), '--meta', str(meta), '--diff', str(diff),
        ], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def automatic_config(self):
        config = copy.deepcopy(self.config)
        config['human_approves_merge'] = False
        config['merge_policy']['default'] = 'auto'
        return config

    def test_empty_or_unusable_checks_stop_dispatch(self):
        for commands in ([], [' ', '\t\n'], ['git\x00diff'], 'python3 check.py'):
            with self.subTest(commands=commands):
                result = self.ready(commands)
                self.assertEqual(result.returncode, 9)
                self.assertIn('verification-readiness', result.stderr)

    def test_real_project_check_command_is_accepted(self):
        self.assertEqual(self.ready(['python3 scripts/check_factory.py']).returncode, 0)

    def test_normal_change_waits_for_human_under_initial_policy(self):
        result = self.policy()
        self.assertTrue(result['human'])
        self.assertEqual(result['run'], [])
        self.assertFalse(result['done'])

    def test_explicit_auto_allows_a_normal_change(self):
        result = self.policy(self.automatic_config())
        self.assertEqual(result['human'], [])
        self.assertEqual(result['needs_you'], [])

    def test_codex_without_auto_opt_in_waits_for_human(self):
        config = self.automatic_config()
        del config['merge_policy']['default']
        self.assertTrue(self.policy(config)['human'])

    def test_sensitive_changes_still_need_a_human_under_auto(self):
        cases = [
            ('src/auth/login.py', 'return session', (), 'auth'),
            ('src/billing/invoice.py', 'return invoice', (), 'money'),
            ('migrations/change.sql', 'DROP TABLE users;', (), 'schema'),
            ('src/config.py', 'enabled = True', ('security',), 'auth'),
        ]
        for path, added, labels, category in cases:
            with self.subTest(path=path, labels=labels):
                result = self.policy(self.automatic_config(), path, added, labels)
                self.assertIn(category, {finding['category'] for finding in result['human']})

    def test_live_migration_never_runs_with_no_allowed_environments(self):
        config = self.automatic_config()
        config['migrations']['commands'] = {'live': 'apply-live-migration'}
        result = self.policy(config, path='supabase/migrations/add_table.sql',
                             added='CREATE TABLE example(id integer);')
        self.assertEqual(result['run'], [])
        self.assertTrue(result['needs_you'])
        self.assertFalse(result['done'])

    def test_invalid_factory_config_reports_failure_without_traceback(self):
        path = self.work / 'broken.json'
        for data in ('{broken', 'null', '{"host": "claude"}'):
            with self.subTest(data=data):
                path.write_text(data, encoding='utf-8')
                result = subprocess.run([
                    sys.executable, str(ROOT / 'scripts/check_factory.py'), '--config', str(path),
                ], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 1)
                self.assertIn('FAIL:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
