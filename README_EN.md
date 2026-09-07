# ManjuForge — AI Manju Serial Production Engine

**An Agent Skill for serialized AI manju (comic-drama) creation — works with Hermes Agent, Claude Code, Codex, GitHub Copilot, and any Agent Skills–compatible runtime.**

> Others make a beautiful single episode. We make an IP that survives 30+ episodes.

<p align="center">
  <a href="https://github.com/mengxiujie/ManjuForge">GitHub</a> |
  <a href="./README.md">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-v1.8.0-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT--0-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Agent%20Skill-blue" alt="Platform">
</p>

---

## What is this?

ManjuForge is a **serialization-focused** AI creation engine for manju (漫剧, comic-drama short series popular on Douyin-style vertical platforms). It turns a one-line concept into production-ready deliverables per episode:

**Full script + storyboard (16:9 horizontal / 9:16 vertical AI-execution) + voiceover copy + AI image/video prompts.**

It solves the problem every 30+ episode series hits: **character drift, lost foreshadowing, world-building inconsistency, and relationship confusion.**

### Positioning: visual consistency vs narrative memory

Most 2026 AI short-drama tools solve **visual** consistency (same character/scene across shots). ManjuForge solves **narrative** consistency across episodes:

| | Asset-based workspaces (Jellyfish, ArcReel, ...) | ManjuForge |
|---|---|---|
| What stays consistent | Visual assets: character/scene/prop/costume appearance | **Narrative memory**: personality, relationships, foreshadowing, timeline, world rules |
| Prevents | Shot-to-shot drift | **Cross-episode collapse** (OOC at E30, dropped setups, drifting settings) |
| Timescale | shot → episode | **episode → whole series** (evolving visual motifs, trust curves, relationship stages) |
| Mechanism | asset library + reference images | 7 memory files + 3 engines (Story Bible / Character Graph / Foreshadow Engine) |

They keep the *picture* stable; we keep the *story* stable. Complementary — ManjuForge's prompt output feeds any generation workspace.

## Proven in production

- **Demo 1: 《代码赘婿》6 episodes** — 0 character breaks; 100% foreshadowing closure (11/11); dual mainlines from E4; personal → faction conflict by E6. Third-party rating: A / A+ across six dimensions (Character Memory, Relationship Graph, State Engine, Economic Logic, World Consistency, Narrative Engine).
- **Demo 2: 《渊烬》Unit 1 (E1–5)** — greenfield run (not retrospective): quality curve E1 4 fixes → E2 1 → E3–5 zero; mean 91.1/100 per episode; unit rating 6×A+ / 1×A.

## Core capabilities

- **7 memory files**: character files / worldbuilding / scene layout (with lighting state) / plot summary / foreshadowing ledger / story bible (refreshed every 5 eps) / character relationship graph
- **3 engines**: Story Bible (single source of truth), Character Graph (relationship matrix + event timeline with trust curve), Foreshadow Engine (setup → ferment → advance → payoff lifecycle)
- **18-point automated quality check**: `python scripts/quality_check.py <episode file> [--villain X --foreshadow ... --bible ... --graph ...]` — 🔴 items block advancing to the next episode
- **Knowledge base**: 29 reference files + 13 film-teardown case studies + 6 style templates + hook formula library (6 openings / 4 cliffhangers) + psychological trigger system
- **Vendor-decoupled execution contract (v1.8.0)**: prompts never hard-bind a generator; any image/video production goes through an adapter layer with a 4-step confirmation gate (bounded job → preview → explicit confirm → run), preventing runaway cost. See `references/adapter-contract.md`.

## Install

> The install directory must be lowercase `manjuforge` (Agent Skills spec: SKILL.md `name` must match its parent directory).

**Hermes Agent**
```bash
git clone https://github.com/mengxiujie/ManjuForge.git ~/.hermes/skills/creative/manjuforge
```

**Claude Code**
```bash
git clone https://github.com/mengxiujie/ManjuForge.git && cd ManjuForge
mkdir -p ~/.claude/skills && ln -s "$PWD" ~/.claude/skills/manjuforge
```
Or just tell Claude Code: `install these skills https://github.com/mengxiujie/ManjuForge`

**Codex (OpenAI)**
```bash
git clone https://github.com/mengxiujie/ManjuForge.git && cd ManjuForge
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills" && ln -s "$PWD" "${CODEX_HOME:-$HOME/.codex}/skills/manjuforge"
```

**GitHub Copilot CLI / cross-client**: copy to `~/.copilot/skills/manjuforge`, `.github/skills/manjuforge/` (project), or `~/.agents/skills/manjuforge` (cross-client standard).

**China mirror**: `git clone https://gitcode.com/gcw_LRlig9U4/manjuforge.git <same target>` if GitHub is slow.

## Structure

```
ManjuForge/                        # skill root (dir name = skill name)
├── SKILL.md                       # core definition (frontmatter: name/description/license/metadata)
├── skill.json                     # metadata
├── prompt.core.txt                # core engine rules (open, stable)
├── LICENSE                        # MIT-0
├── scripts/quality_check.py       # 18-point automated checks
├── templates/                     # 6 memory templates
├── references/                    # 29 reference files + knowledge_base/
├── demo/                          # 6-episode complete demo
└── docs/
```

## License

MIT-0 — free for commercial use, no attribution required, closed-source modification allowed.

## Contribute

Star, fork, and open issues welcome: https://github.com/mengxiujie/ManjuForge/issues
