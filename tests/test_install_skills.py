import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import install_skills as installer


class ProjectRulesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "source"
        self.skill = self.repo / "design-dialogue"
        (self.skill / "assets").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("测试 skill", encoding="utf-8")
        self.fragment = self.skill / "assets" / "AGENTS.fragment.md"
        self.fragment.write_text("规则第一版\n", encoding="utf-8")
        self.project = self.root / "project"
        self.project.mkdir()
        self.target = self.project / "AGENTS.md"

    def run_install(self, *args, answers=()):
        with patch.object(installer, "REPO_ROOT", self.repo), patch.object(
            installer, "project_skills_dir", return_value=self.project / ".agents" / "skills"
        ), patch.object(
            installer, "user_skills_dir", return_value=self.root / "user-skills"
        ), patch("sys.argv", ["install_skills.py", *args]), patch(
            "builtins.input", side_effect=answers
        ), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return installer.main()

    def test_create_repeat_and_update_preserve_surroundings(self):
        self.assertEqual(self.run_install("design-dialogue", "--project"), 0)
        first = self.target.read_bytes()
        self.assertEqual(self.run_install("design-dialogue", "--project", "--force"), 0)
        self.assertEqual(self.target.read_bytes(), first)
        self.target.write_bytes(b"# Existing\r\n\r\n" + first + b"\nFooter\n")
        self.fragment.write_text("规则第二版\n", encoding="utf-8")
        self.assertEqual(self.run_install("design-dialogue", "--project", "--force"), 0)
        updated = self.target.read_bytes()
        self.assertTrue(updated.startswith(b"# Existing\r\n\r\n"))
        self.assertTrue(updated.endswith(b"\nFooter\n"))
        self.assertIn("规则第二版".encode(), updated)
        self.assertNotIn("规则第一版".encode(), updated)

    def test_append_preserves_existing_text(self):
        self.target.write_bytes(b"Existing without newline")
        self.assertEqual(self.run_install("design-dialogue", "--project"), 0)
        self.assertTrue(self.target.read_bytes().startswith(b"Existing without newline\n\n"))

    def test_manual_edit_survives_force_and_retries(self):
        self.run_install("design-dialogue", "--project")
        edited = self.target.read_bytes().replace("规则第一版".encode(), "用户修改".encode())
        self.target.write_bytes(edited)
        for _ in range(2):
            self.assertEqual(self.run_install("design-dialogue", "--project", "--force"), 1)
            self.assertEqual(self.target.read_bytes(), edited)

    def test_damaged_duplicate_and_symlink_are_preserved(self):
        self.run_install("design-dialogue", "--project")
        original = self.target.read_bytes()
        for damaged in (original + original, original.replace(b":end -->", b":end broken")):
            self.target.write_bytes(damaged)
            self.assertEqual(self.run_install("design-dialogue", "--project", "--force"), 1)
            self.assertEqual(self.target.read_bytes(), damaged)
        self.target.unlink()
        other = self.root / "external.md"
        other.write_bytes(b"External")
        self.target.symlink_to(other)
        self.assertEqual(self.run_install("design-dialogue", "--project", "--force"), 1)
        self.assertEqual(other.read_bytes(), b"External")

    def test_user_list_skip_failure_and_unrelated_skill_do_not_inject(self):
        self.assertEqual(self.run_install("design-dialogue", "--user"), 0)
        self.assertEqual(self.run_install("--list", "--project"), 0)
        unrelated = self.repo / "other-skill"
        unrelated.mkdir()
        (unrelated / "SKILL.md").write_text("其他", encoding="utf-8")
        self.assertEqual(self.run_install("other-skill", "--project"), 0)
        with patch.object(installer, "install_skill", side_effect=OSError("模拟失败")):
            self.assertEqual(self.run_install("design-dialogue", "--project"), 1)
        self.assertFalse(self.target.exists())
        self.run_install("design-dialogue", "--project")
        self.target.unlink()
        self.assertEqual(self.run_install("design-dialogue", "--project", answers=["n"]), 0)
        self.assertFalse(self.target.exists())

    def test_interactive_project_install(self):
        self.assertEqual(self.run_install(answers=["1", "y", "all"]), 0)
        self.assertTrue(self.target.exists())

    def test_write_failure_is_reported_with_skill_installed(self):
        with patch.object(installer, "sync_dialogue_rules", side_effect=OSError("无法写入")):
            self.assertEqual(self.run_install("design-dialogue", "--project"), 1)
        self.assertTrue((self.project / ".agents/skills/design-dialogue/SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
