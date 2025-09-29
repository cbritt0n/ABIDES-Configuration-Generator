# ABIDES Configuration Generator

[![Production Ready](https://img.shields.io/badge/Production-Ready-green.svg)](https://github.com/jpmorganchase/abides-jpmc-public)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/jpmorganchase/abides-jpmc-public)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Research Templates](https://img.shields.io/badge/Templates-RMSC03%20%7C%20RMSC04%20%7C%20HFT-purple.svg)](https://github.com/jpmorganchase/abides-jpmc-public)
[![Agent Types](https://img.shields.io/badge/Agents-6%20Types%20Supported-brightgreen.svg)](https://github.com/jpmorganchase/abides-jpmc-public)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](https://opensource.org/licenses/Apache-2.0)

**Configuration generator for ABIDES market simulations** - Generate research-grade configurations with 6+ agent types, standard research templates (RMSC03/RMSC04), ABIDES-Gym compatibility, and enterprise validation.

---

## 🚀 Features

### 🎯 **Research Templates**
- **RMSC03/RMSC04** - Standard academic research configurations
- **HFT** - High-frequency trading environment  
- **Behavioral** - Multi-agent behavioral finance setup
- **Minimal** - Testing and debugging configurations

### 🤖 **Agent Support (6 Types)**
- **Market Makers** - Traditional liquidity providers
- **Adaptive Market Makers** - Dynamic spread adjustment ✨ NEW
- **Momentum Agents** - Trend-following behavior ✨ NEW
- **Zero Intelligence** - Random trading agents
- **Noise Agents** - Background market activity  
- **Value Agents** - Fundamental analysis trading

### ⚡ **Advanced Features**
- **Template System** - Instant research configurations
- **Agent Scaling** - Scale configurations by percentage
- **ABIDES-Gym Mode** - RL environment compatibility ✨ NEW
- **Batch Generation** - Parameter sweep capabilities (Coming Soon)
- **Comprehensive Validation** - Business logic and error checking

### 🔧 **Production Quality**
- **Professional CLI** with grouped arguments
- **Cross-platform** compatibility (Windows, macOS, Linux)
- **Enterprise Logging** with multiple levels
- **Comprehensive Documentation** and examples

---

## 🚀 Quick Start

### Installation

```bash
# Clone the ABIDES repository
git clone https://github.com/jpmorganchase/abides-jpmc-public
cd abides-jpmc-public/ABIDES-Configuration-Generator

# Install dependencies (optional - no external dependencies required)
pip install -r requirements.txt
```

### Basic Usage

```bash
# List available research templates
python configgen.py --list-templates

# Generate standard research configuration
python configgen.py --template rmsc03 -f my_research_config

# Custom configuration with new agent types
python configgen.py -f custom_sim -mm 2 -amm 3 -mo 15 -zi 100 -va 25

# Validation without file generation
python configgen.py --validate-only --template rmsc04 --agents-scale 0.1
```

---

## 📖 Usage Guide

### 🎯 Research Templates (Recommended)

```bash
# List available templates
python configgen.py --list-templates

# Get detailed template information
python configgen.py --template-info rmsc03

# Generate standard research configurations
python configgen.py --template rmsc03 -f my_research_config
python configgen.py --template rmsc04 --symbol AAPL -f apple_study

# Scale template configurations
python configgen.py --template behavioral --agents-scale 0.1 -f small_test
```

### 🔧 Custom Agent Configurations

```bash
# Basic market simulation with momentum agents
python configgen.py -f market_sim -mm 5 -zi 100 -na 20 -mo 10

# Advanced multi-agent setup
python configgen.py -f complex_market \\
    -mm 3 -amm 2 -zi 200 -na 50 -va 25 -mo 15 \\
    --symbol JPM --gym-mode

# High-frequency trading environment
python configgen.py -f hft_sim -mm 10 -zi 1000 -na 500
```

### 🤖 ABIDES-Gym Integration

```bash
# Generate RL-compatible configurations
python configgen.py --template minimal --gym-mode -f rl_training_env
python configgen.py -f execution_env -mm 2 -zi 50 --gym-mode
```

### ✅ Validation and Testing

```bash
# Validation only (no file generation)
python configgen.py --validate-only --template rmsc03
python configgen.py --validate-only -f test -mm 5 -mo 10
```

---

## 🔬 Research Templates

### **RMSC03** - Standard Academic Configuration
- **Description**: High-volume research configuration (Academic Standard)
- **Agents**: 2 Adaptive MMs + 100 Value + 25 Momentum + 5,000 Noise
- **Total**: 5,127 agents
- **Usage**: `python configgen.py --template rmsc03 -f my_rmsc03`

### **RMSC04** - Smaller Scale Research
- **Description**: Smaller scale research configuration
- **Agents**: 2 Adaptive MMs + 102 Value + 12 Momentum + 1,000 Noise  
- **Total**: 1,116 agents
- **Usage**: `python configgen.py --template rmsc04 -f my_rmsc04`

### **HFT** - High-Frequency Trading
- **Description**: High-frequency trading environment
- **Agents**: 10 Market Makers + 1,000 Zero Intelligence + 500 Noise
- **Total**: 1,510 agents
- **Usage**: `python configgen.py --template hft -f hft_study`

### **Behavioral** - Multi-Agent Research
- **Description**: Behavioral finance with diverse agent types
- **Agents**: 3 MMs + 2 Adaptive MMs + 50 Value + 75 Momentum + 200 Noise + 100 ZI
- **Total**: 430 agents
- **Usage**: `python configgen.py --template behavioral -f behavior_study`

### **Minimal** - Testing Configuration
- **Description**: Minimal setup for testing and debugging
- **Agents**: 1 Market Maker + 10 Zero Intelligence + 5 Noise
- **Total**: 16 agents
- **Usage**: `python configgen.py --template minimal -f debug_test`

> 💡 **Template Customization**: All templates can be customized with additional arguments:
> ```bash
> python configgen.py --template rmsc03 --symbol AAPL --agents-scale 0.1 -f custom_rmsc03
> ```

---

## 📋 CLI Reference

### 🎯 Template Options
| Argument | Description | Example |
|----------|-------------|---------|
| `-t, --template` | Use research template | `-t rmsc03` |
| `--list-templates` | List available templates | `--list-templates` |
| `--template-info` | Show template details | `--template-info rmsc03` |

### 🤖 Agent Configuration
| Argument | Description | Example |
|----------|-------------|---------|
| `-mm, --market-makers` | Market Maker agents | `-mm 5` |
| `-amm, --adaptive-market-makers` | Adaptive Market Makers ✨ NEW | `-amm 2` |
| `-zi, --zero-intelligence` | Zero Intelligence agents | `-zi 100` |
| `-na, --noise-agents` | Noise agents | `-na 20` |
| `-va, --value-agents` | Value agents | `-va 25` |
| `-mo, --momentum-agents` | Momentum agents ✨ NEW | `-mo 15` |

### 📊 Market Parameters
| Argument | Description | Example |
|----------|-------------|---------|
| `-f, --config-name` | Configuration name | `-f market_sim` |
| `-d, --market-date` | Historical market date | `-d 2019-06-28` |
| `-st, --market-open` | Market opening time | `-st 09:30:00` |
| `-et, --market-close` | Market closing time | `-et 16:00:00` |
| `--symbol` | Primary trading symbol | `--symbol AAPL` |
| `-sc, --starting-cash` | Starting cash per agent (cents) | `-sc 10000000` |
| `-s, --random-seed` | Random seed | `-s 12345` |

### ⚡ Advanced Options
| Argument | Description | Example |
|----------|-------------|---------|
| `--agents-scale` | Scale all agent counts | `--agents-scale 0.1` |
| `--gym-mode` | ABIDES-Gym compatibility ✨ NEW | `--gym-mode` |
| `--batch-mode` | Batch generation (dev) | `--batch-mode` |
| `--validate-only` | Validate without generating | `--validate-only` |
| `--verbose` | Enable verbose logging | `--verbose` |
| `-o, --output-dir` | Output directory | `-o ./configs` |

---

## 🎯 Generated Configuration Structure

The generator creates comprehensive ABIDES configuration files with:

```python
#!/usr/bin/env python3
"""
ABIDES Configuration File
Generated by ABIDES Configuration Generator v2.0.0
"""

# Professional imports for all ABIDES components
import argparse, numpy as np, pandas as pd
from abides_core.kernel import Kernel
from abides_core.utils import util, str_to_ns
from abides_markets.oracles.SparseMeanRevertingOracle import SparseMeanRevertingOracle
from abides_markets.agents.ExchangeAgent import ExchangeAgent
from abides_markets.agents.market_makers.MarketMakerAgent import MarketMakerAgent
from abides_markets.agents.examples.momentum_agent import MomentumAgent
# ... all agent imports

# Configuration parameters with validation
seed = 12345
starting_cash = 10000000  # $100,000 per agent

# Market setup with realistic oracle
historical_date = pd.to_datetime('2019-06-28')
symbol = 'JPM'
mkt_open = historical_date + pd.to_timedelta('09:30:00')
mkt_close = historical_date + pd.to_timedelta('16:00:00')

# Oracle with mean-reverting dynamics
oracle = SparseMeanRevertingOracle(mkt_open, mkt_close, symbols)

# Professional agent initialization
agents = [ExchangeAgent(...)]  # Always included
agents.extend([MomentumAgent(...) for j in range(...)])  # NEW
agents.extend([AdaptiveMarketMakerAgent(...) for j in range(...)])  # NEW
# ... other agent types with proper random state management

# Kernel setup with latency modeling and execution
kernel = Kernel(...)
kernel.runner(agents=agents, startTime=mkt_open, stopTime=mkt_close, ...)
```

### 🤖 ABIDES-Gym Compatibility

When `--gym-mode` is used, additional exports are generated:

```python
# ABIDES-Gym Integration
def create_background_config():
    """Create background configuration for ABIDES-Gym."""
    return {
        'start_time': kernel_start_time,
        'stop_time': kernel_stop_time,
        'agents': agents[1:],  # Exclude exchange agent (handled by Gym)
        'agent_latency_model': latency_model,
        'default_computation_delay': default_computation_delay,
        'oracle': oracle,
        'stdout_log_level': 'INFO'
    }

background_config = create_background_config()
```

---

## 🧪 Testing & Validation

### Basic Validation
```bash
# Test configuration generation
python configgen.py --template minimal -f test_config --validate-only

# Generate and validate syntax
python configgen.py -f test_sim -mm 1 -zi 10
python -m py_compile test_sim.py
```

### Integration Testing
```bash
# Test with ABIDES (requires ABIDES installation)
cd /path/to/abides
python test_sim.py -c test_sim -v

# Test ABIDES-Gym compatibility
python -c "
import sys; sys.path.append('.')
from test_sim import background_config
print('Gym config keys:', list(background_config.keys()))
"
```

---

## 🏗️ Architecture

```
ABIDES-Configuration-Generator/
├── configgen.py                    # Main application (1,169 lines)
├── README.md                       # This documentation
├── requirements.txt                # Dependencies (minimal)
├── examples/                       # Example implementations
│   ├── all_agents_test.py         # Generated: All 6 agent types
│   ├── gym_test.py                # Generated: Gym compatibility
│   └── comprehensive_test.py      # Generated: Template example
├── docs/                          # Additional documentation
│   ├── examples.md                # Usage examples
│   └── project_structure.md       # Architecture details
├── EXTENSION_RECOMMENDATIONS.md   # Development roadmap
├── IMPLEMENTATION_ROADMAP.md      # Implementation guide
├── IMPLEMENTATION_COMPLETE.md     # Feature completion summary
├── Dockerfile                     # Container configuration
├── docker-compose.yml             # Multi-service setup
└── pyproject.toml                 # Modern Python packaging
```

---

## 📈 Performance & Scalability

### Agent Count Recommendations
- **Development/Testing**: Use `--agents-scale 0.01` with templates
- **Research Studies**: Use full templates (RMSC03: 5,127 agents)  
- **Production/HFT**: Custom configurations with optimized agent ratios

### Memory Usage Estimates
- **Minimal (16 agents)**: ~50MB
- **RMSC04 (1,116 agents)**: ~2GB
- **RMSC03 (5,127 agents)**: ~8GB

### Performance Warnings
The generator automatically warns about:
- Large agent counts that may impact performance
- Very small scaling factors that may result in zero agents
- Unusual market hours outside typical trading times

---

## 🔄 Migration from v1.0

If upgrading from the original version:

```bash
# Old v1.0 syntax
python configgen.py -f sim -m 5 -z 100 -n 20 -v 10

# New v2.0 equivalent with templates
python configgen.py --template behavioral --agents-scale 0.3 -f sim

# New v2.0 with custom agents
python configgen.py -f sim -mm 5 -zi 100 -na 20 -va 10 -mo 5
```

**New capabilities not available in v1.0:**
- Research templates (RMSC03/RMSC04)
- Momentum and Adaptive Market Maker agents
- ABIDES-Gym compatibility mode
- Agent scaling and comprehensive validation

---

## 🤝 Contributing

1. Fork the [ABIDES repository](https://github.com/jpmorganchase/abides-jpmc-public)
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Test your changes with multiple templates and agent configurations
4. Ensure all generated configurations compile successfully
5. Submit a Pull Request with example configurations

### Development Guidelines
- Maintain backward compatibility with existing configurations
- Add comprehensive validation for new features
- Include template examples for new functionality
- Update documentation and help text

---

## 📄 License

This project is part of the [ABIDES framework](https://github.com/jpmorganchase/abides-jpmc-public) and is licensed under the Apache 2.0 License.

---

## 🙏 Acknowledgments

- **JPMorgan Chase ABIDES Team** - For the excellent simulation framework
- **Academic Research Community** - For RMSC03/RMSC04 standard configurations  
- **ABIDES-Gym Contributors** - For reinforcement learning integration
- **Python Community** - For amazing tools and libraries

---

## 📞 Support

- 📚 **ABIDES Documentation**: [GitHub Repository](https://github.com/jpmorganchase/abides-jpmc-public)
- 🐛 **Issue Tracker**: [Report Bugs](https://github.com/jpmorganchase/abides-jpmc-public/issues)
- 💬 **Discussions**: [Community Forum](https://github.com/jpmorganchase/abides-jpmc-public/discussions)
- 📖 **Research Papers**: [ABIDES Publications](https://arxiv.org/search/?query=ABIDES&searchtype=all)

### Quick Help
```bash
# Get help anytime
python configgen.py --help
python configgen.py --list-templates
python configgen.py --template-info <template_name>
```

---

**Built with ❤️ for the ABIDES research community**

*ABIDES Configuration Generator v1.0.0 - Production Release - The definitive tool for ABIDES market simulation configuration*