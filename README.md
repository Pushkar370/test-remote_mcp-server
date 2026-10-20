# Expense Tracker MCP Server

This project contains an MCP server for recording and reviewing expenses, plus a small local STDIO proxy for connecting a remote FastMCP Cloud server to an MCP client such as Claude Desktop.

## Project components

### Expense tracker server (`main.py`)

The server exposes these MCP tools:

| Tool | Purpose |
| --- | --- |
| `add_expense` | Save an expense with a date, amount, category, and optional subcategory and note. |
| `list_expenses` | List expenses between an inclusive start and end date. |
| `summarize` | Return totals and counts grouped by category for an inclusive date range; optionally filter to one category. |

It also exposes the `expense:///categories` resource as JSON. It reads `categories.json` from the project directory when present; otherwise it returns a built-in set of common expense categories.

The database is SQLite, stored as `expenses.db` in the operating system's temporary directory. The server creates the database and `expenses` table on startup.

By default, the server listens on `http://0.0.0.0:8000` using FastMCP's HTTP transport.

### Remote server proxy (`proxy.py`)

The proxy connects to the FastMCP Cloud server configured in `proxy.py` over Streamable HTTP and runs its local side using STDIO. This is a transport bridge: it lets an STDIO-based client such as Claude Desktop use the tools exposed by that remote server without hosting a second copy of the server locally.

The proxy is intended to make capabilities available through the configured FastMCP Cloud server—including connector-related capabilities, when enabled and available to that server/account—usable from a local MCP client. It does not grant Cloud access or bypass any account, server, or connector permissions.

The Cloud URL is currently hard-coded in `proxy.py`. Change it there if you want the proxy to connect to a different remote MCP server.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) for environment and dependency management

`main.py` imports `aiosqlite`, but `aiosqlite` is not currently listed as a direct project dependency. Add it before running the expense tracker server:

```powershell
uv add aiosqlite
```

Then install the project dependencies:

```powershell
uv sync
```

## Run the expense tracker server

Start the HTTP MCP server from the project directory:

```powershell
uv run python main.py
```

The server listens on port `8000`. Keep the process running while an MCP client or other service uses it.

## Connect the remote proxy to Claude Desktop

Claude Desktop can launch the proxy as a local STDIO MCP server. Add an entry like the following to Claude Desktop's `claude_desktop_config.json`, replacing the directory with the absolute path to this project:

```json
{
  "mcpServers": {
    "pushkar-cloud-server": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\test-remote-server",
        "run",
        "python",
        "proxy.py"
      ]
    }
  }
}
```

On Windows, Claude Desktop's configuration file is commonly located at:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

Save the configuration and restart Claude Desktop. The proxy process needs network access to the configured FastMCP Cloud URL. The proxy and the locally hosted expense tracker are separate: configuring this proxy connects to the remote URL in `proxy.py`, not to `main.py`.

## Data and configuration notes

- Expense records are stored locally in the temporary directory, not in `categories.json`.
- `categories.json` is optional and only supplies the category resource; the current tools do not validate expense categories against it.
- The Cloud endpoint used by the proxy is fixed in source code. Keep the URL pointed at a server you are authorized to use.
- The project currently defines no automated test suite.