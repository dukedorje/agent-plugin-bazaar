# Tasks

- [x] `run_pi` installs an rsync runner as `pi_tmux.STAGE_RUNNER` when that global is still `None`, before `run_turn`.
- [x] The runner executes `rsync -a` from `src` to `dest`. It adds `--delete` only when `delete` is `true`. Empty SSH prefix is a local copy. A non-empty prefix is the remote shell, and `dest` is on that host.
- [x] The runner enforces `timeout_sec` itself and returns non-zero on timeout, a missing `src`, or a non-zero rsync. It does not paste and it does not write the prompt file.
- [x] `python3 plugins/intention/scripts/test-pi-tmux.py` covers a zero rsync then paste, a non-zero rsync with no paste, no declaration with no rsync, and `--delete` present only when the entry says `true`. Use a fake `rsync` or a local temp dir. Do not contact the dev VM.
