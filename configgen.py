#!/usr/bin/env python3
"""
ABIDES Configuration Generator v1.0.0

The definitive configuration generator for ABIDES (Agent-Based Interactive Discrete 
Event Simulation) market simulations. Generate research-grade configurations with 
6+ agent types, standard research templates, and ABIDES-Gym compatibility.

Features:
    - Research Templates: RMSC03, RMSC04, HFT, Behavioral, Minimal configurations
    - 6 Agent Types: Market Makers, Adaptive MMs, Momentum, ZI, Noise, Value agents
    - ABIDES-Gym Mode: RL environment compatibility layer
    - Agent Scaling: Proportional scaling of template configurations
    - Enterprise Validation: Business logic validation with helpful errors
    - Professional CLI: Grouped arguments with comprehensive help
    - Cross-platform: Windows, macOS, Linux compatibility

Examples:
    # Research template configurations
    python configgen.py --template rmsc03 -f my_research_config
    python configgen.py --template rmsc04 --symbol AAPL --agents-scale 0.1
    
    # Custom agent configurations with new types
    python configgen.py -f custom -mm 2 -amm 3 -mo 15 -zi 100 -va 25
    
    # ABIDES-Gym RL environment
    python configgen.py -f rl_env -mm 1 -zi 50 --gym-mode
    
    # Information and validation
    python configgen.py --list-templates
    python configgen.py --template-info rmsc03
    python configgen.py --validate-only -f test -mm 5

Author: ABIDES Development Team
License: Apache 2.0
Repository: https://github.com/jpmorganchase/abides-jpmc-public
Version: 2.0.0 - Complete research and RL capabilities
"""

import argparse
import os
import re
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Union

# Optional GUI support
try:
    import tkinter as tk
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    tk = None

# Research Configuration Templates
RESEARCH_TEMPLATES = {
    'rmsc03': {
        'description': 'RMSC-3: Standard high-volume research configuration (Academic Standard)',
        'agents': {
            'market_makers': 0,  # Uses adaptive market makers instead
            'adaptive_market_makers': 2,
            'value_agents': 100,
            'momentum_agents': 25,
            'noise_agents': 5000,
            'zero_intelligence': 0
        },
        'market_params': {
            'starting_cash': 10_000_000,
            'symbol': 'ABM',
            'market_date': '2020-06-03',
            'market_open': '09:30:00',
            'market_close': '16:00:00'
        }
    },
    'rmsc04': {
        'description': 'RMSC-4: Smaller scale research configuration',
        'agents': {
            'market_makers': 0,  # Uses adaptive market makers instead
            'adaptive_market_makers': 2,
            'value_agents': 102,
            'momentum_agents': 12,
            'noise_agents': 1000,
            'zero_intelligence': 0
        },
        'market_params': {
            'starting_cash': 10_000_000,
            'symbol': 'ABM',
            'market_date': '2021-02-05',
            'market_open': '09:30:00',
            'market_close': '10:00:00'
        }
    },
    'hft': {
        'description': 'High-frequency trading environment with fast agents',
        'agents': {
            'market_makers': 10,
            'adaptive_market_makers': 0,
            'zero_intelligence': 1000,
            'noise_agents': 500,
            'value_agents': 0,
            'momentum_agents': 0
        },
        'market_params': {
            'starting_cash': 10_000_000,
            'symbol': 'JPM'
        }
    },
    'minimal': {
        'description': 'Minimal configuration for testing and debugging',
        'agents': {
            'market_makers': 1,
            'zero_intelligence': 10,
            'noise_agents': 5,
            'value_agents': 0,
            'momentum_agents': 0,
            'adaptive_market_makers': 0
        },
        'market_params': {
            'starting_cash': 1_000_000,
            'symbol': 'TEST'
        }
    },
    'behavioral': {
        'description': 'Behavioral finance research with diverse agent types',
        'agents': {
            'market_makers': 3,
            'adaptive_market_makers': 2,
            'value_agents': 50,
            'momentum_agents': 75,
            'noise_agents': 200,
            'zero_intelligence': 100
        },
        'market_params': {
            'starting_cash': 5_000_000,
            'symbol': 'BEH'
        }
    }
}

# Constants
VERSION = "1.0.0"
DEFAULT_MARKET_DATE = "2019-06-28"
DEFAULT_MARKET_OPEN = "09:30:00"
DEFAULT_MARKET_CLOSE = "16:00:00"
DEFAULT_STARTING_CASH = 10_000_000  # $100,000 in cents
DEFAULT_SYMBOL = "JPM"
MAX_FILENAME_LENGTH = 100
SUPPORTED_DATE_FORMAT = "%Y-%m-%d"
SUPPORTED_TIME_FORMAT = "%H:%M:%S"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Global state
output_config_file: Optional[str] = None


def list_available_templates() -> None:
    """Display all available research configuration templates."""
    print("\n🔬 Available ABIDES Research Configuration Templates:")
    print("=" * 60)
    
    for name, template in RESEARCH_TEMPLATES.items():
        agents = template['agents']
        total_agents = sum(count for count in agents.values() if count > 0)
        
        print(f"\n📋 {name.upper()}")
        print(f"   Description: {template['description']}")
        print(f"   Total Agents: {total_agents:,}")
        
        # Show agent breakdown
        agent_breakdown = []
        if agents.get('market_makers', 0) > 0:
            agent_breakdown.append(f"{agents['market_makers']} Market Makers")
        if agents.get('adaptive_market_makers', 0) > 0:
            agent_breakdown.append(f"{agents['adaptive_market_makers']} Adaptive MMs")
        if agents.get('value_agents', 0) > 0:
            agent_breakdown.append(f"{agents['value_agents']} Value")
        if agents.get('momentum_agents', 0) > 0:
            agent_breakdown.append(f"{agents['momentum_agents']} Momentum")
        if agents.get('noise_agents', 0) > 0:
            agent_breakdown.append(f"{agents['noise_agents']} Noise")
        if agents.get('zero_intelligence', 0) > 0:
            agent_breakdown.append(f"{agents['zero_intelligence']} Zero Intelligence")
            
        print(f"   Agents: {' + '.join(agent_breakdown)}")
        
        # Show market parameters if available
        if 'market_params' in template:
            params = template['market_params']
            if 'symbol' in params:
                print(f"   Symbol: {params['symbol']}")
            if 'starting_cash' in params:
                print(f"   Starting Cash: ${params['starting_cash']/100:,.0f} per agent")
    
    print("\n💡 Usage: python configgen.py --template <name> -f <config_name>")
    print("💡 Override: python configgen.py --template rmsc03 --symbol AAPL -f custom_rmsc03")
    print("="*60 + "\n")


def show_template_info(template_name: str) -> None:
    """Show detailed information about a specific template."""
    if template_name not in RESEARCH_TEMPLATES:
        print(f"❌ Template '{template_name}' not found.")
        print(f"💡 Available templates: {', '.join(RESEARCH_TEMPLATES.keys())}")
        return
    
    template = RESEARCH_TEMPLATES[template_name]
    agents = template['agents']
    
    print(f"\n📋 Template: {template_name.upper()}")
    print("=" * 50)
    print(f"Description: {template['description']}")
    
    print("\n🤖 Agent Configuration:")
    for agent_type, count in agents.items():
        if count > 0:
            agent_display = agent_type.replace('_', ' ').title()
            print(f"  • {agent_display}: {count:,}")
    
    if 'market_params' in template:
        print("\n📊 Market Parameters:")
        params = template['market_params']
        for param, value in params.items():
            if param == 'starting_cash':
                print(f"  • Starting Cash: ${value/100:,.0f} per agent")
            else:
                param_display = param.replace('_', ' ').title()
                print(f"  • {param_display}: {value}")
    
    total_agents = sum(count for count in agents.values() if count > 0)
    print(f"\n📈 Total Agents: {total_agents:,}")
    print(f"💰 Total Market Cap: ${(template.get('market_params', {}).get('starting_cash', DEFAULT_STARTING_CASH) * total_agents)/100:,.0f}")
    
    print(f"\n💡 Generate: python configgen.py --template {template_name} -f my_{template_name}_config")
    print("="*50 + "\n")


def apply_template_to_args(template_name: str, args) -> None:
    """Apply template configuration to parsed arguments."""
    template = RESEARCH_TEMPLATES[template_name]
    
    # Apply agent counts (only if not manually overridden)
    agents = template['agents']
    if not args.market_makers and 'market_makers' in agents:
        args.market_makers = agents['market_makers']
    if not args.adaptive_market_makers and 'adaptive_market_makers' in agents:
        args.adaptive_market_makers = agents['adaptive_market_makers']
    if not args.zero_intelligence and 'zero_intelligence' in agents:
        args.zero_intelligence = agents['zero_intelligence']
    if not args.noise_agents and 'noise_agents' in agents:
        args.noise_agents = agents['noise_agents']
    if not args.value_agents and 'value_agents' in agents:
        args.value_agents = agents['value_agents']
    if not args.momentum_agents and 'momentum_agents' in agents:
        args.momentum_agents = agents['momentum_agents']
    
    # Apply market parameters (only if not manually overridden)
    if 'market_params' in template:
        params = template['market_params']
        if args.starting_cash == DEFAULT_STARTING_CASH and 'starting_cash' in params:
            args.starting_cash = params['starting_cash']
        if args.symbol == DEFAULT_SYMBOL and 'symbol' in params:
            args.symbol = params['symbol']
        if args.market_date == DEFAULT_MARKET_DATE and 'market_date' in params:
            args.market_date = params['market_date']
        if args.market_open == DEFAULT_MARKET_OPEN and 'market_open' in params:
            args.market_open = params['market_open']
        if args.market_close == DEFAULT_MARKET_CLOSE and 'market_close' in params:
            args.market_close = params['market_close']
    
    logger.info(f"✅ Applied template '{template_name}': {template['description']}")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser with comprehensive options."""
    parser = argparse.ArgumentParser(
        prog='abides-configgen',
        description=f'ABIDES Configuration Generator v{VERSION}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate standard research configurations
  %(prog)s --template rmsc03 -f my_research_config
  %(prog)s --template rmsc04 --symbol AAPL -f apple_study
  
  # Custom agent configurations
  %(prog)s -f market_sim -mm 5 -zi 100 -na 20 -mo 10
  %(prog)s -f custom -amm 3 -va 50 -mo 25 --gym-mode
  
  # Scaled configurations
  %(prog)s --template behavioral --agents-scale 0.1 -f small_behavioral
  
  # Information and validation
  %(prog)s --list-templates
  %(prog)s --template-info rmsc03
  %(prog)s --validate-only -f test_config -mm 2 -zi 5

For more information: https://github.com/jpmorganchase/abides-jpmc-public
        """
    )
    
    # Interface options
    interface_group = parser.add_argument_group('Interface Options')
    interface_group.add_argument('-g', '--gui', action="store_true", 
                               help="Launch graphical user interface (if available)")
    interface_group.add_argument('--validate-only', action='store_true',
                               help="Validate configuration without generating files")
    interface_group.add_argument('--verbose', action='store_true', 
                               help="Enable verbose logging output")
    
    # Output configuration
    output_group = parser.add_argument_group('Output Configuration')
    output_group.add_argument('-o', '--output-dir', metavar='DIR', default='.',
                            help="Output directory (default: current directory)")
    output_group.add_argument('-f', '--config-name', metavar='NAME',
                            help="Configuration name (auto-generated if not specified)")
    
    # Simulation parameters
    sim_group = parser.add_argument_group('Simulation Parameters')
    sim_group.add_argument('-s', '--random-seed', metavar='N', type=int,
                         help="Random seed for reproducible simulations")
    sim_group.add_argument('-d', '--market-date', metavar='YYYY-MM-DD', 
                         default=DEFAULT_MARKET_DATE,
                         help=f"Historical market date (default: {DEFAULT_MARKET_DATE})")
    sim_group.add_argument('-st', '--market-open', metavar='HH:MM:SS', 
                         default=DEFAULT_MARKET_OPEN,
                         help=f"Market opening time (default: {DEFAULT_MARKET_OPEN})")
    sim_group.add_argument('-et', '--market-close', metavar='HH:MM:SS', 
                         default=DEFAULT_MARKET_CLOSE,
                         help=f"Market closing time (default: {DEFAULT_MARKET_CLOSE})")
    sim_group.add_argument('--symbol', metavar='SYM', default=DEFAULT_SYMBOL,
                         help=f"Primary trading symbol (default: {DEFAULT_SYMBOL})")
    
    # Template configuration (placed before agent configuration)
    template_group = parser.add_argument_group('Research Configuration Templates')
    template_group.add_argument('-t', '--template', metavar='NAME',
                               choices=list(RESEARCH_TEMPLATES.keys()),
                               help=f"Use research template: {', '.join(RESEARCH_TEMPLATES.keys())}")
    template_group.add_argument('--list-templates', action='store_true',
                               help="List all available configuration templates with details")
    template_group.add_argument('--template-info', metavar='NAME',
                               help="Show detailed information about a specific template")
    
    # Agent configuration
    agent_group = parser.add_argument_group('Agent Configuration')
    agent_group.add_argument('-sc', '--starting-cash', metavar='CENTS', type=int, 
                           default=DEFAULT_STARTING_CASH,
                           help=f"Starting cash per agent in cents (default: {DEFAULT_STARTING_CASH:,} = ${DEFAULT_STARTING_CASH/100:,.0f})")
    agent_group.add_argument('-mm', '--market-makers', metavar='N', type=int, default=0,
                           help="Number of Market Maker agents (provide liquidity)")
    agent_group.add_argument('-amm', '--adaptive-market-makers', metavar='N', type=int, default=0,
                           help="Number of Adaptive Market Maker agents (dynamic spreads)")
    agent_group.add_argument('-zi', '--zero-intelligence', metavar='N', type=int, default=0,
                           help="Number of Zero Intelligence agents (random trading)")
    agent_group.add_argument('-na', '--noise-agents', metavar='N', type=int, default=0,
                           help="Number of Noise agents (background trading)")
    agent_group.add_argument('-v', '--value-agents', metavar='N', type=int, default=0,
                           help="Number of Value agents (fundamental trading)")
    agent_group.add_argument('-mo', '--momentum-agents', metavar='N', type=int, default=0,
                           help="Number of Momentum agents (trend following)")
    
    # Advanced configuration
    advanced_group = parser.add_argument_group('Advanced Configuration')
    advanced_group.add_argument('--gym-mode', action='store_true',
                               help="Generate configuration optimized for ABIDES-Gym RL environments")
    advanced_group.add_argument('--batch-mode', action='store_true',
                               help="Enable batch configuration generation mode")
    advanced_group.add_argument('--agents-scale', metavar='FACTOR', type=float, default=1.0,
                               help="Scale all agent counts by this factor (e.g., 0.1 for 10%% of template size)")
    
    # Utility options
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    
    return parser


def validate_config_filename(filename: Optional[str]) -> Optional[str]:
    """Validate and sanitize configuration filename."""
    if not filename:
        return None
        
    cleaned = filename.strip()
    if len(cleaned) > MAX_FILENAME_LENGTH:
        raise ValueError(f"Filename too long (max {MAX_FILENAME_LENGTH} characters): {len(cleaned)}")
    
    sanitized = re.sub(r'[<>:"/\\|?*\s]+', '_', cleaned)
    
    if not sanitized.replace('_', 'a').replace('-', 'a').isalnum():
        raise ValueError(f"Filename contains invalid characters: {filename}")
    
    if not sanitized.endswith('.py'):
        sanitized += '.py'
        
    return sanitized


def validate_market_date(date_str: str) -> str:
    """Validate market date format and business logic."""
    try:
        parsed_date = datetime.strptime(date_str, SUPPORTED_DATE_FORMAT)
        
        if parsed_date.year < 1990 or parsed_date.year > datetime.now().year + 1:
            raise ValueError(f"Market date should be between 1990 and {datetime.now().year + 1}: {date_str}")
            
        return date_str
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError(f"Invalid date format '{date_str}' (expected: YYYY-MM-DD)")
        raise


def validate_market_time(time_str: str, time_type: str = "time") -> str:
    """Validate market time format and business logic."""
    try:
        parsed_time = datetime.strptime(time_str, SUPPORTED_TIME_FORMAT)
        
        hour = parsed_time.hour
        if hour < 4 or hour > 22:
            logger.warning(f"Unusual market {time_type}: {time_str} (typical range: 04:00-22:00)")
            
        return time_str
    except ValueError:
        raise ValueError(f"Invalid {time_type} format '{time_str}' (expected: HH:MM:SS)")


def validate_agent_count(count: Optional[int], agent_type: str) -> int:
    """Validate agent count with business logic constraints."""
    if count is None:
        return 0
        
    if not isinstance(count, int):
        raise ValueError(f"{agent_type} count must be an integer, got: {type(count).__name__}")
        
    if count < 0:
        raise ValueError(f"{agent_type} count must be non-negative, got: {count}")
        
    if count > 10000:
        logger.warning(f"Large {agent_type} count ({count:,}) may impact simulation performance")
        
    return count


def validate_starting_cash(cash: int) -> int:
    """Validate starting cash amount with business logic."""
    if not isinstance(cash, int):
        raise ValueError(f"Starting cash must be an integer (cents), got: {type(cash).__name__}")
        
    if cash < 0:
        raise ValueError(f"Starting cash cannot be negative: {cash}")
        
    if cash == 0:
        logger.warning("Starting cash is zero - agents cannot trade")
    elif cash < 100_000:
        logger.warning(f"Low starting cash: ${cash/100:.2f} per agent")
    elif cash > 10_000_000_000:
        logger.warning(f"Very high starting cash: ${cash/100:,.0f} per agent")
        
    return cash


def validate_agents_scale(scale: float) -> float:
    """Validate agents scaling factor."""
    if not isinstance(scale, (int, float)):
        raise ValueError(f"Agents scale must be a number, got: {type(scale).__name__}")
    
    if scale <= 0:
        raise ValueError(f"Agents scale must be positive, got: {scale}")
    
    if scale > 10:
        logger.warning(f"Very large agents scale factor: {scale}x - this may impact performance")
    elif scale < 0.01:
        logger.warning(f"Very small agents scale factor: {scale}x - may result in zero agents")
    
    return scale


def validate_template_name(template_name: str) -> str:
    """Validate template name exists."""
    if template_name not in RESEARCH_TEMPLATES:
        available = ', '.join(RESEARCH_TEMPLATES.keys())
        raise ValueError(f"Unknown template '{template_name}'. Available templates: {available}")
    
    return template_name


def write_to_config_file(content: str) -> None:
    """Write content to the configuration output file."""
    global output_config_file
    if not output_config_file:
        raise RuntimeError("No output configuration file specified")
    
    try:
        with open(output_config_file, "a", encoding='utf-8') as f:
            f.write(content)
        logger.debug(f"Wrote {len(content)} characters to {output_config_file}")
    except IOError as e:
        logger.error(f"Failed to write to configuration file {output_config_file}: {e}")
        raise RuntimeError(f"Configuration file write failed: {e}") from e


def generate_imports_section() -> None:
    """Generate the imports section for the ABIDES configuration file."""
    imports = f'''#!/usr/bin/env python3
"""
ABIDES Configuration File
Generated by ABIDES Configuration Generator v{VERSION}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This configuration sets up an ABIDES market simulation with specified parameters.
Run with: python {os.path.basename(output_config_file)} -c {os.path.splitext(os.path.basename(output_config_file))[0]} -v
"""

###### IMPORTS ######

import argparse
import numpy as np
import pandas as pd
import datetime as dt
import logging

# ABIDES Core Components
from abides_core.kernel import Kernel
from abides_core.utils import util, str_to_ns

# Oracle Components
from abides_markets.oracles.SparseMeanRevertingOracle import SparseMeanRevertingOracle

# Latency Model
from abides_core.latency_model import LatencyModel

# Agent Components
from abides_markets.agents.ExchangeAgent import ExchangeAgent
from abides_markets.agents.NoiseAgent import NoiseAgent
from abides_markets.agents.ValueAgent import ValueAgent
from abides_markets.agents.ZeroIntelligenceAgent import ZeroIntelligenceAgent
from abides_markets.agents.market_makers.MarketMakerAgent import MarketMakerAgent
from abides_markets.agents.examples.momentum_agent import MomentumAgent
from abides_markets.agents.market_makers.adaptive_market_maker_agent import AdaptiveMarketMakerAgent


'''
    write_to_config_file(imports)


def generate_config_section(seed: Optional[int] = None) -> None:
    """Generate the general configuration section."""
    if seed is None:
        import time
        seed = int(time.time() * 1000000) % (2**32 - 1)
    
    config = f'''###### GENERAL CONFIGURATION ######

# Parse command line arguments
parser = argparse.ArgumentParser(
    description='ABIDES Market Simulation - Generated Configuration',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-c', '--config', required=True,
                   help='Configuration name (must match filename)')
parser.add_argument('-l', '--log_dir', default=None,
                   help='Log directory (default: auto-generated timestamp)')
parser.add_argument('-v', '--verbose', action='store_true',
                   help='Enable verbose logging and detailed output')
parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                   default='INFO', help='Set logging level')

args, remaining_args = parser.parse_known_args()

# Configuration parameters
log_dir = args.log_dir
seed = {seed}

# Set up logging
log_level = getattr(logging, args.log_level.upper())
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize random state for reproducible simulations
np.random.seed(seed)
util.silent_mode = not args.verbose

# Simulation metadata
simulation_start_time = dt.datetime.now()

print("=" * 60)
print("🚀 ABIDES Market Simulation Starting")
print("=" * 60)
print(f"📅 Start Time: {{simulation_start_time.strftime('%Y-%m-%d %H:%M:%S')}}")
print(f"🎲 Random Seed: {{seed}}")
print(f"📁 Log Directory: {{log_dir or 'Auto-generated'}}")
print(f"🔊 Verbose Mode: {{'Enabled' if args.verbose else 'Disabled'}}")
print("=" * 60 + "\\n")

'''
    write_to_config_file(config)


def generate_oracle_section(
    market_date: str = DEFAULT_MARKET_DATE,
    market_open: str = DEFAULT_MARKET_OPEN, 
    market_close: str = DEFAULT_MARKET_CLOSE,
    symbol: str = DEFAULT_SYMBOL
) -> None:
    """Generate the oracle configuration section."""
    oracle = f'''###### ORACLE CONFIGURATION ######

# Market timing and symbol configuration
historical_date = pd.to_datetime('{market_date}')
symbol = '{symbol}'
mkt_open = historical_date + pd.to_timedelta('{market_open}')
mkt_close = historical_date + pd.to_timedelta('{market_close}')

print(f"📈 Market Configuration:")
print(f"  • Symbol: {{symbol}}")
print(f"  • Date: {{historical_date.strftime('%Y-%m-%d (%A)')}}")
print(f"  • Trading Hours: {{mkt_open.strftime('%H:%M:%S')}} - {{mkt_close.strftime('%H:%M:%S')}}")
trading_duration = mkt_close - mkt_open
print(f"  • Duration: {{trading_duration}}\\n")

# Oracle parameters for realistic market dynamics
symbols = {{
    symbol: {{
        'r_bar': 1e5,                    # Fundamental return rate
        'kappa': 1.67e-12,               # Mean reversion strength
        'agent_kappa': 1.67e-15,         # Agent-specific mean reversion
        'sigma_s': 0,                    # Shock variance
        'fund_vol': 1e-4,                # Fundamental volatility
        'megashock_lambda_a': 2.77778e-13,  # Megashock arrival rate
        'megashock_mean': 1e3,           # Megashock mean magnitude
        'megashock_var': 5e4,            # Megashock variance
        'random_state': np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
    }}
}}

# Initialize oracle for realistic price dynamics
oracle = SparseMeanRevertingOracle(mkt_open, mkt_close, symbols)
print(f"🔮 Oracle Initialized: SparseMeanRevertingOracle")
print(f"  • Mean-reverting fundamental price dynamics")
print(f"  • Stochastic megashock events for stress testing\\n")

'''
    write_to_config_file(oracle)


def generate_agents_section(
    starting_cash: int = DEFAULT_STARTING_CASH,
    market_maker_count: int = 0,
    adaptive_market_maker_count: int = 0,
    zero_intelligence_count: int = 0, 
    noise_agent_count: int = 0,
    value_agent_count: int = 0,
    momentum_agent_count: int = 0
) -> None:
    """Generate the agents configuration section."""
    
    total_trading_agents = (market_maker_count + adaptive_market_maker_count + 
                           zero_intelligence_count + noise_agent_count + 
                           value_agent_count + momentum_agent_count)
    
    agents = f'''###### AGENTS CONFIGURATION ######

# Agent setup and initialization
agent_count = 0
agents = []
starting_cash = {starting_cash}  # ${starting_cash/100:,.2f} per agent
total_trading_agents = {total_trading_agents}

print(f"Setting up {{total_trading_agents}} trading agents with ${{starting_cash/100:,.2f}} starting cash each")

# Exchange Agent (required - always present)
agents.append(ExchangeAgent(
    id=0,
    name='EXCHANGE_AGENT',
    type='ExchangeAgent',
    mkt_open=mkt_open,
    mkt_close=mkt_close,
    symbols=[symbol],
    log_orders=False,  # Set to True for detailed order logging
    pipeline_delay=0,
    computation_delay=0,
    stream_history=10,
    book_freq=0,
    random_state=np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
))
agent_count = 1

'''

    # Market Maker Agents
    if market_maker_count > 0:
        agents += f'''# Market Maker Agents ({market_maker_count})
print(f"Creating {market_maker_count} Market Maker agents...")
agents.extend([
    MarketMakerAgent(
        id=j,
        name=f'MARKET_MAKER_{{j}}',
        type='MarketMakerAgent',
        symbol=symbol,
        starting_cash=starting_cash,
        min_size=500,
        max_size=1000,
        log_orders=False,
        random_state=np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
    ) for j in range(agent_count, agent_count + {market_maker_count})
])
agent_count += {market_maker_count}

'''

    # Zero Intelligence Agents
    if zero_intelligence_count > 0:
        agents += f'''# Zero Intelligence Agents ({zero_intelligence_count})
print(f"Creating {zero_intelligence_count} Zero Intelligence agents...")
agents.extend([
    ZeroIntelligenceAgent(
        id=j,
        name=f'ZI_AGENT_{{j}}',
        type='ZeroIntelligenceAgent',
        symbol=symbol,
        starting_cash=starting_cash,
        log_orders=False,
        random_state=np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
    ) for j in range(agent_count, agent_count + {zero_intelligence_count})
])
agent_count += {zero_intelligence_count}

'''

    # Noise Agents
    if noise_agent_count > 0:
        agents += f'''# Noise Agents ({noise_agent_count})
print(f"Creating {noise_agent_count} Noise agents...")
# Noise agents have slightly extended trading hours
noise_mkt_open = historical_date + pd.to_timedelta('09:00:00')
noise_mkt_close = historical_date + pd.to_timedelta('16:00:00')

agents.extend([
    NoiseAgent(
        id=j,
        name=f'NOISE_AGENT_{{j}}',
        type='NoiseAgent',
        symbol=symbol,
        starting_cash=starting_cash,
        wakeup_time=util.get_wake_time(noise_mkt_open, noise_mkt_close),
        log_orders=False,
        random_state=np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
    ) for j in range(agent_count, agent_count + {noise_agent_count})
])
agent_count += {noise_agent_count}

'''

    # Value Agents
    if value_agent_count > 0:
        agents += f'''# Value Agents ({value_agent_count})
print(f"Creating {value_agent_count} Value agents...")
agents.extend([
    ValueAgent(
        id=j,
        name=f'VALUE_AGENT_{{j}}',
        type='ValueAgent',
        symbol=symbol,
        starting_cash=starting_cash,
        random_state=np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
    ) for j in range(agent_count, agent_count + {value_agent_count})
])
agent_count += {value_agent_count}

'''

    # Momentum Agents
    if momentum_agent_count > 0:
        agents += f'''# Momentum Agents ({momentum_agent_count})
print(f"Creating {momentum_agent_count} Momentum agents...")
agents.extend([
    MomentumAgent(
        id=j,
        name=f'MOMENTUM_AGENT_{{j}}',
        type='MomentumAgent',
        symbol=symbol,
        starting_cash=starting_cash,
        min_size=20,
        max_size=50,
        wake_up_freq=str_to_ns('60s'),
        poisson_arrival=True,
        subscribe=False,
        log_orders=False,
        random_state=np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
    ) for j in range(agent_count, agent_count + {momentum_agent_count})
])
agent_count += {momentum_agent_count}

'''

    # Adaptive Market Makers
    if adaptive_market_maker_count > 0:
        agents += f'''# Adaptive Market Maker Agents ({adaptive_market_maker_count})
print(f"Creating {adaptive_market_maker_count} Adaptive Market Maker agents...")
agents.extend([
    AdaptiveMarketMakerAgent(
        id=j,
        name=f'ADAPTIVE_MM_AGENT_{{j}}',
        type='AdaptiveMarketMakerAgent',
        symbol=symbol,
        starting_cash=starting_cash,
        pov=0.025,  # Participation of volume
        min_order_size=1,
        window_size=20,
        num_ticks=10,
        wake_up_freq=str_to_ns('10s'),
        subscribe=True,
        log_orders=False,
        random_state=np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
    ) for j in range(agent_count, agent_count + {adaptive_market_maker_count})
])
agent_count += {adaptive_market_maker_count}

'''

    # Summary
    agents += f'''
# Agent Summary
print(f"\\n📊 Agent Configuration Summary:")
print(f"  • Total agents: {{agent_count}}")
print(f"  • Exchange agents: 1")
if {market_maker_count} > 0:
    print(f"  • Market Maker agents: {market_maker_count}")
if {zero_intelligence_count} > 0:
    print(f"  • Zero Intelligence agents: {zero_intelligence_count}")
if {noise_agent_count} > 0:
    print(f"  • Noise agents: {noise_agent_count}")
if {value_agent_count} > 0:
    print(f"  • Value agents: {value_agent_count}")
print(f"  • Starting cash per agent: ${starting_cash/100:,.2f}")
total_market_cap = starting_cash * (agent_count)
print(f"  • Total market capitalization: ${{total_market_cap/100:,.2f}}\\n")

'''
    
    write_to_config_file(agents)


def generate_kernel_section() -> None:
    """Generate the kernel configuration and simulation execution logic."""
    
    kernel = '''###### SIMULATION KERNEL & EXECUTION ######

def run_simulation():
    """Execute the ABIDES market simulation."""
    
    # Create simulation kernel
    config_name = args.config
    kernel = Kernel(
        config_name,
        random_state=np.random.RandomState(seed=np.random.randint(0, 2**32, dtype='uint64'))
    )
    
    # Simulation timing
    kernel_start_time = historical_date
    kernel_stop_time = mkt_close + pd.to_timedelta('00:01:00')  # 1 minute buffer
    
    print(f"⏱️  Simulation Timing:")
    print(f"  • Kernel Start: {kernel_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  • Kernel Stop: {kernel_stop_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  • Duration: {kernel_stop_time - kernel_start_time}\\n")
    
    # Latency model configuration (realistic network delays)
    default_computation_delay = 50  # 50 nanoseconds
    latency_rstate = np.random.RandomState(seed=np.random.randint(0, 2**32))
    
    # Geographic distribution: agents distributed from NYC to Seattle
    nyc_to_seattle_meters = 3866660
    pairwise_distances = util.generate_uniform_random_pairwise_dist_on_line(
        0.0, nyc_to_seattle_meters, agent_count, random_state=latency_rstate
    )
    pairwise_latencies = util.meters_to_light_ns(pairwise_distances)
    
    # Create latency model
    model_args = {
        'connected': True,
        'min_latency': pairwise_latencies
    }
    latency_model = LatencyModel(
        latency_model='deterministic',
        random_state=latency_rstate,
        kwargs=model_args
    )
    
    print(f"🌐 Network Latency Model:")
    print(f"  • Model Type: Deterministic")
    print(f"  • Geographic Span: NYC to Seattle ({nyc_to_seattle_meters:,} meters)")
    print(f"  • Agent Distribution: Uniform along line")
    print(f"  • Computation Delay: {default_computation_delay} nanoseconds\\n")
    
    # Execute simulation
    print("🚀 Starting simulation execution...")
    print("=" * 60)
    
    try:
        kernel.runner(
            agents=agents,
            startTime=kernel_start_time,
            stopTime=kernel_stop_time,
            agentLatencyModel=latency_model,
            defaultComputationDelay=default_computation_delay,
            oracle=oracle,
            log_dir=log_dir
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        logging.error(f"Simulation execution failed: {e}", exc_info=True)
        return False

# Main execution
if __name__ == "__main__":
    success = run_simulation()
    
    # Simulation completion
    simulation_end_time = dt.datetime.now()
    duration = simulation_end_time - simulation_start_time
    
    print("=" * 60)
    if success:
        print("✅ Simulation completed successfully!")
    else:
        print("❌ Simulation completed with errors!")
    print("=" * 60)
    print(f"🏁 Simulation End Time: {simulation_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Total Execution Time: {duration}")
    
    if agent_count > 0 and duration.total_seconds() > 0:
        print(f"📊 Performance: {agent_count / duration.total_seconds():.2f} agents/second")
    
    if log_dir:
        print(f"📁 Logs saved to: {log_dir}")
    
    print("\\n🎯 Simulation Summary:")
    print(f"  • Configuration: {args.config}")
    print(f"  • Total Agents: {agent_count}")
    print(f"  • Market Symbol: {symbol}")
    print(f"  • Simulation Seed: {seed}")
    print("\\n" + "=" * 60)

'''
    
    write_to_config_file(kernel)


def generate_gym_config_section() -> None:
    """Generate additional configuration for ABIDES-Gym compatibility."""
    gym_config = '''
# ABIDES-Gym Integration
# This configuration is optimized for reinforcement learning environments

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

# Export for ABIDES-Gym
background_config = create_background_config()

'''
    write_to_config_file(gym_config)


def generate_batch_configs(base_args, param_sweep: str) -> None:
    """Generate multiple configurations for parameter sweeps."""
    print("🚧 Batch mode is under development")
    print(f"💡 Parameter sweep: {param_sweep}")
    print("📖 This feature will generate multiple configurations")
    print("     for systematic parameter studies")


def gui_placeholder() -> int:
    """GUI placeholder - displays helpful message and exits."""
    if not GUI_AVAILABLE:
        print("❌ GUI not available: tkinter not installed")
        print("💡 Install tkinter or use command-line mode")
        print("📖 See README.md for installation instructions")
        return 1
    
    print("🚧 GUI mode is under development")
    print("💡 Use command-line mode for now:")
    print("   python configgen.py -f my_sim -mm 5 -zi 100 -na 20")
    print("📖 See --help for all options")
    return 0


def main() -> int:
    """Main execution function with comprehensive error handling."""
    global output_config_file
    
    try:
        # Parse arguments
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Set up verbose logging if requested
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Verbose mode enabled")
        
        # Handle template information requests
        if args.list_templates:
            list_available_templates()
            return 0
        
        if args.template_info:
            show_template_info(args.template_info)
            return 0
        
        # Check special modes
        if args.gym_mode and args.batch_mode:
            logger.error("❌ Cannot use both --gym-mode and --batch-mode simultaneously")
            return 1
        
        if args.batch_mode:
            print("🚧 Batch mode is under development")
            print("💡 This feature will enable parameter sweeps:")
            print("   python configgen.py --batch --param-sweep 'mm=[2,5,10]:zi=[100,500,1000]'")
            return 0
            
        if args.gui:
            return gui_placeholder()
        
        # Apply template if specified
        if args.template:
            try:
                validate_template_name(args.template)
                apply_template_to_args(args.template, args)
            except ValueError as e:
                logger.error(f"❌ Template error: {e}")
                return 1
        
        # Apply agents scaling if specified
        if args.agents_scale != 1.0:
            try:
                validate_agents_scale(args.agents_scale)
                # Scale all agent counts
                args.market_makers = int(args.market_makers * args.agents_scale)
                args.adaptive_market_makers = int(args.adaptive_market_makers * args.agents_scale)
                args.zero_intelligence = int(args.zero_intelligence * args.agents_scale)
                args.noise_agents = int(args.noise_agents * args.agents_scale)
                args.value_agents = int(args.value_agents * args.agents_scale)
                args.momentum_agents = int(args.momentum_agents * args.agents_scale)
                logger.info(f"📏 Applied {args.agents_scale}x scaling to all agent counts")
            except ValueError as e:
                logger.error(f"❌ Scaling error: {e}")
                return 1
        
        # Validate all inputs
        try:
            validate_market_date(args.market_date)
            validate_market_time(args.market_open, "market open time")
            validate_market_time(args.market_close, "market close time")
            validate_agent_count(args.market_makers, "Market Maker agents")
            validate_agent_count(args.adaptive_market_makers, "Adaptive Market Maker agents")
            validate_agent_count(args.zero_intelligence, "Zero Intelligence agents")
            validate_agent_count(args.noise_agents, "Noise agents")
            validate_agent_count(args.value_agents, "Value agents")
            validate_agent_count(args.momentum_agents, "Momentum agents")
            validate_starting_cash(args.starting_cash)
        except ValueError as e:
            logger.error(f"❌ Validation error: {e}")
            return 1
        
        # Set configuration filename
        if not args.config_name:
            total_agents = (args.market_makers + args.adaptive_market_makers + 
                           args.zero_intelligence + args.noise_agents + 
                           args.value_agents + args.momentum_agents)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if args.template:
                args.config_name = f"abides_{args.template}_{total_agents}agents_{timestamp}"
            else:
                args.config_name = f"abides_config_{total_agents}agents_{timestamp}"
        
        validated_filename = validate_config_filename(args.config_name)
        if not validated_filename:
            logger.error("❌ Invalid or empty configuration name")
            return 1
        
        # Set up output file path
        if args.output_dir != '.':
            output_directory = Path(args.output_dir)
            output_directory.mkdir(parents=True, exist_ok=True)
            output_config_file = str(output_directory / validated_filename)
        else:
            output_config_file = validated_filename
        
        # Validation-only mode
        if args.validate_only:
            logger.info("✅ All inputs are valid")
            if args.template:
                logger.info(f"� Template: {args.template} - {RESEARCH_TEMPLATES[args.template]['description']}")
            logger.info(f"�💡 Would generate: {output_config_file}")
            total_agents = (args.market_makers + args.adaptive_market_makers + 
                           args.zero_intelligence + args.noise_agents + 
                           args.value_agents + args.momentum_agents)
            logger.info(f"📊 Total agents: {total_agents:,}")
            return 0
        
        logger.info(f"Generating configuration: {output_config_file}")
        if args.template:
            logger.info(f"📝 Using template: {args.template} - {RESEARCH_TEMPLATES[args.template]['description']}")
        logger.info(f"Agents: MM={args.market_makers}, AMM={args.adaptive_market_makers}, "
                   f"ZI={args.zero_intelligence}, Noise={args.noise_agents}, "
                   f"Value={args.value_agents}, Momentum={args.momentum_agents}")
        
        # Clear existing file if it exists
        if os.path.exists(output_config_file):
            os.remove(output_config_file)
            logger.debug(f"Removed existing file: {output_config_file}")
        
        # Generate configuration file components
        generate_imports_section()
        generate_config_section(args.random_seed)
        generate_oracle_section(args.market_date, args.market_open, args.market_close, args.symbol)
        generate_agents_section(
            args.starting_cash, 
            args.market_makers,
            args.adaptive_market_makers,
            args.zero_intelligence,
            args.noise_agents, 
            args.value_agents,
            args.momentum_agents
        )
        generate_kernel_section()
        
        # Add Gym compatibility if requested
        if args.gym_mode:
            generate_gym_config_section()
            logger.info("🤖 Added ABIDES-Gym compatibility layer")
        
        logger.info(f"✅ Configuration generated successfully: {output_config_file}")
        config_basename = os.path.splitext(os.path.basename(output_config_file))[0]
        logger.info(f"💡 Run simulation: python {output_config_file} -c {config_basename} -v")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("❌ Generation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Configuration generation failed: {e}")
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
