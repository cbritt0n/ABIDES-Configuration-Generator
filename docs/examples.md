# Usage Examples

## Quick Start Examples

### Basic Market Simulation
# ABIDES Configuration Generator v1.0.0 - Usage Examples

## Research Templates

### RMSC03 Academic Template
```bash
# Generate standard RMSC03 configuration (JPMorgan research paper)
python configgen.py --template rmsc03 -f rmsc03_study --symbol AAPL

# Custom RMSC03 with different parameters
python configgen.py --template rmsc03 -f custom_rmsc03 \
  --symbol MSFT --date 2019-06-28 --mm 8 --zi 150 --verbose
```

### RMSC04 Enhanced Template  
```bash
# Generate RMSC04 configuration with momentum agents
python configgen.py --template rmsc04 -f rmsc04_study --symbol GOOGL

# RMSC04 with adaptive market makers
python configgen.py --template rmsc04 -f adaptive_study \
  --symbol AAPL --am 5 --mm 10 --zi 200
```

### High-Frequency Trading (HFT) Template
```bash
# HFT-focused simulation with fast agents
python configgen.py --template hft -f hft_study --symbol AAPL

# Custom HFT with momentum strategies
python configgen.py --template hft -f momentum_hft \
  --symbol TSLA --mo 15 --mm 5 --zi 100
```

### Behavioral Finance Template
```bash
# Behavioral agents with psychological biases
python configgen.py --template behavioral -f behavioral_study --symbol AAPL

# Mixed behavioral and rational agents
python configgen.py --template behavioral -f mixed_behavior \
  --symbol AMZN --va 25 --no 50 --zi 150
```

### Minimal Template (ABIDES-Gym Compatible)
```bash
# Minimal setup for reinforcement learning
python configgen.py --template minimal -f rl_env --gym-mode --symbol AAPL

# Gym-compatible with custom agents
python configgen.py --template minimal -f gym_custom \
  --gym-mode --mm 3 --zi 50 --symbol SPY
```

## Agent Types (6 Types Available)

### Individual Agent Commands
```bash
# Market Maker agents (--mm)
python configgen.py -f mm_study --mm 10 --zi 100

# Adaptive Market Maker agents (--am) - New!
python configgen.py -f adaptive_study --am 5 --mm 5 --zi 100

# Momentum agents (--mo) - New!  
python configgen.py -f momentum_study --mo 8 --zi 150

# Zero Intelligence agents (--zi)
python configgen.py -f zi_study --zi 200

# Noise agents (--no)
python configgen.py -f noise_study --no 50 --zi 100

# Value agents (--va)
python configgen.py -f value_study --va 20 --zi 100
```

### Multi-Agent Combinations
```bash
# All 6 agent types in one simulation
python configgen.py -f comprehensive_market \
  --mm 5 --am 3 --mo 8 --zi 150 --no 30 --va 15 \
  --symbol AAPL --verbose

# Research-grade multi-agent setup
python configgen.py -f research_multi_agent \
  --template rmsc04 --mm 10 --am 5 --mo 12 \
  --zi 200 --no 50 --va 25 --symbol AAPL
```

## ABIDES-Gym Integration

### Gym-Compatible Configurations
```bash
# Basic gym environment
python configgen.py --gym-mode -f gym_basic --mm 3 --zi 50

# Complex gym environment with templates
python configgen.py --template minimal --gym-mode -f gym_complex \
  --mm 5 --am 3 --zi 100 --symbol AAPL

# Gym environment for training
python configgen.py --gym-mode -f training_env \
  --mm 2 --mo 5 --zi 75 --episodes 1000
```

## Advanced Features

### Agent Scaling
```bash
# Scale all agents by factor (2x, 3x, etc.)
python configgen.py -f scaled_2x --mm 5 --zi 100 --scale-factor 2

# Large-scale simulation
python configgen.py -f large_market --mm 20 --zi 500 --am 10 \
  --scale-factor 1.5 --symbol AAPL
```

### Output Management
```bash
# Specify output directory
python configgen.py -f organized_sim --mm 5 --zi 100 -o ./configs/

# Quiet mode (minimal output)
python configgen.py -f quiet_sim --mm 5 --zi 100 --quiet

# Verbose mode (detailed output)
python configgen.py -f detailed_sim --mm 5 --zi 100 --verbose
```

### Validation and Testing
```bash
# List all available templates
python configgen.py --list-templates

# Validate configuration without generating
python configgen.py --validate-only -f test --mm 5 --zi 100

# Version information
python configgen.py --version
```

## Configuration Parameters Reference

| Parameter | Description | Example | Default |
|-----------|-------------|---------|---------|
| **Templates** |||
| `--template` | Research template | `--template rmsc03` | none |
| **Agent Types** |||
| `--mm` | Market Maker agents | `--mm 10` | 1 |
| `--am` | Adaptive Market Makers | `--am 5` | 0 |
| `--mo` | Momentum agents | `--mo 8` | 0 |
| `--zi` | Zero Intelligence agents | `--zi 200` | 100 |
| `--no` | Noise agents | `--no 50` | 0 |
| `--va` | Value agents | `--va 25` | 0 |
| **Simulation Config** |||
| `-f` | Output filename | `-f my_sim` | required |
| `--symbol` | Trading symbol | `--symbol AAPL` | JPM |
| `--date` | Market date | `--date 2019-06-28` | 2019-06-28 |
| `--seed` | Random seed | `--seed 12345` | auto |
| **Special Modes** |||
| `--gym-mode` | ABIDES-Gym compatible | `--gym-mode` | false |
| `--scale-factor` | Agent scaling | `--scale-factor 2.0` | 1.0 |
| **Output Control** |||
| `-o` | Output directory | `-o ./configs/` | current |
| `--verbose` | Detailed output | `--verbose` | false |
| `--quiet` | Minimal output | `--quiet` | false |

## Generated File Structure

```python
#!/usr/bin/env python3
"""
ABIDES Configuration: [Template Name]
Generated by ABIDES Configuration Generator v2.0.0

Agent Composition:
- Market Makers: X
- Adaptive MMs: Y  
- Momentum: Z
- Zero Intelligence: W
- Noise: V
- Value: U
Total Agents: N
"""

import argparse
import numpy as np
import pandas as pd
from datetime import datetime
from abides_core import abides
from abides_core.utils import parse_logs_df, ns_date, str_to_ns
from abides_markets.configs.rmsc04 import build_config

# ... Agent definitions and configuration ...
# ... Template-specific parameters ...
# ... ABIDES-Gym integration (if enabled) ...

if __name__ == "__main__":
    config = build_config(
        start_time=mkt_open,
        end_time=mkt_close, 
        agents=agents,
        seed=seed
    )
    
    if gym_mode:
        # Gym-compatible execution
        from abides_gym.envs.markets_daily_investor_environment_v0 import DailyInvestorGym
        # ... gym setup ...
    else:
        # Standard ABIDES execution  
        kernel = abides.markets.configure(config)
        kernel.runner()
```

## Integration with ABIDES Framework

### Standard ABIDES Integration
```bash
# 1. Generate configuration
python configgen.py --template rmsc03 -f market_study --symbol AAPL

# 2. Move to ABIDES directory
cp market_study.py /path/to/abides-markets/

# 3. Run simulation
cd /path/to/abides-markets/
python market_study.py
```

### ABIDES-Gym Integration  
```bash
# 1. Generate gym-compatible config
python configgen.py --template minimal --gym-mode -f rl_env --symbol AAPL

# 2. Move to gym directory  
cp rl_env.py /path/to/abides-gym/

# 3. Use in reinforcement learning
python rl_env.py  # or import as module
```

## Best Practices

### Research Templates
- **RMSC03/04**: Academic studies, replication research
- **HFT**: High-frequency trading analysis, latency studies  
- **Behavioral**: Psychological bias studies, sentiment analysis
- **Minimal**: Baseline comparisons, RL environments

### Agent Composition Guidelines
- **Market Makers (--mm)**: 1-20 (liquidity providers)
- **Adaptive MMs (--am)**: 0-10 (dynamic liquidity, new!)
- **Momentum (--mo)**: 0-20 (trend followers, new!)
- **Zero Intelligence (--zi)**: 50-500 (base volume)
- **Noise (--no)**: 10-100 (random activity)
- **Value (--va)**: 10-50 (informed traders)

### Performance Optimization
- Keep total agents under 1000 for responsive performance
- Use `--scale-factor` for proportional scaling
- Enable `--gym-mode` for RL training efficiency
- Use `--quiet` mode for batch processing

### Research Applications
- **Market Microstructure**: Focus on MM and AM agent interactions
- **Price Discovery**: Include VA agents with information asymmetry
- **Algorithmic Trading**: Test MO and AM agent strategies
- **Market Resilience**: Stress test with NO agents and events
- **Reinforcement Learning**: Use minimal templates with gym-mode

### Research Configuration
```bash
# Complex market for research with multiple agent types
python configgen.py \
  -f research_study \
  -d 2019-06-28 \
  -st 09:30:00 \
  -et 16:00:00 \
  -sc 5000000 \
  -m 10 \
  -z 500 \
  -n 100 \
  -v 50 \
  --symbol AAPL \
  --verbose
```

### GUI Mode
```bash
# Launch the graphical interface
python configgen.py -g
```

## Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-f` | Output filename | `-f my_simulation` |
| `-m` | Market Maker agents | `-m 10` |
| `-z` | Zero Intelligence agents | `-z 500` |
| `-n` | Noise agents | `-n 100` |
| `-v` | Value agents | `-v 50` |
| `-d` | Market date | `-d 2019-06-28` |
| `-st` | Market open time | `-st 09:30:00` |
| `-et` | Market close time | `-et 16:00:00` |
| `-sc` | Starting cash (cents) | `-sc 10000000` |

## Generated File Structure

The generator creates Python files with this structure:

```python
#!/usr/bin/env python3
"""
Generated ABIDES Configuration
"""

# Imports - all necessary ABIDES components
import argparse, numpy as np, pandas as pd
from abides_core.kernel import Kernel
# ... more imports

# Configuration - argument parsing and setup
args, remaining_args = parse_arguments()
seed = 12345  # or auto-generated
# ... configuration setup

# Oracle - market data and timing
historical_date = pd.to_datetime('2019-06-28')
oracle = SparseMeanRevertingOracle(mkt_open, mkt_close, symbols)

# Agents - market participants
agents = [ExchangeAgent(...)]  # Always includes exchange
agents.extend([MarketMakerAgent(...) for j in range(...)])
# ... other agent types

# Execution - simulation kernel and run
kernel = Kernel(...)
kernel.runner(agents=agents, ...)
```

## Integration with ABIDES

1. **Generate Configuration**:
   ```bash
   python configgen.py -f my_sim -m 5 -z 100
   ```

2. **Copy to ABIDES Directory**:
   ```bash
   cp my_sim.py /path/to/abides/
   ```

3. **Run Simulation**:
   ```bash
   cd /path/to/abides
   python my_sim.py -c my_sim -v
   ```

## Best Practices

### Agent Ratios
- **Market Makers**: 1-10 (provides liquidity)
- **Zero Intelligence**: 50-500 (base trading volume)
- **Noise Agents**: 10-100 (random activity)
- **Value Agents**: 10-50 (informed trading)

### Performance Considerations
- Total agents < 1000 for reasonable performance
- Starting cash should reflect realistic market cap
- Longer simulations need more memory

### Research Use Cases
- **Market Microstructure**: Focus on market makers and order flow
- **Price Discovery**: Include value agents with information
- **Market Stress**: Add noise agents and megashock events
- **Algorithm Testing**: Vary agent types and parameters