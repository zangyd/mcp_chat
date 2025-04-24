# Memory Bank MCP Server

[![smithery badge](https://smithery.ai/badge/@alioshr/memory-bank-mcp)](https://smithery.ai/server/@alioshr/memory-bank-mcp)
[![npm version](https://badge.fury.io/js/%40allpepper%2Fmemory-bank-mcp.svg)](https://www.npmjs.com/package/@allpepper/memory-bank-mcp)
[![npm downloads](https://img.shields.io/npm/dm/@allpepper/memory-bank-mcp.svg)](https://www.npmjs.com/package/@allpepper/memory-bank-mcp)

<a href="https://glama.ai/mcp/servers/ir18x1tixp"><img width="380" height="200" src="https://glama.ai/mcp/servers/ir18x1tixp/badge" alt="Memory Bank Server MCP server" /></a>

A Model Context Protocol (MCP) server implementation for remote memory bank management, inspired by [Cline Memory Bank](https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md).

## Overview

The Memory Bank MCP Server transforms traditional file-based memory banks into a centralized service that:

- Provides remote access to memory bank files via MCP protocol
- Enables multi-project memory bank management
- Maintains consistent file structure and validation
- Ensures proper isolation between project memory banks

## Features

- **Multi-Project Support**

  - Project-specific directories
  - File structure enforcement
  - Path traversal prevention
  - Project listing capabilities
  - File listing per project

- **Remote Accessibility**

  - Full MCP protocol implementation
  - Type-safe operations
  - Proper error handling
  - Security through project isolation

- **Core Operations**
  - Read/write/update memory bank files
  - List available projects
  - List files within projects
  - Project existence validation
  - Safe read-only operations

## Installation

### Installation

To install Memory Bank Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@alioshr/memory-bank-mcp):

```bash
npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude
```

This will set up the MCP server configuration automatically. Alternatively, you can configure the server manually as described in the Configuration section below.

## Quick Start

1. Configure the MCP server in your settings (see Configuration section below)
2. Start using the memory bank tools in your AI assistant

## Configuration

The memory bank MCP server needs to be configured in your Cline MCP settings file. The location depends on your setup:

- For Cline extension: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- For Claude desktop app: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the following configuration to your MCP settings:

```json
{
  "allpepper-memory-bank": {
    "command": "npx",
    "args": ["-y", "@allpepper/memory-bank-mcp"],
    "env": {
      "MEMORY_BANK_ROOT": "<path-to-bank>"
    },
    "disabled": false,
    "autoApprove": [
      "memory_bank_read",
      "memory_bank_write",
      "memory_bank_update",
      "list_projects",
      "list_project_files"
    ]
  }
}
```

### Configuration Details

- `MEMORY_BANK_ROOT`: Directory where project memory banks will be stored (e.g., `/path/to/memory-bank`)
- `disabled`: Set to `false` to enable the server
- `autoApprove`: List of operations that don't require explicit user approval:
  - `memory_bank_read`: Read memory bank files
  - `memory_bank_write`: Create new memory bank files
  - `memory_bank_update`: Update existing memory bank files
  - `list_projects`: List available projects
  - `list_project_files`: List files within a project

## For Cursor

For Cursor, open the settings -> features -> add MCP server -> add the following:

```
env MEMORY_BANK_ROOT=<path-to-bank> npx -y @allpepper/memory-bank-mcp@latest
```

## Custom IA instructions

This section contains the instructions that should be pasted on the AI custom instructions, either for Cline, Claude or Cursor, or any other MCP client. You should copy and paste these rules. For reference, see [custom-instructions.md](custom-instructions.md) which contains these rules.

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Test
npm run test

# Watch mode
npm run dev
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Use TypeScript for all new code
- Maintain type safety across the codebase
- Add tests for new features
- Update documentation as needed
- Follow existing code style and patterns

### Testing

- Write unit tests for new features
- Include multi-project scenario tests
- Test error cases thoroughly
- Validate type constraints
- Mock filesystem operations appropriately

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project implements the memory bank concept originally documented in the [Cline Memory Bank](https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md), extending it with remote capabilities and multi-project support.
