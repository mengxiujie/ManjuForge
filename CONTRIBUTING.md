# Contributing to ManjuForge

Thank you for your interest in contributing to ManjuForge! This document provides guidelines for contributing to this project.

## What is ManjuForge?

ManjuForge is an AI-powered skill for Hermes Agent that generates serialized comic (manju) scripts, vertical-format storyboards, voiceover text, and AI image prompts. Its core focus is maintaining consistency in character, plot, and foreshadowing across 30+ episodes.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue using the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md). Include:

- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Hermes version, model used)

### Suggesting Features

Feature requests are welcome! Please open an issue with:

- A clear description of the feature
- Why it would be useful for manju creators
- Any examples or references

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test with at least one episode generation
5. Commit with clear messages (`git commit -m "Add: character relationship graph template"`)
6. Push to your fork (`git push origin feature/your-feature`)
7. Open a Pull Request

### What We're Looking For

- **Template improvements**: Better character dossier, worldbuilding, or plot summary templates
- **Style additions**: New cinematic style templates (e.g., Wes Anderson, Wong Kar-wai)
- **Knowledge base expansion**: Film analysis cases, cinematography references
- **Documentation**: Tutorials, usage examples, integration guides
- **Bug fixes**: Memory leaks, consistency issues, edge cases
- **Translations**: README and docs in other languages

### Code Style

- SKILL.md uses Markdown with clear section headers
- Templates use structured YAML-like frontmatter
- Keep file names descriptive and in English where possible

## Development Setup

```bash
# Clone the repository
git clone https://github.com/mengxiujie/ManjuForge.git

# Install as Hermes skill
cp -r ManjuForge ~/.hermes/skills/creative/manjuforge

# Test in Hermes
# Start Hermes and say: "I want to create a manju series using ManjuForge"
```

## License

ManjuForge is licensed under [MIT-0](LICENSE) (No Attribution Required). By contributing, you agree that your contributions will be licensed under the same license.

## Questions?

Open an issue or reach out to the maintainer. We're here to help!
