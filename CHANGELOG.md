# Changelog

All notable changes to ManjuForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2026-08-07

### Added

- **4.3 AI提示词模板 → Direct it 范式** in `ai_execution_fields.md` — absorbed from Seedance 2.0 Skill OS (Emily2040/seedance-2.0, MIT, 6.2k★, surveyed 2026-08-07, see `references/competitive_seedance_survey.md`):
  - **语序原则**: subject + one visible action beat opens the prompt (the model locks "who is doing what" first), then camera/light/sound follow, then technical specs.
  - **情绪承载原则**: emotion is carried by one visible action ("the realization lands in the stilled hands, not a word"); adjectives demoted to auxiliary.
  - Template now `[Style anchor], [Subject]+[action beat], [Camera: shot type+movement], [Light: source+quality], [Sound], [Color/mood via action], [Tech specs]` with decorative-vs-direct contrast examples (incl. wuxia-flavored example).

## [1.5.0] - 2026-08-07

### Added

- **《渊烬》实战验证（第一单元 E1-5）** — 用完整 7 文件流程从零跑通一部新剧（改编自同名小说第一卷），非 demo 回顾性迁移:
  - Quality curve: E1 4 fixes → E2 1 fix → E3-5 zero fixes (workflow internalized).
  - Per-episode six-dimension mean **91.1/100**; unit seven-dimension rating **6×A+ / 1×A**.
  - Engines battle-tested: foreshadow table 10 planned / 5 activated, character graph 8 events landed, trust curve 0→15→20.
  - 18 checks caught 4 real defect classes (fragment duration, title coverage, visual hammer, engagement guide).
- **4.4.1 锚点粒度决策（介质锚 vs 情绪锚）** in `ai_execution_fields.md` — from 《渊烬》practice: shows with strongly varying per-episode mood (war field → village → plague city) must use a media-only anchor (no lighting words); fixed lighting anchors would force every scene's mood (covert content injection, second form). Decision rule: single-tone mood curve → emotional anchor; multi-tone → media anchor.

### Changed

- **`quality_check.py` sound-time check → scene-segment granularity**: detection now runs on the script zone only (storyboard sound fields 🎵🔊 excluded) and warns only when day/night keywords coexist within the same `**场景：` segment — cross-scene morning/evening coexistence no longer false-positives (E5 real-world regression).
- **README / skill.json / prompt.core / CHANGELOG → v1.5.0**; README gained a "实战验证（《渊烬》E1-5）" section.

## [1.4.0] - 2026-08-07

### Added

- **Story Bible (v1.0)** — strategic pillar #1, "记不住设定":
  - `references/story_bible.md` — design doc: single source of truth overview (world rules summary / character arc table / visual-motif table / forbidden-changes digest + mainline tracker), refreshed every 5 episodes; visual motif table is the full-series symbol panorama complementing the foreshadow table's per-symbol lifecycle.
  - `templates/story_bible_template.md` + `demo/故事圣经.md` (4 roles, 3 motifs, world+character bans, A/B mainlines migrated from the 6-episode demo).
- **Character Graph (v1.0)** — strategic pillar #2, "记不住关系":
  - `references/character_graph.md` — design doc: relation matrix (current snapshot, symmetric, stage-tagged) + event timeline (change log), trust-curve pacing (E1-6 +10~15/ep, E7+ plateau), no stage skipping.
  - `templates/character_graph_template.md` + `demo/角色关系图.md` (4×4 matrix + 11 events; 沈舟-林霜 0→15→30→45→60→65 trust curve exactly on spec).
- **`quality_check.py` 16 → 18 checks**: "故事圣经健康" (`--bible`: 4-section completeness 🔴, empty motif table 🔴, incomplete motif fields 🟡, empty bans 🟡) and "角色关系图健康" (`--graph`: matrix asymmetry 🔴, trust jump >20 in one episode 🔴, missing timeline/events 🟡).

### Changed

- **SKILL.md**: memory system is now 7 files in two tiers (per-episode: character dossier/plot summary/foreshadow table/scene layout; overview: worldbuilding/story bible/character graph); initialization flow gained steps 6-7; self-check gained 3 items (bible refresh every 5 eps, graph update on relationship episodes, no stage skipping).
- **`prompt.core.txt` synced to v1.4.0**: 7-file memory table with tier split.
- **README / skill.json**: v1.4.0, 18 checks, Story Bible + Character Graph feature sections, 7-file memory claim.
- **All 3 strategic pillars now landed**: Foreshadow Engine (v1.3.0) + Story Bible + Character Graph (v1.4.0) — the 6-month focus is complete at the design-and-landing level.

## [1.3.0] - 2026-08-07

### Added

- **Foreshadow Engine (v1.0)** — the 3rd strategic pillar (Story Bible / Character Graph / Foreshadow Engine) is now formally designed and landed:
  - `references/foreshadow_engine.md` — design doc: foreshadow lifecycle state machine (planted → active → collected / abandoned / suspended), 7 foreshadow types (prop / line / character / event / setting / relationship / **symbol** — the symbol type emerged from demo evidence: the token / desk-tapping / "bug" catchphrase cross-episode evolution), fermentation window (collect ≥2 eps after planting), collection consistency (🔴 upgrade allowed, downgrade banned), density rules (1-2 planted + ≥1 advanced per episode), concurrency caps (S≤3 / A≤5).
  - `templates/foreshadow_template.md` — the 4th memory file template.
  - `demo/伏笔表.md` — all 12 real demo foreshadows migrated to full lifecycle tracking (F001-F012), including an honest fast-collect case (F008, E5→E6) that the checker flags as a 🟡 fermentation-window warning — checker and manual judgment agree.
- **`quality_check.py` 15 → 16 checks**: new "伏笔表健康" check (`--foreshadow <伏笔表.md>`): duplicate IDs 🔴, illegal status 🔴, collected-before-planted 🔴, collected-without-date 🔴, fermentation window <2 eps 🟡, discarded-without-reason 🟡. Verified live against the demo foreshadow table.

### Changed

- **SKILL.md**: memory mechanism is now 4 files (added 伏笔表.md); hard rules extended (foreshadow registration + collection consistency); per-episode workflow Step 4 now includes foreshadow-table sync; self-check checklist gained 3 foreshadow items.
- **`prompt.core.txt` synced to v1.3.0**: 4 memory files + foreshadow hard rules.
- **README / skill.json**: version v1.3.0, 16 checks, Foreshadow Engine feature section, 4-file memory claim.

## [1.2.1] - 2026-08-07

### Added

- **Style anchor pollution prevention** (`references/knowledge_base/ai_execution_fields.md` §4.4): anchors must be medium/grade-only — banned content words (historical/ancient/romance/hanfu/古装/民国/校园 etc.) that would covertly override legitimate content on every panel. Absorbed from DramaClaw (58-episode production pipeline). `quality_check.py` now parses the anchor declaration and flags banned words as 🔴.
- **Reference-image slot binding** (`ai_execution_fields.md` §4.5): Image N slot declaration + in-prompt references, three binding modes (composite / portrait / prompt_only). Absorbed from DramaClaw identity-lock mechanism. `quality_check.py` gained a 15th check (reference-binding 🟡 reminder, non-blocking).
- **Character dossier invariant/variant split** (`templates/character_template.md` rewrite + `demo/角色档案.md` migrated): identity invariants (locked: appearance anchors / personality core / dialogue style) vs state variables (per-episode: emotion / costume / injury / relationship stage) + "forbidden changes" negative checklist. Absorbed from Hell-Grind AIGC Skill (asset-state-matrix / story-bible design). `templates/worldbuilding_template.md` gained a "forbidden changes" section.
- **Competitor surveys archived**: `references/competitive_dramaclaw_survey.md` (open-source AIGC video engine, Elastic 2.0, 5 absorbable points) and `references/competitive_hellgrind_survey.md` (Higgsfield 90-min AI film skill extraction, MIT, 3 absorbable points).

### Changed

- **`scripts/quality_check.py` 14 → 15 checks**: style-anchor content validation (banned-word detection, 🔴) + new reference-binding reminder (🟡). Ad-hoc verified (17 assertions, both rounds green) plus full 6-episode demo pass without regressions.
- **`prompt.core.txt` synced to v1.2.1**: style-anchor pollution rules, reference-image slot guidance, negative-prompt correction (dropped `NO modern elements` content ban), updated self-check table. Fixes the internal/external rule drift first noted in v1.2.0.
- **`references/style_guide.md`**: all six style anchors rewritten medium/grade-only (content words removed).
- **`SKILL.md`**: anchor rules + self-check checklist + 15-check wording updated; memory-mechanism table documents the invariant/variant split.

## [1.2.0] - 2026-07-31

### Added

- **Automatic Quality Check Tool** (`scripts/quality_check.py`): One-command 14-item auto inspection (opening frame / title honesty / style anchor / Character ID / fragment duration / sound-time match / visual hammer / villain lines / follow-up guide / subtitle card / negative prompt / title format / scene marker / time transition). Parses real episode files, outputs 🔴🟡🟢 verdict, exits 1 when 🔴 items exist. Verified against all 6 demo episodes — automatically caught the real issue documented in pitfalls (Ep4-6 fragment duration creeping up to 7.6-7.8s).
- **prompt.core.txt upgraded to v1.2**: Added serial memory mechanism (character dossier / worldbuilding / plot summary constraints injection + summary update template), Hook formula library (6 opening types + 4 ending cliffhangers), psychological rhythm design, style anchor / Character ID / negative prompt rules, unified fragment duration (3-7s average, matching SKILL.md), title spec, subtitle card, ending guide rules, and 8 long-series pacing rules. Fixed the fragment duration contradiction between prompt.core (10-15s) and SKILL.md (3-7s).

### Changed

- **SKILL.md restructured**: 804 lines → 586 lines (-27%). Removed duplicated sections (batch mode ×2, pitfall records ×3, knowledge base index ×2, demo iteration workflow ×2, production workflow overlap ×3). Chapter numbering normalized (一~八, no jumps/duplicates). All pitfall records merged into one 24-item verified pitfall table.
- **References deduplicated**: removed `storyboard-skill.md` (stale anime-storyboard-artist copy, already internalized into knowledge_base/) and `pitfalls_log.md` (content merged into SKILL.md pitfall table). 18 → 16 reference files.
- **Iteration documentation**: added `references/optimization-log-v1.2.md` (reusable refactoring methodology + script development patterns + git merge lessons for future versions) and `references/competitive_shanyin_survey.md` (competitor survey archive: Shanyin Screenwriter 2.0 on SekoAI — closed-source, platform-exclusive, limited reference value). 16 → 18 reference files.

## [1.1.0] - 2026-07-02

### Added

- **Hook Formula Library** (`references/hook_formula_library.md`): 6 opening hook types (Conflict, Suspense, Emotional, Visual Hammer, Question, World-Building) + 4 ending cliffhanger types + platform-specific adaptation guide + practical checklists. Each hook type includes formulas, templates, examples, and high-frequency pitfalls.

- **Psychological Triggers System** (`references/psychological_triggers.md`): Information gap theory, emotional resonance mechanisms, cognitive load management, and addiction loop design for short-form drama retention. Includes per-episode psychological rhythm templates (Ep1-3/4-6/7-10/11-15 with different strategies).

- **Quality Checklist Integration**: Hook type verification and psychological trigger checks now integrated into the per-episode quality self-check workflow.

- **Competitive Analysis Notes** (`references/competitive_analysis_notes.md`): Comparative study against similar AI script generation tools, with actionable improvement directions.

### Changed

- **SKILL.md**: Creation workflow now requires explicit Hook type selection and psychological trigger design before generation.
- **README.md**: Updated to highlight new Hook Formula and Psychological Trigger capabilities.

## [1.0.0] - 2026-06-10

### Added

- **Core Skill (SKILL.md)**: Complete manju generation engine with cross-episode memory mechanism
- **Character Dossier Template**: Locks character design, relationships, and dialogue style across episodes
- **Worldbuilding Template**: Locks era, rules, factions, and spatial geography
- **Plot Summary Template**: Auto-updated log of key events, foreshadowing threads, and timeline
- **Vertical Storyboard System**: 9:16 format with fragmented timeline (3-7 seconds per fragment)
- **Four-Layer Sound Annotation**: Music, Environment, Physiological, and Detail sound layers
- **Quality Self-Check System**: Six-dimensional assessment (Script, Storyboard, Voiceover, AI Prompts, Memory Mechanism, TikTok Adaptation)
- **Style Guide**: 6 cinematic style templates (Inception, Your Name, Attack on Titan, and more)
- **Knowledge Base**: 13 film analysis case studies for reference
- **Vertical Cinematography Dictionary**: Camera angles, transitions, and framing specs for mobile-first content
- **Demo**: Complete 6-episode demo series "The Code Son-in-Law" with full output

### Verified Performance (6-Episode Demo)

| Metric | Result |
|--------|--------|
| Cross-episode Memory | Zero inconsistencies |
| Character Consistency | Main character retains defined traits |
| Foreshadowing Recovery | 100% (11 plot threads recovered/advanced) |
| Relationship Evolution | Progress shown through actions/spatial changes |
| Parallel Mainlines | Second mainline successfully introduced in Ep.4 |
| Faction Conflict Escalation | Escalates from personal to factional conflict |

### Technical Details

- Platform: Hermes Agent
- License: MIT-0 (No Attribution Required)
- Third-party evaluation: A+ across all dimensions
