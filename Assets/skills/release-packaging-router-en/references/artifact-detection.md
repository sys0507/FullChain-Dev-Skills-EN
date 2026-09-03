# Artifact shape detection

## When to read this

Before routing. **Know what the project produces before discussing where it goes.**

## Signal table

Each row states which file and which field to read — **no impressions, no guessing from the
project name**.

| Channel | Signal | Where to read it |
|---|---|---|
| **Container** | A `Dockerfile` is present | Project root |
| | `docker-compose.yml` or `compose.yaml` is present | Project root |
| **Package registry** | `package.json` has `main`, `exports` or `bin` | That file's fields |
| | `pyproject.toml` has `[project]` or `[project.scripts]` | That file's sections |
| | `Cargo.toml` is present | Project root |
| **App store** | `*.podspec` or `*.xcodeproj` is present | Project root glob |
| | `AndroidManifest.xml` is present | Project root |
| **Firmware** | `*.ino` or `platformio.ini` is present | Project root |
| **Hosting platform** | `vercel.json`, `netlify.toml`, `fly.toml` or `Procfile` | Project root |
| **Installer** | No automatic signal — **the user says so** | - |
| **Private registry** | No automatic signal — **the user says so** | - |

**The last two rows are not an omission.** No field in any manifest can express "produce an
.msi and install it on machines inside the corporate network". Inventing a detection rule for
it would only produce false positives.

## Three disciplines

### 1. An unclear shape is marked unknown, never guessed

`go.mod` exists but there is no main package — this project might be a library, or it might
simply be unfinished. **Mark the shape unknown and ask the user.**

The cost of guessing wrong: an incorrect release channel travels all the way to tasks, and by
the time anyone notices, the packaging feature is already written.

### 2. A conflict is reported, never chosen

Hitting a mutually exclusive group (container + app store, container + firmware, app store +
firmware) means **reporting the conflict and asking the user to clarify**.

The cost of the script choosing: an unexamined judgement is emitted as an objective
conclusion, and because it came from a tool, nobody questions it.

### 3. Several artifacts are not merged

A project with both a `Dockerfile` and `[project.scripts]` very likely provides a service and
a CLI. **Route two channels and state each one's scope**; do not merge them into "just use the
container, the CLI is in there too".

The cost of merging: the CLI's users get no installable package.

## The fallback: no manifest file

In standalone mode the project may not be initialised yet. **Do not refuse to work** — ask the
user two questions:

1. What does this project produce? (service / library / CLI / mobile app / desktop app /
   firmware)
2. Who consumes it? (public users / colleagues on the internal network / only you)

Label the report "**project manifest not read, shape judgement not cross-checked**".

See `channel-playbooks.md` for what each channel's clarify step must settle.
