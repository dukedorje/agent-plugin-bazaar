#!/usr/bin/env bash
# Validate all plugins in the marketplace before publishing.
# Usage: ./validate.sh [plugin-name]
# If no plugin name given, validates all plugins.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

error() { echo -e "${RED}ERROR:${NC} $1"; ((ERRORS++)); }
warn()  { echo -e "${YELLOW}WARN:${NC} $1"; ((WARNINGS++)); }
ok()    { echo -e "${GREEN}OK:${NC} $1"; }

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PLUGINS_DIR="$REPO_ROOT/plugins"
MARKETPLACE="$REPO_ROOT/.claude-plugin/marketplace.json"

# Determine which plugins to validate
if [[ $# -gt 0 ]]; then
    PLUGIN_DIRS=("$PLUGINS_DIR/$1")
    if [[ ! -d "${PLUGIN_DIRS[0]}" ]]; then
        error "Plugin directory not found: ${PLUGIN_DIRS[0]}"
        exit 1
    fi
else
    PLUGIN_DIRS=("$PLUGINS_DIR"/*)
fi

echo "=== Plugin Validation ==="
echo ""

for PLUGIN_DIR in "${PLUGIN_DIRS[@]}"; do
    [[ ! -d "$PLUGIN_DIR" ]] && continue
    PLUGIN_NAME="$(basename "$PLUGIN_DIR")"
    echo "--- $PLUGIN_NAME ---"

    MANIFEST="$PLUGIN_DIR/.claude-plugin/plugin.json"

    # 1. Check manifest exists and is valid JSON
    if [[ ! -f "$MANIFEST" ]]; then
        error "$PLUGIN_NAME: Missing .claude-plugin/plugin.json"
        echo ""
        continue
    fi

    if ! jq empty "$MANIFEST" 2>/dev/null; then
        error "$PLUGIN_NAME: plugin.json is not valid JSON"
        echo ""
        continue
    fi
    ok "plugin.json is valid JSON"

    # 2. Check required fields
    NAME=$(jq -r '.name // empty' "$MANIFEST")
    VERSION=$(jq -r '.version // empty' "$MANIFEST")

    if [[ -z "$NAME" ]]; then
        error "$PLUGIN_NAME: plugin.json missing required 'name' field"
    else
        ok "name: $NAME"
    fi

    if [[ -z "$VERSION" ]]; then
        error "$PLUGIN_NAME: plugin.json missing 'version' field"
    else
        ok "version: $VERSION"
    fi

    # 3. Check for invalid fields
    VALID_FIELDS='["name","version","description","author","homepage","repository","license","keywords","commands","agents","skills","hooks","mcpServers","outputStyles","lspServers"]'
    INVALID=$(jq -r --argjson valid "$VALID_FIELDS" 'keys - $valid | .[]' "$MANIFEST" 2>/dev/null)
    if [[ -n "$INVALID" ]]; then
        for field in $INVALID; do
            warn "$PLUGIN_NAME: Unknown field '$field' in plugin.json"
        done
    fi

    # 4. Check skills directory
    SKILLS_DIR="$PLUGIN_DIR/skills"
    if [[ -d "$SKILLS_DIR" ]]; then
        SKILL_COUNT=0
        for SKILL_DIR in "$SKILLS_DIR"/*/; do
            [[ ! -d "$SKILL_DIR" ]] && continue
            SKILL_MD="$SKILL_DIR/SKILL.md"
            SKILL_NAME="$(basename "$SKILL_DIR")"

            if [[ ! -f "$SKILL_MD" ]]; then
                error "$PLUGIN_NAME: Skill '$SKILL_NAME' missing SKILL.md"
                continue
            fi

            # Check frontmatter exists (starts with ---)
            if ! head -1 "$SKILL_MD" | grep -q '^---'; then
                error "$PLUGIN_NAME: Skill '$SKILL_NAME' SKILL.md missing frontmatter"
                continue
            fi

            # Check required frontmatter fields
            FRONTMATTER=$(awk '/^---$/{n++; next} n==1' "$SKILL_MD")
            if ! echo "$FRONTMATTER" | grep -q '^name:'; then
                error "$PLUGIN_NAME: Skill '$SKILL_NAME' missing 'name' in frontmatter"
            fi
            if ! echo "$FRONTMATTER" | grep -q '^description:'; then
                warn "$PLUGIN_NAME: Skill '$SKILL_NAME' missing 'description' in frontmatter"
            fi

            ((SKILL_COUNT++))
        done
        ok "skills: $SKILL_COUNT found"
    else
        warn "$PLUGIN_NAME: No skills/ directory"
    fi

    # 5. Check agents directory
    AGENTS_DIR="$PLUGIN_DIR/agents"
    if [[ -d "$AGENTS_DIR" ]]; then
        AGENT_COUNT=0
        for AGENT_FILE in "$AGENTS_DIR"/*.md; do
            [[ ! -f "$AGENT_FILE" ]] && continue
            AGENT_NAME="$(basename "$AGENT_FILE" .md)"

            # Check frontmatter
            if ! head -1 "$AGENT_FILE" | grep -q '^---'; then
                error "$PLUGIN_NAME: Agent '$AGENT_NAME' missing frontmatter"
                continue
            fi

            FRONTMATTER=$(awk '/^---$/{n++; next} n==1' "$AGENT_FILE")
            if ! echo "$FRONTMATTER" | grep -q '^name:'; then
                error "$PLUGIN_NAME: Agent '$AGENT_NAME' missing 'name' in frontmatter"
            fi
            if ! echo "$FRONTMATTER" | grep -q '^description:'; then
                warn "$PLUGIN_NAME: Agent '$AGENT_NAME' missing 'description' in frontmatter"
            fi

            ((AGENT_COUNT++))
        done
        ok "agents: $AGENT_COUNT found"
    fi

    # 6. Check marketplace.json version matches plugin.json version
    if [[ -f "$MARKETPLACE" ]] && [[ -n "$VERSION" ]]; then
        MKT_VERSION=$(jq -r --arg name "$NAME" '.plugins[] | select(.name == $name) | .version // empty' "$MARKETPLACE" 2>/dev/null)
        if [[ -z "$MKT_VERSION" ]]; then
            warn "$PLUGIN_NAME: Not listed in marketplace.json"
        elif [[ "$MKT_VERSION" != "$VERSION" ]]; then
            error "$PLUGIN_NAME: Version mismatch — plugin.json=$VERSION, marketplace.json=$MKT_VERSION"
        else
            ok "marketplace.json version matches"
        fi
    fi

    echo ""
done

# Summary
echo "=== Summary ==="
if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}$ERRORS error(s)${NC}, ${YELLOW}$WARNINGS warning(s)${NC}"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo -e "${GREEN}0 errors${NC}, ${YELLOW}$WARNINGS warning(s)${NC}"
    exit 0
else
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
fi
