# Changelog

All notable changes to ABIDES Configuration Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-28

### 🎉 **Initial Production Release**

This is the first production-ready release of ABIDES Configuration Generator, representing a complete transformation from experimental utility to enterprise-grade research tool.

### ✨ **Added**
- **Research Templates**: Pre-built RMSC03, RMSC04, HFT, Behavioral, and Minimal configurations
- **New Agent Types**: 
  - Adaptive Market Makers (`-amm, --adaptive-market-makers`)
  - Momentum Agents (`-mo, --momentum-agents`)
- **ABIDES-Gym Integration**: `--gym-mode` flag for RL environment compatibility
- **Professional CLI**: Comprehensive help system, template management, validation
- **Agent Scaling**: `--agents-scale` for proportional template scaling
- **Template System**: 
  - `--list-templates` - List available templates
  - `--template-info <name>` - Show detailed template information
  - `--template <name>` - Generate from research templates
- **Validation System**: `--validate-only` for configuration testing without generation
- **Cross-Platform Support**: Windows PowerShell, macOS bash, Linux bash
- **CI/CD Pipeline**: Full GitHub Actions with matrix testing across Python 3.8-3.12
- **Modern Packaging**: pyproject.toml with SPDX licensing

### 🔧 **Changed**
- **CLI Arguments**: Updated for consistency and clarity
  - `-m` → `-mm, --market-makers`
  - `-z` → `-zi, --zero-intelligence` 
  - `-n` → `-na, --noise-agents`
  - `-v` → `-va, --value-agents` (resolved argparse conflict)
- **Package Structure**: Single-file module with zero external dependencies
- **Error Handling**: Comprehensive validation with actionable error messages
- **Output Format**: Professional configuration files with proper imports and structure

### 🛠️ **Fixed**
- **Argparse Conflicts**: Resolved `-v` flag duplication between value-agents and verbose
- **Windows Compatibility**: UTF-8 encoding support for PowerShell environments
- **Package Building**: TOML syntax errors and setuptools deprecation warnings
- **License Format**: Updated to SPDX format (Apache-2.0) removing deprecated classifiers
- **CI Reliability**: Separate Windows/Unix workflows with proper artifact handling

### 🏗️ **Technical Improvements**
- **Zero Dependencies**: Uses only Python standard library for core functionality
- **Memory Optimization**: Efficient handling of large configurations (5,000+ agents)
- **Cross-Platform Testing**: Automated validation on Windows, macOS, Ubuntu
- **Code Quality**: Comprehensive error handling and input validation
- **Documentation**: Complete user guide with examples and troubleshooting

### 📊 **Templates Added**
- **RMSC03**: Standard high-volume research (5,127 agents)
- **RMSC04**: Balanced research configuration (1,116 agents)  
- **HFT**: High-frequency trading environment (1,510 agents)
- **Behavioral**: Multi-agent behavioral finance (430 agents)
- **Minimal**: Testing and debugging (16 agents)

### 🎯 **Performance**
- **Generation Speed**: <1 second for all standard templates
- **Validation Time**: <500ms for largest configurations
- **Memory Usage**: 50MB (minimal) to 8GB (RMSC03) linear scaling
- **Package Size**: <1MB application footprint

### � **Security**
- **No External Dependencies**: Eliminates third-party security vulnerabilities
- **Offline Operation**: No network access required
- **Deterministic Output**: Reproducible builds with seed control
- **Apache 2.0 License**: Enterprise-friendly open source licensing

---

## [Unreleased]

### 🚀 **Planned Features**
- Batch generation with parameter sweeps
- GUI interface with visual configuration builder
- Additional research templates (Crypto, Options, FX)
- Multi-symbol support
- Cloud deployment configurations
- Performance profiling and optimization recommendations

---

## **Legend**

- ✨ **Added** - New features
- 🔧 **Changed** - Changes in existing functionality  
- 🛠️ **Fixed** - Bug fixes
- 🗑️ **Removed** - Removed features
- 🔐 **Security** - Security improvements
- 📖 **Documentation** - Documentation updates
- 🏗️ **Technical** - Technical improvements
- 📊 **Data** - Data format or template changes
- 🎯 **Performance** - Performance improvements

---

*For detailed information about any release, see the corresponding RELEASE-NOTES.md file.*

*ABIDES Configuration Generator - Built with ❤️ for the ABIDES research community*