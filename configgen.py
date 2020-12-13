import argparse
import os.path
import tkinter as tk

## parse args for command line execution (not recommended but supported) ##
parser = argparse.ArgumentParser(description='usage: configgen.py [-o output_dir] [-f file_name]')
parser.add_argument('-g', action="store_true", help="Start GUI")
parser.add_argument('-o', metavar='output_dir', help="Directory to put output, recommend using abides/config/")
parser.add_argument('-f', metavar='file_name', help="Base file name for output files")
parser.add_argument('-m', metavar='market_maker', help="Number of Market Maker agents needed in config")
parser.add_argument('-z', metavar='zero_intel', help="Number of Zero Intelligence agents needed in config")
parser.add_argument('-n', metavar='noise', help="Number of Noise agents needed in config")
parser.add_argument('-v', metavar='value', help="Number of Value agents needed in config")
#parser.add_argument('--doh', action="store_true", help="Use default upstream DoH server")
args = parser.parse_args()

LARGE_FONT= ("Verdana", 12)

def set_final_config(filename):
    global final_config
    final_config = filename

## write to file, append only ## 
def write_to_file(data):
    f = open(final_config, "a")
    f.write(data)
    f.close()

## adds default imports to file ##
def add_imports():

    imports = "###### IMPORTS ######\n\n"

    ## add defaults (numpy, argsparse, pandas, etc.) ##
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

## add general configuration information to file ##
def add_gen_config(seed):

    gen = "###### GENERAL CONFIGURATION INFORMATION ######\n\n"

    ## parsing arguments ##
    gen += "parser = argparse.ArgumentParser(description='Default generated options for parsing arguments')\n"
    gen += "parser.add_argument('-c', '--config', required=True, help='Name of config file to execute')\n"
    gen += "parser.add_argument('-l', '--log_dir', default=None, help='Log directory name (default: unix timestamp at program start)')\n"
    gen += "parser.add_argument('-s', '--seed', type=int, default=None, help='numpy.random.seed() for simulation')\n"
    gen += "parser.add_argument('-v', '--verbose', action='store_true', help='Maximum verbosity!')\n"
    gen += "args, remaining_args = parser.parse_known_args()\n\n"

    try:
        seed = int(seed)
    except ValueError:
        seed = None
    
    if not seed:
        seed = "int(pd.Timestamp.now().timestamp() * 1000000) % (2 ** 32 - 1)"

    ## general setup information ##
    gen += "log_dir = args.log_dir\nseed = " + str(seed) + "\n"
    gen += "np.random.seed(seed)\nutil.silent_mode = not args.verbose\n\n"
    
    ## simulation start information ##
    gen += "simulation_start_time = dt.datetime.now()\nprint('Simulation Start Time: {}'.format(simulation_start_time))\n"
    gen += "print('Configuration seed: {}'.format(seed))\n\n\n"
 
    write_to_file(gen)

## add oracle information to file ##
def add_oracle(date = "2019-06-28", mkt_open = "09:30:00", mkt_close = "16:00:00"):
    oracle = "###### ORACLE ######\n\n"

    if date == "":
        date = "2019-06-28"
    if mkt_open == "":
        mkt_open = "09:30:00"
    if mkt_close == "":
        mkt_close = "16:00:00"

    ## add default historical date and market open/close times ##
    oracle += "historical_date = pd.to_datetime('" + date + "') #change if needed\nsymbol = 'JPM' #change if needed\n"
    oracle += "mkt_open = historical_date + pd.to_timedelta('" + mkt_open + "')\nmkt_close = historical_date + pd.to_timedelta('" + mkt_close + "')\n\n"
    
    ## add default symbols ##
    oracle += "symbols = {symbol: {'r_bar': 1e5, 'kappa': 1.67e-12, 'agent_kappa': 1.67e-15, 'sigma_s': 0, 'fund_vol': 1e-4,"
    oracle += "'megashock_lambda_a': 2.77778e-13, 'megashock_mean': 1e3, 'megashock_var': 5e4, 'random_state': np.random.RandomState(seed=np.random.randint(low=0, high=2 ** 32, dtype='uint64'))}}\n\n"
    
    ## implement default oracle ##
    oracle += "oracle = SparseMeanRevertingOracle(mkt_open, mkt_close, symbols) #default oracle setting, can change if needed\n\n"

    write_to_file(oracle)

class configGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, FileConfig, GenConfig, OracleConfig, AgentConfig):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        intro = tk.Label(self, text="""
        This app is designed to quickly create configuration files for the
        ABIDES: Agent-Based Interactive Discrete Event Simulation environment
        
        Table of Contents: 
        Specify Output File -> Seed for Simulation -> Oracle Settings -> Agent Settings""", font=LARGE_FONT)
        intro.grid(row = 0, column = 0)

        start_button = tk.Button(self, text="Start",
                            command=lambda: controller.show_frame(FileConfig))
        start_button.grid(row = 1, column = 0)


class FileConfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Please specify the file name that will contain the generated data. This generator 
        will put the file in the same directory that contains the generator.
        """, font=LARGE_FONT)
        label.grid(row = 0, column = 0)

        tk.Label(self, text="Specify Filename: ").grid(row=1)
        entry = tk.Entry(self)
        entry.grid(row = 2, column = 0)
        
        """
        backbtn = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        backbtn.grid(row = 4, column = 0, sticky = "nsew")
        """

        nextbtn = tk.Button(self, text="Next",
                            command=lambda: [controller.show_frame(GenConfig), set_final_config(entry.get()), add_imports()] if entry.get() else lambda: controller.show_frame(FileConfig))
        nextbtn.grid(row = 4, column = 0)

class GenConfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Please specify a seed for the simulation. When running the simulation using the 
        generated config file, a seed will be generated using numpy's random seed functionality.
        """, font=LARGE_FONT)
        label.grid(row = 0, column = 0)

        tk.Label(self, text="Specify Seed: ").grid(row=1)
        entry = tk.Entry(self)
        entry.grid(row = 2, column = 0)

        """
        backbtn = tk.Button(self, text="Back",
                            command=lambda: [controller.show_frame(FileConfig)])
        backbtn.grid(row = 4, column = 0, sticky="nsew")
        """

        nextbtn = tk.Button(self, text="Next",
                            command=lambda: [controller.show_frame(OracleConfig), add_gen_config(entry.get())])
        nextbtn.grid(row = 4, column = 0)

class OracleConfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Please enter the market date, market open time, and market close time for the day
        that you want to simulate using this configuration file""", font=LARGE_FONT)
        label.grid(row = 0, column = 0)

        tk.Label(self, text="Specify Market Date (YYYY-MM-DD): ").grid(row = 1)
        mkt_entry = tk.Entry(self)
        mkt_entry.grid(row = 2, column = 0)

        label = tk.Label(self, text=" ", font=LARGE_FONT)
        label.grid(row = 3, column = 0)

        tk.Label(self, text="Specify Market Open Time (HH:MM:SS): ").grid(row = 4)
        open_entry = tk.Entry(self)
        open_entry.grid(row = 5, column = 0)

        label = tk.Label(self, text=" ", font=LARGE_FONT)
        label.grid(row = 6, column = 0)

        tk.Label(self, text="Specify Market Close Time (HH:MM:SS): ").grid(row = 7)
        close_entry = tk.Entry(self)
        close_entry.grid(row = 8, column = 0)

        label = tk.Label(self, text=" ", font=LARGE_FONT)
        label.grid(row = 9, column = 0)

        nextbtn = tk.Button(self, text="Next",
                            command=lambda: [controller.show_frame(AgentConfig), add_oracle(mkt_entry.get(), open_entry.get(), close_entry.get())])
        nextbtn.grid(row = 10, column = 0)

class AgentConfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=""" 
        """, font=LARGE_FONT)
        label.grid(row = 0, column = 0)

        tk.Label(self, text="Starting Cash (in cents): ").grid(row = 1)
        cash_entry = tk.Entry(self)
        cash_entry.grid(row = 2, column = 0)

        label = tk.Label(self, text=" ", font=LARGE_FONT)
        label.grid(row = 3, column = 0)

        tk.Label(self, text="Number of Market Maker Agents: ").grid(row = 4)
        mm_entry = tk.Entry(self)
        mm_entry.grid(row = 5, column = 0)

        label = tk.Label(self, text=" ", font=LARGE_FONT)
        label.grid(row = 6, column = 0)

        tk.Label(self, text="Number of Zero Intelligence Agents:").grid(row = 7)
        zi_entry = tk.Entry(self)
        zi_entry.grid(row = 8, column = 0)

        label = tk.Label(self, text=" ", font=LARGE_FONT)
        label.grid(row = 9, column = 0)

        tk.Label(self, text="Number of Noise Agents: ").grid(row = 10)
        n_entry = tk.Entry(self)
        n_entry.grid(row = 11, column = 0)

        label = tk.Label(self, text=" ", font=LARGE_FONT)
        label.grid(row = 12, column = 0)

        tk.Label(self, text="Number of Value Agents: ").grid(row = 13)
        v_entry = tk.Entry(self)
        v_entry.grid(row = 14, column = 0)

        finish_btn = tk.Button(self, text="Finish",
                            command=lambda: [controller.show_frame(StartPage), add_agents(cash_entry.get(), mm_entry.get(), zi_entry.get(), n_entry.get(), v_entry.get())])
        finish_btn.grid(row = 15, column = 0)

def add_agents(cash = 10000000, num_mm = 0, num_zi = 0, num_n = 0, num_v = 0):

    if cash == "":
        cash = 10000000
    if num_mm == "":
        num_mm = 0
    if num_zi == "":
        num_zi = 0
    if num_n == "":
        num_n = 0
    if num_v == "":
        num_v = 0
    

    ## add default vars, note starting cash ##
    agents = "agent_count, agents, agent_types = 0, [], []\nstarting_cash = " + str(cash) + "\n"  #in cents, change if needed,"
    
    ## add only one echange agent, uniform across all config files ##
    agents += "agents.extend([ExchangeAgent(id=0, name='EXCHANGE_AGENT', type='ExchangeAgent', mkt_open=mkt_open," 
    agents += "mkt_close=mkt_close, symbols=[symbol], log_orders=False, pipeline_delay=0, computation_delay=0, stream_history=10,"
    agents += "book_freq = 0, random_state=np.random.RandomState(seed=np.random.randint(low=0, high=2 ** 32, dtype='uint64')))])\n"
    agents += "agent_types.extend('ExchangeAgent')\nagent_count += 1\n\n"

    ## market maker ##
    if args.m:
        num_mm = args.m

    if int(num_mm) > 0:
        agents += "num_mm_agents = " + str(num_mm) + "\n"
        agents += "agents.extend([MarketMakerAgent(id=j, name='MARKET_MAKER_AGENT_{}'.format(j), type='MarketMakerAgent', symbol=symbol,"
        agents += "starting_cash=starting_cash, min_size=500, max_size=1000, log_orders=False,"
        agents += "random_state=np.random.RandomState(seed=np.random.randint(low=0, high=2 ** 32, dtype='uint64'))) "
        agents += "for j in range(agent_count, agent_count + num_mm_agents)])\n\n"
        agents += "agent_types.extend('MarketMakerAgent')\nagent_count += num_mm_agents\n\n"

    ## ZI ##
    if args.z:
        num_zi = args.z

    if int(num_zi) > 0:
        agents += "num_zi_agents = " + str(num_zi) + "\n"
        agents += "agents.extend([ZeroIntelligenceAgent(id=j, name='ZI_AGENT_{}'.format(j), type='ZeroIntelligenceAgent', symbol=symbol,"
        agents += "starting_cash=starting_cash, log_orders=False, random_state=np.random.RandomState(seed=np.random.randint(low=0, high=2 ** 32,"
        agents += "dtype='uint64'))) for j in range(agent_count, agent_count + num_zi_agents)])\n\n"
        agents += "agent_types.extend('ZeroIntelligenceAgent')\nagent_count += num_zi_agents\n\n"

    ## Noise ##
    if args.n:
        num_n = args.n

    if int(num_n) > 0:
        agents += "num_noise = " + str(num_n) + "\n"
        agents += "noise_mkt_open = historical_date + pd.to_timedelta('09:00:00')\nnoise_mkt_close = historical_date + pd.to_timedelta('16:00:00')\n"
        agents += "agents.extend([NoiseAgent(id=j, name='NoiseAgent {}'.format(j), type='NoiseAgent', symbol=symbol, starting_cash=starting_cash,"
        agents += "wakeup_time=util.get_wake_time(noise_mkt_open, noise_mkt_close), log_orders=log_orders,"
        agents += "random_state=np.random.RandomState(seed=np.random.randint(low=0, high=2 ** 32, dtype='uint64')))"
        agents += " for j in range(agent_count, agent_count + num_noise)])\n\nagent_count += num_noise\nagent_types.extend(['NoiseAgent'])\n\n"

    ## Value ##
    if args.v:
        num_v = args.v
    
    if int(num_v) > 0:
        agents += "num_value = " + str(num_v) + "\n"
        agents += "agents.extend([ValueAgent(id=j, name='Value Agent {}'.format(j), type='ValueAgent', symbol=symbol, starting_cash=starting_cash,"
        agents += "random_state=np.random.RandomState(seed=np.random.randint(low=0, high=2 ** 32, dtype='uint64')))"
        agents += "for j in range(agent_count, agent_count + num_value)])\n\nagent_count += num_value\nagent_types.extend(['ValueAgent'])\n\n"
    
    write_to_file(agents)

def add_kernel():
    

if __name__ == "__main__":

    gui = False
    global final_config
    final_config = "defaultconfig.py"

    if args.f:
        final_config = str(args.f)
    if args.o:
        final_config = os.path.join(str(args.o), final_config)

    if args.g:
        gui = True
        app = configGUI()
        app.title("ABIDES Configuration Generator")
        app.mainloop()
    
    if not gui:
        ## add imports to file ##
        add_imports()

        ## add general configuration information to file ##
        add_gen_config(None)

        ## add oracle information ##
        add_oracle()

        ## add agents ##
        add_agents()

        ## add kernel information ##
        add_kernel()