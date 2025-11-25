# 🔬 prompt-lab

Lasya and I have been reading about the [energy footprint](https://www.technologyreview.com/2025/05/20/1116327/ai-energy-usage-climate-footprint-big-tech/) that booming AI technologies are using. The purpose of this project is threefold:

- Familiarize ourselves with >=3 open-source AI/LLM SDKs
- Explore, learn, and implement at >=3 NLP techniques
- Understand the magnitude of today's growing energy demands, and brainstorm ways to reduce energy consumption - if this is viable

Additionally, the project should do the following:

- Architect complex code within a clean, easy-to-navigate project tree
- Provide unit tests for functions
- Use robust branching strategies to avoid collaboration conflicts
- Set up a dedicated project environment
- Conventional commits
- Auto-magically generated documentation

### 📆 24-Nov-2025

Initial setup is loosely [following this guide](https://docs.python-guide.org/writing/structure/) on project structure. This seems outdated to me, since they're choosing to use `setup.py` and `requirements.txt` rather than `pyproject.toml`.

I am not sure about a few things here:

- How should the tests directory be structured? Should there be a folder `tests/optimizers` folder to mimic our main package, and then a `test_*filename*` for each file within our `optimizers` package? Is there a standard testing library that is preferred?
- How is a license generated, and what data is stored here?
- What is `conf.py` in the `./docs` dir?
- We are including an `index.rst` in `./docs`, so how is this ReStructured Text file rendered?
- Right now, all of these files are blank, so how do I configure environment setup?
- What is the correct structure within a package, do I need a `/config` directory, `/src`, etc?
- Versioning, with git tags, or manually
- How do I integrate, or possibly enforce, conventional commits?
- Linting?
- Secure secret or API Key storage ??
- Could be extensions on VSCode that ease / speed up development:
  - python syntax highlighter
  - gitlens
- Set up terminal and command prompt for development:
  - oh-my-zsh

What do I know:

- In a markdown (MD) file, text in two tick marks \`\` creates an in-line code block
- In MD, to generate a code block, should have three tick marks \`\`\`. The three-tick grouping should be on their own line. Any text in between will be part of the block. Won't work if the ticks aren't on their own line.
- In MD, More pound signs = smaller heading text
- Having a file `__init__.py` within a directory marks the directory as a package
- Need to find the answers to all of these questions ... `:)`

Other comments:

- Setting up `llm_base.py`, my SDK install will be done via `pip install openai`. But if using other languages, it may look like:
  - javascript: `npm install openai`
  - .NET: `dotnet add package OpenAI`
  - java (Maven dep):
  ```
      <dependency>
          <groupId>com.openai</groupId>
          <artifactId>openai-java</artifactId>
          <version>4.0.0</version>
      </dependency>
  ```

  - Go:
  ```
  import (
      "github.com/openai/openai-go" // imported as openai
  )
  ```

### 📆 26-Nov-2025

#### Packaging

I'm gaining a better understanding of a standard project structure, so moved `src`, `tests`, `requirements.txt`, and `setup.py` into my `optimizers` package directory. I created a `.venv` and activated it to test environment building. FYI there were no requirements listed in `requirements.txt` or `setup.py` so this is an empty case. Used the `-e` build editable flag to successfully install `optimizers-0.1` with the following command:

```
pip install -e .
```

I want to try two more things:

1. build an environment with `conda` and a `Makefile`
2. upgrade from `setup.py` to `pyproject.toml` and build the env with `uv`, `poetry`, or `pixi`

Questions:

- Should I gitignore `*.egg-info` files ????

### 📆 08-May-2026

#### AI Tool Integrations

I downloaded Claude, Copilot, Codex, opencode. These tools are difficult to use outside of an enterprise, licensed environment... because I need to fork up money for the subscriptions! Trying to find a usable, free AI coding assistant. Hit a usage ceiling on copilot. Claude code is not available without a paid subscription. Codex I think is similar to Claude's setup. I decided to try out opencode's build/plan features in terminal instead.

So far opencode is alright, I find that it is pretty bold with making changes. Or maybe I just don't remember configuring other tools ... like claude and copilot ... to 'require explicit human approval' before any changes because it was too long ago. And for this tool I didn't specify that at the beginning.

#### Conventional Commits

Set up a `.pre-commit-config.yaml` file with basic hooks. One new one to me is `commitizen`, which is commit message validation. This is baked into pre-commit so I don't need to include it as a dependency in `dev-requirements.txt`.
