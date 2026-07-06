#!/usr/bin/env bash
#
# vibe-setup.sh - Portable installer that wires Superpowers + the Vibe Coding
# Playbook into any repo for use with VS Code Copilot (agent mode).
#
# What it does, without forking anything:
#   1. Clones/updates obra/superpowers into a gitignored .vibe/superpowers
#      (stays upstream-fresh via `git pull`; never copied into your repo).
#   2. Makes the Vibe Coding Playbook's design skills available (local copy when
#      run inside the playbook repo, otherwise a gitignored clone).
#   3. Regenerates .github/skills/ as a disposable layer of symlinks so VS Code
#      Copilot discovers every skill natively.
#   4. Drops an AGENTS.md that tells the agent when to use which system
#      (only if one does not already exist).
#   5. Keeps .vibe/ and the generated symlinks out of git.
#
# Re-run any time to update Superpowers and refresh the skill layer.
#
# Usage:
#   ./tools/vibe-setup.sh            # run from a repo root
#   curl -fsSL <raw-url> | bash      # or pipe into any repo

set -euo pipefail

SUPERPOWERS_REPO="https://github.com/obra/superpowers.git"
PLAYBOOK_REPO="https://github.com/samson-schirmer/vibe-coding-playbook.git"

# Resolve the repo root: prefer git, fall back to current directory.
if REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  :
else
  REPO_ROOT="$(pwd)"
fi
cd "$REPO_ROOT"

VIBE_DIR="$REPO_ROOT/.vibe"
SKILLS_OUT="$REPO_ROOT/.github/skills"

log() { printf '  %s\n' "$*"; }
say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# Clone the repo on first run, otherwise fast-forward it.
sync_repo() {
  local url="$1" dest="$2" name="$3"
  if [ -d "$dest/.git" ]; then
    log "updating ${name}..."
    git -C "$dest" pull --ff-only --quiet || log "  (could not fast-forward ${name}, keeping current)"
  else
    log "cloning ${name}..."
    git clone --depth 1 --quiet "$url" "$dest"
  fi
}

# Symlink every skill folder (a dir containing SKILL.md) from SRC into
# .github/skills, using a repo-relative link. Skips names already linked so the
# first source wins (local > playbook > superpowers).
link_skills() {
  local src="$1" rel_prefix="$2"
  [ -d "$src" ] || return 0
  local dir name
  for dir in "$src"/*/; do
    [ -f "${dir}SKILL.md" ] || continue
    name="$(basename "$dir")"
    if [ -e "$SKILLS_OUT/$name" ] || [ -L "$SKILLS_OUT/$name" ]; then
      continue
    fi
    ln -s "$rel_prefix/$name" "$SKILLS_OUT/$name"
    log "  + $name"
  done
}

# Detect whether we are running inside the playbook home repo itself.
is_playbook_home() {
  [ -f "$REPO_ROOT/skills/vibe-coding-playbook/SKILL.md" ]
}

say "1/4  Syncing Superpowers (upstream-fresh, never forked)"
mkdir -p "$VIBE_DIR"
sync_repo "$SUPERPOWERS_REPO" "$VIBE_DIR/superpowers" "obra/superpowers"

say "2/4  Resolving Vibe Coding Playbook skills"
if is_playbook_home; then
  log "running inside the playbook home - using local skills/"
  PLAYBOOK_SKILLS_REL="../../skills"
  PLAYBOOK_SKILLS_SRC="$REPO_ROOT/skills"
else
  sync_repo "$PLAYBOOK_REPO" "$VIBE_DIR/playbook" "vibe-coding-playbook"
  PLAYBOOK_SKILLS_REL="../../.vibe/playbook/skills"
  PLAYBOOK_SKILLS_SRC="$VIBE_DIR/playbook/skills"
fi

say "3/4  Regenerating .github/skills discovery layer"
mkdir -p "$SKILLS_OUT"
# Clear only managed symlinks; leave any hand-authored real skill folders intact.
find "$SKILLS_OUT" -maxdepth 1 -type l -exec rm {} +

# Precedence: this repo's own skills, then playbook design skills, then
# Superpowers process skills.
if ! is_playbook_home && [ -d "$REPO_ROOT/skills" ]; then
  link_skills "$REPO_ROOT/skills" "../../skills"
fi
link_skills "$PLAYBOOK_SKILLS_SRC" "$PLAYBOOK_SKILLS_REL"
link_skills "$VIBE_DIR/superpowers/skills" "../../.vibe/superpowers/skills"

say "4/4  Wiring AGENTS.md and .gitignore"
if [ -f "$REPO_ROOT/AGENTS.md" ]; then
  log "AGENTS.md already exists - leaving it untouched"
else
  log "no AGENTS.md found - run inside the playbook repo to get the canonical one,"
  log "or copy .vibe/playbook/AGENTS.md into this repo"
  if [ -f "$VIBE_DIR/playbook/AGENTS.md" ]; then
    cp "$VIBE_DIR/playbook/AGENTS.md" "$REPO_ROOT/AGENTS.md"
    log "copied AGENTS.md from the playbook clone"
  fi
fi

# Keep the machinery out of git.
GITIGNORE="$REPO_ROOT/.gitignore"
touch "$GITIGNORE"
add_ignore() {
  grep -qxF "$1" "$GITIGNORE" 2>/dev/null || printf '%s\n' "$1" >> "$GITIGNORE"
}
add_ignore "# Vibe setup (regenerable - see tools/vibe-setup.sh)"
add_ignore ".vibe/"
add_ignore ".github/skills/"

say "Done."
log "Skills discoverable by VS Code Copilot:"
ls -1 "$SKILLS_OUT" | sed 's/^/    - /'
log ""
log "Update anytime by re-running: ./tools/vibe-setup.sh"
