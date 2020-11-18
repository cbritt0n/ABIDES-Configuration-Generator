import argparse

## parse args for command line execution (not recommended but supported) ##
parser = argparse.ArgumentParser(description='usage: configgen.py [-o output_dir] [-f file_name]')
parser.add_argument('-o', metavar='output_dir', help="Directory to put output, recommend using abides/config/")
parser.add_argument('-f', metavar='file_name', help="Base file name for output files")
#parser.add_argument('--doh', action="store_true", help="Use default upstream DoH server")
args = parser.parse_args()

final_config = ""
if args.f:
    final_config = str(args.f)

## write to file, append only## 
def write_to_file(data):
    f = open(final_config, "a")
    f.write(data)
    f.close()

## adds default imports to file ##
def add_imports():

    imports = "###### IMPORTS ######\n\n"

    ## add defaults ##
    imports += "import argparse\nimport numpy as np\nimport pandas as pd\nimport sys\nimport datetime as dt\nfrom dateutil.parser import parse\n\n"
    
    ## add kernel and utilities ##
    imports += "from Kernel import Kernel\nfrom util import util\n\n"

    ## add all oracles ##
    imports += "from util.oracle.DataOracle import DataOracle\nfrom util.oracle.ExternalFileOracle import ExternalFileOracle\n"
    imports += "from util.oracle.MeanRevertingOracle import MeanRevertingOracle\nfrom util.oracle.SparseMeanRevertingOracle import SparseMeanRevertingOracle\n\n"

    ## add all agents ##
    imports += "from agent.ExchangeAgent import ExchangeAgent\nfrom agent.FundamentalTrackingAgent import FundamentalTrackingAgent\n"
    imports += "from agent.HeuristicBeliefLearningAgent import HeuristicBeliefLearningAgent\nfrom agent.NoiseAgent import NoiseAgent\n"
    imports += "from agent.OrderBookImbalanceAgent import OrderBookImbalanceAgent\nfrom agent.ValueAgent import ValueAgent\n"
    imports += "from agent.ZeroIntelligenceAgent import ZeroIntelligenceAgent\nfrom agent.market_makers.AdaptiveMarketMakerAgent import AdaptiveMarketMakerAgent\n"
    imports += "from agent.market_makers.MarketMakerAgent import MarketMakerAgent\nfrom agent.market_makers.POVMarketMakerAgent import POVMarketMakerAgent\n"
    imports += "from agent.market_makers.SpreadBasedMarketMakerAgent import SpreadBasedMarketMakerAgent\nfrom agent.execution.POVExecutionAgent import POVExecutionAgent\n\n\n"

    ## write to final_config ##
    write_to_file(imports)

def add_gen_config():

    gen = "###### GENERAL CONFIGURATION INFORMATION ######\n\n"

    ## parsing arguments ##
    gen += "parser = argparse.ArgumentParser(description='Default generated options for parsing arguments')\n"
    gen += "parser.add_argument('-c', '--config', required=True, help='Name of config file to execute')\n"
    gen += "parser.add_argument('-l', '--log_dir', default=None, help='Log directory name (default: unix timestamp at program start)')\n"
    gen += "parser.add_argument('-s', '--seed', type=int, default=None, help='numpy.random.seed() for simulation')\n"
    gen += "parser.add_argument('-v', '--verbose', action='store_true', help='Maximum verbosity!')\n"
    gen += "args, remaining_args = parser.parse_known_args()\n\n"

    ## general setup information ##
    gen += "log_dir = args.log_dir\nseed = args.seed\nif not seed: seed = int(pd.Timestamp.now().timestamp() * 1000000) % (2 ** 32 - 1)\n"
    gen += "np.random.seed(seed)\nutil.silent_mode = not args.verbose\n\n"
    
    ## simulation start information ##
    gen += "simulation_start_time = dt.datetime.now()\nprint('Simulation Start Time: {}'.format(simulation_start_time))\n"
    gen += "print('Configuration seed: {}'.format(seed))\n\n\n"

    write_to_file(gen)

def init_gui():
    ## TODO: add gui stuff ##
    gui = ""

def add_agents():
    ## TODO: dynamically add agents based on command line ##
    agents = ""

if __name__ == "__main__":

    gui = False

    if args.f or args.o:
        gui = False
    else:
        gui = True
    
    if not gui:
        ## add imports to file ##
        add_imports()

        ## add general configuration information to file ##
        add_gen_config()

        ## add agents to file ##
        add_agents()
    else:
        init_gui()