# Git ladder — submission

**Student name:**
**Aness**

## Repositories

| What | URL |
|---|---|
| Part A practice repo (`git-practice`) | |
| Team repo (assignment 12) | |
| Pull Request for assignment 10 | |

## Which assignments did you complete?

| # | Assignment | Done | Notes |
|---|---|---|---|
| 1 | First contact with Git | ☐ | |
| 2 | The staging area | ☐ | |
| 3 | Commit like a professional | ☐ | |
| 4 | Time travel | ☐ | |
| 5 | Branches | ☐ | |
| 6 | Merge | ☐ | |
| 7 | GitHub | ☐ | |
| 8 | Collaboration | ☐ | |
| 9 | Merge conflict | ☐ | |
| 10 | Open source simulation | ☐ | |
| 11 | Recover from mistakes | ☐ | |
| 12 | Mini team project | ☐ | |
| — | Bonus challenges attempted | ☐ | which ones: |

## check.py output

Paste the output of `python check.py` run in your `git-practice` repo:

```
  [FAIL]  1. First contact with Git
        13 commit subject(s) not in 'w01: ...

  0 passed, 1 to fix.

  [PASS]  2. The staging area
        main.py committed alone in 73f471c, rest followed, .gitignore present

  1 passed, 0 to fix.

[FAIL]  3. Commit like a professional
        13 message problem(s)
        → 6e3df1c 'Push test' — not 'w01: ...'
      8dd62e8 '7:53 - 31/07/2026' — not 'w01: ...'
      d4e9fe1 'check.py commit' — not 'w01: ...'
      73f471c 'commit of main.py file' — not 'w01: ...'
      fccb0d8 'commit of about.txt file' — not 'w01: ...'

  0 passed, 1 to fix.

[FAIL]  4. Time travel
        the three expected versions are not all in history
        → Found: ['Hello World!!!', 'Hello', 'Hello World!!!']

  0 passed, 1 to fix.

[FAIL]  5. Branches   
        no branch 'feature/about', and no merged branch in history
        → Branches found: Main, student/Aness7/week-01

  0 passed, 1 to fix.

[FAIL]  6. Merge      
        no merge commit in history
        → Switch to main and run: git merge feature/<name>

  0 passed, 1 to fix.

[  - ]  7. GitHub
        origin does not look like the course fork — run this in your fork

  0 passed, 0 to fix.

for the 8th assignment here's the check message:
Traceback (most recent call last):
  File "C:\Users\Aness\Desktop\Github-git_practice\check.py", line 541, in <module>
    sys.exit(main(sys.argv[1:]))
             ^^^^^^^^^^^^^^^^^^
  File "C:\Users\Aness\Desktop\Github-git_practice\check.py", line 496, in main
    if not g.ok("rev-parse", "--git-dir"):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Aness\Desktop\Github-git_practice\check.py", line 54, in ok
    self.run(*args)
  File "C:\Users\Aness\Desktop\Github-git_practice\check.py", line 42, in run
    proc = subprocess.run(
           ^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\subprocess.py", line 548, in run
    with Popen(*popenargs, **kwargs) as process:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\subprocess.py", line 1026, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "C:\Program Files\Python312\Lib\subprocess.py", line 1538, in _execute_child
    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
NotADirectoryError: [WinError 267] The directory name is invalid

```

And run in your fork:

```
[FAIL]  1. First contact with Git
        14 commit subject(s) not in 'w01: ...' form, e.g. 'i wish this work'
  [PASS]  2. The staging area
        main.py committed alone in 73f471c, rest followed, .gitignore present
  [FAIL]  3. Commit like a professional
        14 message problem(s)
        → 77f9b30 'i wish this work' — not 'w01: ...'
      6e3df1c 'Push test' — not 'w01: ...'
      8dd62e8 '7:53 - 31/07/2026' — not 'w01: ...'
      d4e9fe1 'check.py commit' — not 'w01: ...'
      73f471c 'commit of main.py file' — not 'w01: ...'
  [FAIL]  4. Time travel
        the three expected versions are not all in history
        → Found: ['Hello World!!!', 'Hello', 'Hello World!!!']
  [FAIL]  5. Branches
        no branch 'feature/about', and no merged branch in history
        → Branches found: Main, student/Aness7/week-01
  [FAIL]  6. Merge
        no merge commit in history
        → Switch to main and run: git merge feature/<name>
  [  - ]  7. GitHub
        origin does not look like the course fork — run this in your fork
  [FAIL]  8. Collaboration
        0 merge commit(s) on main, need 2
        → Two feature branches, each merged in — yours and your partner's.
  [FAIL]  9. Merge conflict
        no merge where both sides changed the same file
        → Assignment 9 needs a genuine conflict — same line, two branches.
  [  ~ ] 10. Open source simulation
        reviewed on your Pull Request (maintainer requests changes, you push a fix)
  [FAIL] 11. Recover from mistakes
        no revert commit in history
        → git revert <sha> — the only recovery tool that leaves a trace, which is why it is the safe one on a shared branch.
  [  ~ ] 12. Mini team project
        team repository — graded from its PR history, not from this repo

  1 passed, 8 to fix.
```

> If something reports FAIL and you could not fix it, leave it — say what you tried
> below. An honest FAIL with a real attempt is worth more than a green board you did
> not earn.

## Reflection

Short answers. Two or three sentences each — these carry real weight in the grade,
because they are where understanding shows.

**1. `git add` does not save your work. So what does it do, and why does Git make you
do it at all?**

>It's like preparing my work to get commited

**2. You committed something, but your teammate cannot see it. List every reason this
could happen.**

>I didn't push it to github repo.
>My teammate didn't pull my commit from the repo.

**3. In assignment 9 you resolved a conflict. Why could Git not resolve it for you —
what exactly did it not know?**

>it didn't solve it because i should decide which merge i should keep in main

**4. `git revert` and `git reset` both undo things. When would you reach for each, and
which one is safe on a branch other people have pulled?**

>

**5. Which single assignment changed how you think about Git the most, and what did
you believe before it?**

>

## Anything you got stuck on

>
