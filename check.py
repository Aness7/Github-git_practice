#!/usr/bin/env python3
"""Self-check for the Week 01 Git ladder.

Run it inside the repository you are working in — it reads your real Git
history and tells you which assignments are already done.

    python check.py                # check everything it can
    python check.py 3              # check assignment 3 only
    python check.py --repo ~/code/git-practice

Nothing is uploaded and nothing is modified. It only reads.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PASS, FAIL, MANUAL, SKIP = "PASS", "FAIL", "MANUAL", "SKIP"

COMMIT_RE = re.compile(r"^w\d{2}: .+")
LAZY_SUBJECTS = {
    "update", "updates", "changes", "change", "fix", "fixes", "final",
    "last", "new", "test", "commit", "wip", "stuff", "done", "asdf",
}
# Real markers always start a line; the middle one carries no trailing space.
CONFLICT_MARKERS = ("<<<<<<< ", "=======", ">>>>>>> ")
SECRET_PATHS = re.compile(r"(^|/)(\.env|\.env\.local|.*\.env)$")
VENV_PATHS = re.compile(r"(^|/)(\.venv|venv|env|week-\d+-env)/")


class Git:
    """Thin read-only wrapper around the git CLI."""

    def __init__(self, repo: Path):
        self.repo = repo

    def run(self, *args: str) -> str:
        proc = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise GitError(proc.stderr.strip() or f"git {' '.join(args)} failed")
        return proc.stdout.strip()

    def ok(self, *args: str) -> bool:
        try:
            self.run(*args)
            return True
        except GitError:
            return False

    # --- convenience readers -------------------------------------------------

    def commits(self, rev: str = "HEAD") -> list[tuple[str, str]]:
        """[(sha, subject), ...] newest first."""
        try:
            out = self.run("log", "--format=%H%x1f%s", rev)
        except GitError:
            return []
        rows = []
        for line in out.splitlines():
            if "\x1f" in line:
                sha, subject = line.split("\x1f", 1)
                rows.append((sha, subject))
        return rows

    def changed_files(self, sha: str) -> set[str]:
        """Files touched by a commit (works for the root commit too)."""
        out = self.run(
            "show", "--pretty=format:", "--name-only", "--no-renames", sha
        )
        return {line for line in out.splitlines() if line}

    def parents(self, sha: str) -> list[str]:
        return self.run("log", "-1", "--format=%P", sha).split()

    def tracked(self, rev: str = "HEAD") -> set[str]:
        try:
            return set(self.run("ls-tree", "-r", "--name-only", rev).splitlines())
        except GitError:
            return set()

    def file_at(self, rev: str, path: str) -> str | None:
        try:
            return self.run("show", f"{rev}:{path}")
        except GitError:
            return None

    def branches(self) -> list[str]:
        try:
            out = self.run("for-each-ref", "--format=%(refname:short)", "refs/heads")
        except GitError:
            return []
        return [b for b in out.splitlines() if b]

    def remotes(self) -> dict[str, str]:
        try:
            out = self.run("remote", "-v")
        except GitError:
            return {}
        remotes = {}
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                remotes[parts[0]] = parts[1]
        return remotes

    def branch_only_commits(self, branch: str, main: str) -> list[str]:
        """Commits belonging to `branch` that never sat on main's own line.

        Survives the branch being merged later, which plain `main..branch`
        does not.
        """
        try:
            main_line = set(self.run("rev-list", "--first-parent", main).split())
            branch_commits = self.run("rev-list", branch).split()
        except GitError:
            return []
        return [c for c in branch_commits if c not in main_line]

    def merged_side_branch(self, main: str) -> str | None:
        """The second parent of the newest merge on main.

        Lets a branch still be graded after `git branch -d` has removed the ref.
        """
        for sha, _ in self.commits(main):
            parents = self.parents(sha)
            if len(parents) > 1:
                return parents[1]
        return None

    def main_branch(self) -> str:
        for name in ("main", "master"):
            if self.ok("rev-parse", "--verify", name):
                return name
        return "HEAD"


class GitError(RuntimeError):
    pass


class Result:
    def __init__(self, status: str, message: str, hint: str = ""):
        self.status, self.message, self.hint = status, message, hint


def ok(msg: str) -> Result:
    return Result(PASS, msg)


def no(msg: str, hint: str = "") -> Result:
    return Result(FAIL, msg, hint)


def manual(msg: str) -> Result:
    return Result(MANUAL, msg)


def skip(msg: str) -> Result:
    return Result(SKIP, msg)


# --- assignment checks -------------------------------------------------------


def check_01(g: Git) -> Result:
    commits = g.commits()
    if len(commits) < 3:
        return no(
            f"found {len(commits)} commit(s), need at least 3",
            "One commit per step: initial project, add about page, update README.",
        )
    tracked = g.tracked()
    missing = [f for f in ("README.md", "about.txt") if f not in tracked]
    if missing:
        return no(f"missing tracked file(s): {', '.join(missing)}")
    readme_touches = sum(
        1 for sha, _ in commits if "README.md" in g.changed_files(sha)
    )
    if readme_touches < 2:
        return no(
            "README.md was only written once",
            "Assignment 1 asks you to edit it later and commit that change too.",
        )
    bad = [s for _, s in commits if not COMMIT_RE.match(s)]
    if bad:
        return no(
            f"{len(bad)} commit subject(s) not in 'w01: ...' form, e.g. {bad[0]!r}"
        )
    return ok(f"{len(commits)} commits, README edited across {readme_touches} of them")


def check_02(g: Git) -> Result:
    trio = {"README.md", "main.py", "notes.txt"}
    commits = g.commits()
    solo = None
    for sha, subject in commits:
        touched = g.changed_files(sha)
        if touched & trio == {"main.py"}:
            solo = (sha, subject)
            break
    if solo is None:
        return no(
            "no commit contains main.py alone",
            "Stage only main.py (git add main.py) while README.md and notes.txt "
            "stay modified but unstaged, then commit.",
        )
    # the other two must arrive in a *later* commit (i.e. earlier in log order)
    solo_index = [sha for sha, _ in commits].index(solo[0])
    later = commits[:solo_index]
    arrived = set()
    for sha, _ in later:
        arrived |= g.changed_files(sha) & (trio - {"main.py"})
    if not arrived:
        return no(
            "README.md / notes.txt never got committed after the main.py commit",
            "Commit them separately afterwards so the two-commit split is visible.",
        )
    gitignore = g.file_at("HEAD", ".gitignore")
    if gitignore is None:
        return no(
            "no .gitignore committed",
            "Add one ignoring .env and your virtualenv folder.",
        )
    has_env = ".env" in gitignore
    has_venv = any(p in gitignore for p in (".venv", "venv/", "env/"))
    if not (has_env and has_venv):
        return no(
            ".gitignore does not cover both .env and a virtualenv folder",
            "Staging picks what enters a snapshot; .gitignore states what never may.",
        )
    return ok(f"main.py committed alone in {solo[0][:7]}, rest followed, .gitignore present")


def check_03(g: Git) -> Result:
    commits = g.commits()
    if len(commits) < 5:
        return no(
            f"found {len(commits)} commit(s), need at least 5",
            "Break the work into steps: create, implement, implement, document, polish.",
        )
    problems = []
    for sha, subject in commits:
        if not COMMIT_RE.match(subject):
            problems.append(f"{sha[:7]} {subject!r} — not 'w01: ...'")
            continue
        body = subject.split(": ", 1)[1].strip()
        if body.lower().rstrip(".!") in LAZY_SUBJECTS:
            problems.append(f"{sha[:7]} {subject!r} — says nothing")
        if len(subject) > 72:
            problems.append(f"{sha[:7]} subject is {len(subject)} chars (max 72)")
    if problems:
        return no(f"{len(problems)} message problem(s)", "\n      ".join(problems[:5]))
    oversized = [
        (sha, len(g.changed_files(sha)))
        for sha, _ in commits[:-1]  # the root commit may legitimately be large
        if len(g.changed_files(sha)) > 10
    ]
    if oversized:
        sha, n = oversized[0]
        return no(
            f"commit {sha[:7]} touches {n} files",
            "Keep one logical change per commit.",
        )
    return ok(f"{len(commits)} commits, all well-formed and small")


def check_04(g: Git) -> Result:
    if "notes.txt" not in g.tracked():
        return no("notes.txt is not tracked")
    history = [
        sha for sha, _ in g.commits() if "notes.txt" in g.changed_files(sha)
    ]
    if len(history) < 3:
        return no(
            f"notes.txt only changed in {len(history)} commit(s), need 3",
            "Hello → Hello World → Hello World!!!, one commit each.",
        )
    contents = [(g.file_at(sha, "notes.txt") or "").strip() for sha in history]
    wanted = ["Hello World!!!", "Hello World", "Hello"]
    if not all(any(w == c for c in contents) for w in wanted):
        return no(
            "the three expected versions are not all in history",
            f"Found: {contents[:3]}",
        )
    return ok(f"3 versions of notes.txt recoverable across {len(history)} commits")


def check_05(g: Git) -> Result:
    """Isolation is provable even after the branch has been merged (assignment 6)
    and after the branch ref has been deleted, so work from main's first-parent
    line and fall back to the merge commit's second parent."""
    main = g.main_branch()
    tip = "feature/about" if "feature/about" in g.branches() else None
    if tip is None:
        tip = g.merged_side_branch(main)
    if tip is None:
        return no(
            "no branch 'feature/about', and no merged branch in history",
            f"Branches found: {', '.join(g.branches()) or 'none'}",
        )
    own = g.branch_only_commits(tip, main)
    if len(own) < 2:
        return no(
            f"feature/about has {len(own)} commit(s) of its own, need 2",
            "Commit twice while you are on the branch, not on main.",
        )
    fork_point = g.run("rev-parse", f"{own[-1]}^")
    before = g.file_at(fork_point, "README.md")
    after = g.file_at("feature/about", "README.md")
    if before is not None and before == after:
        return no(
            "README.md is unchanged on the branch",
            "The point is to see the file differ depending on the branch you are on.",
        )
    label = "feature/about" if tip == "feature/about" else f"the merged branch ({tip[:7]})"
    return ok(f"{label} holds {len(own)} isolated commits, README diverged")


def check_06(g: Git) -> Result:
    merges = [sha for sha, _ in g.commits() if len(g.parents(sha)) > 1]
    if not merges:
        return no(
            "no merge commit in history",
            "Switch to main and run: git merge feature/<name>",
        )
    return ok(f"{len(merges)} merge commit(s) found, e.g. {merges[0][:7]}")


def check_07(g: Git) -> Result:
    remotes = g.remotes()
    if "origin" not in remotes:
        return no("no 'origin' remote — did you clone your fork?")
    if "upstream" not in remotes:
        return no(
            "no 'upstream' remote",
            "git remote add upstream https://github.com/Hacenbens/iot-backend-course.git",
        )
    if "iot-backend-course" not in remotes["origin"]:
        return skip("origin does not look like the course fork — run this in your fork")
    student = [b for b in g.branches() if re.match(r"student/[^/]+/week-01$", b)]
    if not student:
        return no(
            "no branch named student/YOUR_USERNAME/week-01",
            f"Branches found: {', '.join(g.branches()) or 'none'}",
        )
    branch = student[0]
    if not g.ok("rev-parse", "--verify", f"{branch}@{{upstream}}"):
        return no(
            f"{branch} has never been pushed",
            f"git push -u origin {branch}",
        )
    if not g.ok("rev-parse", "--verify", "upstream/main"):
        return no(
            "you have never fetched upstream",
            "git fetch upstream   — this is how you get each week's new material.",
        )
    return ok(f"fork + upstream configured, {branch} pushed")


def check_08(g: Git) -> Result:
    main = g.main_branch()
    merges = [sha for sha, _ in g.commits(main) if len(g.parents(sha)) > 1]
    if len(merges) < 2:
        return no(
            f"{len(merges)} merge commit(s) on {main}, need 2",
            "Two feature branches, each merged in — yours and your partner's.",
        )
    return ok(f"{len(merges)} feature branches merged into {main}")


def check_09(g: Git) -> Result:
    """A real conflict means both sides of a merge touched the same file."""
    for sha, _ in g.commits():
        parents = g.parents(sha)
        if len(parents) < 2:
            continue
        try:
            base = g.run("merge-base", parents[0], parents[1])
        except GitError:
            continue
        side_a = set(g.run("diff", "--name-only", base, parents[0]).splitlines())
        side_b = set(g.run("diff", "--name-only", base, parents[1]).splitlines())
        overlap = {f for f in side_a & side_b if f}
        if overlap:
            leftovers = markers_in_tree(g)
            if leftovers:
                return no(
                    f"conflict markers still in {', '.join(sorted(leftovers)[:3])}",
                    "Delete the <<<<<<< ======= >>>>>>> lines and keep real code.",
                )
            return ok(
                f"merge {sha[:7]} resolved a real overlap on {', '.join(sorted(overlap)[:2])}"
            )
    return no(
        "no merge where both sides changed the same file",
        "Assignment 9 needs a genuine conflict — same line, two branches.",
    )


def check_10(g: Git) -> Result:
    return manual("reviewed on your Pull Request (maintainer requests changes, you push a fix)")


def check_11(g: Git) -> Result:
    reverts = [s for _, s in g.commits() if s.startswith("Revert ")]
    if not reverts:
        return no(
            "no revert commit in history",
            "git revert <sha> — the only recovery tool that leaves a trace, "
            "which is why it is the safe one on a shared branch.",
        )
    return ok(f"{len(reverts)} revert commit(s); restore/reset are self-reported")


def check_12(g: Git) -> Result:
    return manual("team repository — graded from its PR history, not from this repo")


CHECKS = {
    1: ("First contact with Git", check_01),
    2: ("The staging area", check_02),
    3: ("Commit like a professional", check_03),
    4: ("Time travel", check_04),
    5: ("Branches", check_05),
    6: ("Merge", check_06),
    7: ("GitHub", check_07),
    8: ("Collaboration", check_08),
    9: ("Merge conflict", check_09),
    10: ("Open source simulation", check_10),
    11: ("Recover from mistakes", check_11),
    12: ("Mini team project", check_12),
}


# --- repository hygiene ------------------------------------------------------


def markers_in_tree(g: Git) -> set[str]:
    """Tracked text files still containing conflict markers.

    The ladder's own documentation is skipped: it teaches what the markers
    look like, and flagging it inside a student's fork would be noise.
    """
    bad = set()
    for path in g.tracked():
        if "assignment/git-ladder/" in path:
            continue
        full = g.repo / path
        try:
            text = full.read_text(encoding="utf-8", errors="ignore")
        except (OSError, IsADirectoryError, UnicodeDecodeError):
            continue
        lines = text.splitlines()
        if any(line.startswith(CONFLICT_MARKERS) for line in lines):
            bad.add(path)
    return bad


def hygiene(g: Git) -> list[str]:
    warnings = []
    tracked = g.tracked()
    secrets = [p for p in tracked if SECRET_PATHS.search(p)]
    if secrets:
        warnings.append(f"secret file(s) committed: {', '.join(sorted(secrets)[:3])}")
    venvs = {VENV_PATHS.search(p).group(0).strip("/") for p in tracked if VENV_PATHS.search(p)}
    if venvs:
        warnings.append(f"virtualenv committed: {', '.join(sorted(venvs)[:3])}")
    leftovers = markers_in_tree(g)
    if leftovers:
        warnings.append(f"conflict markers left in: {', '.join(sorted(leftovers)[:3])}")
    return warnings


# --- reporting ---------------------------------------------------------------

SYMBOL = {PASS: "PASS", FAIL: "FAIL", MANUAL: "  ~ ", SKIP: "  - "}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("only", nargs="*", type=int, help="assignment numbers to check")
    parser.add_argument("--repo", default=".", help="path to the repository")
    args = parser.parse_args(argv)

    repo = Path(args.repo).expanduser().resolve()
    g = Git(repo)
    if not g.ok("rev-parse", "--git-dir"):
        print(f"{repo} is not a Git repository. Did you run 'git init'?")
        return 2

    wanted = args.only or sorted(CHECKS)
    unknown = [n for n in wanted if n not in CHECKS]
    if unknown:
        print(f"No such assignment: {unknown[0]}. Pick from 1-12.")
        return 2

    print(f"\nGit ladder — checking {repo}\n")
    passed = failed = 0
    for number in wanted:
        title, check = CHECKS[number]
        try:
            result = check(g)
        except GitError as exc:
            result = no(f"git error: {exc}")
        print(f"  [{SYMBOL[result.status]}] {number:>2}. {title}")
        print(f"        {result.message}")
        if result.hint:
            print(f"        → {result.hint}")
        if result.status == PASS:
            passed += 1
        elif result.status == FAIL:
            failed += 1

    warnings = hygiene(g)
    if warnings:
        print("\n  Repository hygiene:")
        for w in warnings:
            print(f"        ! {w}")

    print(f"\n  {passed} passed, {failed} to fix.")
    if not args.only and "upstream" not in g.remotes():
        print(
            "\n  Note: this repository has no 'upstream' remote, so it looks like your\n"
            "  Part A practice repo. Assignments 7-12 are meant to be done in your fork\n"
            "  of the course repo — their failures above are expected here."
        )
    print()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
