"""English-first setup wizard for ml-search-mcp.

The installed MCP can answer English and Chinese queries. Use
ML_OUTPUT_LANGUAGE=auto (default), en, or zh to control answer language.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from typing import Optional

try:
    import questionary
    from questionary import Style
except ImportError:  # pragma: no cover
    print(
        "Missing optional dependency 'questionary'. Reinstall with:\n"
        "    pip install 'ml-search-mcp[setup]'\n"
        "or: uvx --from 'ml-search-mcp[setup]' ml-search-setup",
        file=sys.stderr,
    )
    sys.exit(1)


WIZARD_STYLE = Style(
    [
        ("qmark", "fg:#5f87ff bold"),
        ("question", "bold"),
        ("answer", "fg:#00afaf bold"),
        ("pointer", "fg:#5f87ff bold"),
        ("highlighted", "fg:#5f87ff bold"),
        ("selected", "fg:#00afaf"),
        ("instruction", "fg:#808080 italic"),
    ]
)

BANNER = r"""
╭──────────────────────────────────────────────────────────╮
│   ml-search-mcp · Setup Wizard                           │
│   Grok (OpenRouter/xAI) + Tavily + Firecrawl → Claude   │
╰──────────────────────────────────────────────────────────╯
"""

PROVIDER_PRESETS = {
    "openrouter": {
        "label": "OpenRouter (recommended; one key for many models)",
        "api_url": "https://openrouter.ai/api/v1",
        "model": "x-ai/grok-4-fast",
        "key_hint": "Create a key at https://openrouter.ai/settings/keys (normally starts with sk-or-v1-).",
    },
    "xai": {
        "label": "xAI official API (api.x.ai)",
        "api_url": "https://api.x.ai/v1",
        "model": "grok-4-fast",
        "key_hint": "Create a key at https://console.x.ai/ (normally starts with xai-).",
    },
    "custom": {
        "label": "Custom OpenAI-compatible endpoint",
        "api_url": "",
        "model": "grok-4-fast",
        "key_hint": "Enter the key for your compatible API endpoint.",
    },
}


def section(title: str) -> None:
    print(f"\n\033[1;34m▎ {title}\033[0m")


def info(message: str) -> None:
    print(f"  \033[2m{message}\033[0m")


def ok(message: str) -> None:
    print(f"  \033[32m✓\033[0m {message}")


def warn(message: str) -> None:
    print(f"  \033[33m⚠\033[0m {message}")


def err(message: str) -> None:
    print(f"  \033[31m✗\033[0m {message}")


def _cancel() -> None:
    print("\nCancelled.")
    raise SystemExit(130)


def _ask_text(message: str, *, default: str = "", validate=None, secret: bool = False) -> str:
    prompt = questionary.password if secret else questionary.text
    answer = prompt(message, default=default, validate=validate, style=WIZARD_STYLE).ask()
    if answer is None:
        _cancel()
    return answer.strip()


def _ask_select(message: str, choices: list, default=None) -> str:
    answer = questionary.select(message, choices=choices, default=default, style=WIZARD_STYLE).ask()
    if answer is None:
        _cancel()
    return answer


def _ask_confirm(message: str, default: bool = True) -> bool:
    answer = questionary.confirm(message, default=default, style=WIZARD_STYLE).ask()
    if answer is None:
        _cancel()
    return answer


def check_prerequisites() -> None:
    section("Step 1 · Environment check")
    has_claude = shutil.which("claude") is not None
    has_uvx = shutil.which("uvx") is not None
    has_python = sys.version_info >= (3, 10)
    (ok if has_python else err)(f"Python >= 3.10 (current: {sys.version.split()[0]})")
    (ok if has_claude else warn)("Claude Code CLI" + ("" if has_claude else " was not found; registration will be printed"))
    (ok if has_uvx else warn)("uv / uvx" + ("" if has_uvx else " was not found; see https://docs.astral.sh/uv/"))


def step_provider() -> tuple[str, str, str, str]:
    section("Step 2 · Search provider (required)")
    choices = [questionary.Choice(title=cfg["label"], value=name) for name, cfg in PROVIDER_PRESETS.items()]
    provider = _ask_select("Choose a provider:", choices, default=choices[0])
    preset = PROVIDER_PRESETS[provider]
    api_url = _ask_text("OpenAI-compatible base URL:") if provider == "custom" else preset["api_url"]
    if provider != "custom":
        ok(f"base_url = {api_url}")
    info(preset["key_hint"])
    api_key = _ask_text(
        "API key (required; input is hidden):",
        secret=True,
        validate=lambda value: True if value and len(value) >= 8 else "The key is too short.",
    )
    model = _ask_text("Default model:", default=preset["model"])
    return provider, api_url, api_key, model


def step_output_language(default_language: str) -> str:
    section("Step 3 · Response language")
    choices = [
        questionary.Choice("Auto — match the user's English or Chinese query", value="auto"),
        questionary.Choice("English — always answer in English", value="en"),
        questionary.Choice("中文 — 始终使用简体中文回答", value="zh"),
    ]
    default = next((choice for choice in choices if choice.value == default_language), choices[0])
    return _ask_select("Choose response-language behavior:", choices, default=default)


def step_tavily() -> tuple[Optional[str], Optional[str]]:
    section("Step 4 · Tavily (optional: web_fetch and web_map)")
    info("Without Tavily, web_search remains available, but web_fetch/web_map may be hidden.")
    info("Sign up: https://app.tavily.com/home")
    if not _ask_confirm("Configure Tavily now?", default=False):
        warn("Tavily skipped.")
        return None, None
    key = _ask_text("TAVILY_API_KEY:", secret=True, validate=lambda value: True if value else "A key is required.")
    url = _ask_text("TAVILY_API_URL:", default="https://api.tavily.com")
    return key, url


def step_firecrawl() -> Optional[str]:
    section("Step 5 · Firecrawl (optional fetch fallback)")
    info("Sign up: https://www.firecrawl.dev/signin?view=signup")
    if not _ask_confirm("Configure Firecrawl now?", default=False):
        warn("Firecrawl skipped.")
        return None
    return _ask_text("FIRECRAWL_API_KEY:", secret=True, validate=lambda value: True if value else "A key is required.")


def build_env(
    provider: str,
    api_url: str,
    api_key: str,
    model: str,
    tavily_key: Optional[str],
    tavily_url: Optional[str],
    firecrawl_key: Optional[str],
    output_language: str = "auto",
) -> dict[str, str]:
    env = {
        "ML_PROVIDER": provider,
        "ML_API_URL": api_url,
        "ML_API_KEY": api_key,
        "ML_MODEL": model,
        "ML_OUTPUT_LANGUAGE": output_language,
    }
    if tavily_key:
        env["TAVILY_API_KEY"] = tavily_key
        if tavily_url:
            env["TAVILY_API_URL"] = tavily_url
    if firecrawl_key:
        env["FIRECRAWL_API_KEY"] = firecrawl_key
    return env


def build_register_command(env: dict[str, str], package_spec: str, scope: str) -> list[str]:
    payload = {"type": "stdio", "command": "uvx", "args": ["--from", package_spec, "ml-search"], "env": env}
    return ["claude", "mcp", "add-json", "ml-search", "--scope", scope, json.dumps(payload, ensure_ascii=False)]


def step_scope(default_scope: str) -> str:
    section("Step 6 · MCP scope")
    choices = [
        questionary.Choice("local — this project and machine only (recommended for API keys)", value="local"),
        questionary.Choice("user — all projects for this user", value="user"),
        questionary.Choice("project — shared project .mcp.json", value="project"),
    ]
    default = next((choice for choice in choices if choice.value == default_scope), choices[0])
    return _ask_select("Register at which scope?", choices, default=default)


def _mask_env(env: dict[str, str]) -> dict[str, str]:
    return {key: (value[:4] + "***" + value[-4:] if "KEY" in key and len(value) > 8 else value) for key, value in env.items()}


def _shell_quote(value: str) -> str:
    if not value or any(char in value for char in " \t\n'\"\\$`"):
        return "'" + value.replace("'", "'\\''") + "'"
    return value


def register(env: dict[str, str], package_spec: str, scope: str, print_only: bool) -> None:
    section("Step 7 · Review and register")
    print("  MCP configuration (secrets masked):")
    for key, value in _mask_env(env).items():
        print(f"    {key} = {value}")
    if scope == "project":
        warn("Project scope may write API keys to .mcp.json. Never commit secrets.")
    command = build_register_command(env, package_spec, scope)
    display_command = build_register_command(_mask_env(env), package_spec, scope)
    print("\n  Command:")
    print("    " + " ".join(_shell_quote(part) for part in display_command))
    if print_only or shutil.which("claude") is None:
        warn("Command not executed; copy the command above to register manually.")
        return
    if not _ask_confirm("Register now?", default=True):
        warn("Automatic registration skipped.")
        return
    subprocess.run(["claude", "mcp", "remove", "ml-search"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode:
        err("Registration failed:")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)
    ok("Registered. Restart Claude Code and run /mcp to verify ml-search.")


def _resolve_provider_url(provider: str, custom_url: Optional[str]) -> tuple[str, str]:
    preset = PROVIDER_PRESETS.get(provider) or PROVIDER_PRESETS["openrouter"]
    url = custom_url or preset["api_url"]
    if not url:
        raise SystemExit("--api-url is required when --provider=custom.")
    return url, preset["model"]


def run_non_interactive(args: argparse.Namespace) -> None:
    if not args.api_key:
        raise SystemExit("--api-key is required (or set ML_API_KEY).")
    api_url, default_model = _resolve_provider_url(args.provider, args.api_url)
    env = build_env(
        args.provider,
        api_url,
        args.api_key,
        args.model or default_model,
        args.tavily_key,
        "https://api.tavily.com" if args.tavily_key else None,
        args.firecrawl_key,
        args.output_language,
    )
    command = build_register_command(env, args.package_spec, args.scope)
    display_command = build_register_command(_mask_env(env), args.package_spec, args.scope)
    print("==> MCP configuration (secrets masked):")
    for key, value in _mask_env(env).items():
        print(f"      {key} = {value}")
    print(f"==> Scope: {args.scope}")
    if args.print_only:
        print("\n==> Command preview (secrets masked; not executed):")
        print("    " + " ".join(_shell_quote(part) for part in display_command))
        return
    if shutil.which("claude") is None:
        raise SystemExit("Claude CLI was not found. Install it or use --print-only.")
    subprocess.run(["claude", "mcp", "remove", "ml-search"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode:
        print("==> Registration failed:")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)
    print(f"\n==> Registered at scope={args.scope}. Restart Claude Code and run /mcp.")


def main() -> None:
    # Windows may otherwise inherit a legacy code page that cannot print
    # non-ASCII project paths or Chinese labels.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="English-first setup wizard for ml-search-mcp")
    parser.add_argument("--print-only", action="store_true", help="print, but do not run, the Claude registration command")
    parser.add_argument("--package-spec", default=os.getenv("ML_PACKAGE_SPEC", "ml-search-mcp"), help="package/path passed to uvx --from")
    parser.add_argument("--scope", choices=["project", "user", "local"], default=os.getenv("ML_SCOPE", "local"), help="MCP registration scope (default: local)")
    parser.add_argument("--non-interactive", action="store_true", help="read all settings from CLI arguments")
    parser.add_argument("--provider", choices=list(PROVIDER_PRESETS), default="openrouter")
    parser.add_argument("--api-key", default=os.getenv("ML_API_KEY"))
    parser.add_argument("--api-url")
    parser.add_argument("--model")
    parser.add_argument("--output-language", choices=["auto", "en", "zh"], default=os.getenv("ML_OUTPUT_LANGUAGE", "auto"), help="auto matches the query language; en/zh force a language")
    parser.add_argument("--tavily-key", default=os.getenv("TAVILY_API_KEY"))
    parser.add_argument("--firecrawl-key", default=os.getenv("FIRECRAWL_API_KEY"))
    args = parser.parse_args()

    if args.non_interactive:
        run_non_interactive(args)
        return

    print(BANNER)
    check_prerequisites()
    provider, api_url, api_key, model = step_provider()
    output_language = step_output_language(args.output_language)
    tavily_key, tavily_url = step_tavily()
    firecrawl_key = step_firecrawl()
    env = build_env(provider, api_url, api_key, model, tavily_key, tavily_url, firecrawl_key, output_language)
    scope = step_scope(args.scope)
    register(env, args.package_spec, scope, args.print_only)


if __name__ == "__main__":
    main()
