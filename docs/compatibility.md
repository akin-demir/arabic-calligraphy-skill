# Agent compatibility

Official sources checked 2026-11-07: [Agent Skills](https://agentskills.io/specification), [Skills CLI](https://github.com/vercel-labs/skills), [Codex skills](https://developers.openai.com/codex/skills/), [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/docs/skills).

The root skill follows the portable SKILL.md frontmatter format with progressive reference loading. The Skills CLI currently supports selecting Codex, Claude Code and Cursor agents; use `npx skills add . --skill arabic-calligraphy-skill` in a checkout and select your agent, or use `-a codex`, `-a claude-code`, or `-a cursor`. Current CLI documentation requires Node.js 22.20+. Review upstream guidance for host-specific installation paths rather than assuming every agent uses the same directory.

After merge, the intended GitHub source is `npx skills add akin-demir/arabic-calligraphy-skill --skill arabic-calligraphy-skill`. The repository is private: Git authentication is required. Remote Skills CLI installation has not been executed in this environment and discovery is not verified. No skills.sh submission endpoint or listing is claimed. Follow the directory's SKILL.md and install the Python package/native dependencies separately.

A local/custom LLM agent can read SKILL.md and invoke the CLI without any commercial model API. The renderer is independent of model vendor.

ChatGPT and Claude.ai web interfaces have separate skill, tool and file capabilities that vary by product and plan. This repository does not provide a universal import-GitHub button or guarantee shell execution in a web chat. A web interface must expose a compatible runtime or an explicit integration to execute this software. Portable metadata compliance does not prove end-to-end behavior on every host; host execution remains untested here.
