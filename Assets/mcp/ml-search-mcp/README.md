# ML Search MCP

ML Search MCP is an English-first, bilingual MCP server for Claude Code. It adds web search, page extraction, site mapping, source tracking, and structured research planning.

English is the default interface language. Search requests and answers support both English and Simplified Chinese.

## Capabilities

| Tool | Purpose |
| --- | --- |
| `web_search` | Search the web through a Grok-compatible model and return a sourced answer. |
| `get_sources` | Retrieve the normalized source list for a search session. |
| `web_fetch` | Extract a page as structured Markdown through Tavily, with Firecrawl fallback. |
| `web_map` | Discover URLs and map the structure of a website. |
| `get_config_info` | Inspect masked configuration and test provider connectivity. |
| `switch_model` | Change and persist the default search model. |
| `toggle_builtin_tools` | Enable or disable Claude Code's built-in web tools. |
| `plan_*` | Build and validate a structured research plan before complex searches. |

## Language behavior

Set `ML_OUTPUT_LANGUAGE` to one of these values:

| Value | Behavior |
| --- | --- |
| `auto` | Default. Answer in the same language as the user query. |
| `en` | Always answer in English. |
| `zh` | Always answer in Simplified Chinese. |

Examples:

```text
Search for the latest React Server Components changes and cite the sources.
```

```text
搜索 React Server Components 的最新变化，并列出可追溯的信息来源。
```

The search engine detects both English and Chinese time-sensitive terms. Page extraction preserves the source page's language unless Chinese output is explicitly forced.

## Requirements

- Python 3.10 or newer
- `uv` / `uvx`
- Claude Code CLI
- A supported search-provider API key

Provider support:

- OpenRouter: default and recommended
- xAI: supported directly
- Custom: any compatible OpenAI-style endpoint

Optional extraction services:

- Tavily enables `web_fetch` and `web_map`.
- Firecrawl provides a fallback for `web_fetch`.

## Setup wizard

From the project in which you want to register the MCP:

```powershell
uvx --from 'E:\path\to\ml-search-mcp[setup]' ml-search-setup --package-spec 'E:\path\to\ml-search-mcp'
```

The wizard is English-first and lets you select `auto`, `en`, or `zh` response behavior.

The default registration scope is `local`, because the generated MCP configuration contains API keys. Use `project` only if the configuration is protected from version control.

## Non-interactive setup

```powershell
uvx --from 'E:\path\to\ml-search-mcp[setup]' ml-search-setup `
  --non-interactive `
  --package-spec 'E:\path\to\ml-search-mcp' `
  --scope local `
  --provider openrouter `
  --output-language auto `
  --api-key 'YOUR_OPENROUTER_KEY'
```

Add `--print-only` to inspect the registration command without executing it.

## MCP configuration example

```json
{
  "mcpServers": {
    "ml-search": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "E:\\path\\to\\ml-search-mcp", "ml-search"],
      "env": {
        "ML_PROVIDER": "openrouter",
        "ML_API_KEY": "YOUR_OPENROUTER_KEY",
        "ML_MODEL": "x-ai/grok-4-fast",
        "ML_OUTPUT_LANGUAGE": "auto",
        "TAVILY_API_KEY": "YOUR_TAVILY_KEY"
      }
    }
  }
}
```

Never commit live API keys. Prefer Claude Code's `local` scope or a secret-management mechanism.

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `ML_PROVIDER` | `openrouter` | `openrouter`, `xai`, or `custom` |
| `ML_API_URL` | Provider default | Compatible API base URL |
| `ML_API_KEY` | none | Required search-provider key |
| `ML_MODEL` | `x-ai/grok-4-fast` | Default search model |
| `ML_OUTPUT_LANGUAGE` | `auto` | `auto`, `en`, or `zh` |
| `ML_OPENROUTER_REFERER` | none | Optional OpenRouter HTTP referer |
| `ML_OPENROUTER_TITLE` | `ml-search-mcp` | OpenRouter application title |
| `ML_DEBUG` | `false` | Enable debug logging |
| `ML_LOG_LEVEL` | `INFO` | Log level |
| `ML_LOG_DIR` | `logs` | Log directory |
| `ML_STATE_DIR` | `~/.config/ml-search` | Persistent planning/session state root |
| `TAVILY_API_KEY` | none | Enables Tavily extraction and mapping |
| `FIRECRAWL_API_KEY` | none | Enables Firecrawl extraction fallback |

Runtime state is stored under `~/.config/ml-search/`. The OpenRouter referer is empty by default for private deployments; the title is `ml-search-mcp`.

## Research planning gate

Complex searches can use a six-stage plan:

```text
plan_intent -> plan_complexity -> plan_sub_query -> plan_search_term
            -> plan_tool_mapping -> plan_execution
```

When `web_search` receives a `plan_session_id`, it validates that all required planning phases are complete. One-shot factual searches may leave `plan_session_id` empty.

## Verification

```powershell
claude mcp list
```

Restart Claude Code and run `/mcp`. The server should appear as `ml-search`.

Test both languages:

```text
Use ml-search to find the latest Python 3 release notes and cite sources.

使用 ml-search 搜索最新的 Python 3 发布说明，并列出信息来源。
```

## Private deployment note

This folder is designed as an internal ML-branded fork. Keep it in a private repository and record the authorization and license terms that apply to the source from which it was derived. Repository visibility does not replace source-code licensing or written permission.
