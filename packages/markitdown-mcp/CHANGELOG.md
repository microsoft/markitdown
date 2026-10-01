# Changelog

All notable changes to the markitdown-mcp package will be documented in this file.

## [Unreleased]

### Added
- `convert_and_save()` tool for context-preserving conversion (#1353)
- `convert_to_markdown_with_options()` tool for flexible conversion options
- Support for converting large documents without consuming agent context window
- Automatic directory creation for output files
- Comprehensive error handling and metadata return

### Changed
- Enhanced documentation with detailed tool descriptions and use cases
- Updated README with examples of all three available tools

### Fixed
- Context window exhaustion issue when processing large documents

## [0.0.1a4] - Previous Release
- Initial MCP server implementation with `convert_to_markdown()` tool
