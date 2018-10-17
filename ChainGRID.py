import json
import datetime
import random
import mosaik
from mosaik.util import connect_randomly, connect_many_to_one
import sawtooth_client_interact
import run_mosaik_demo
import read_mosaik_hdf5

sim_config = {
    'CSV': {
        'python': 'mosaik_csv:CSV',
    },
    'DB': {
        'cmd': 'mosaik-hdf5 %(addr)s',
    },
    'HouseholdSim': {
        'python': 'householdsim.mosaik:HouseholdSim',
        # 'cmd': 'mosaik-householdsim %(addr)s',
    },
    'PyPower': {
        'python': 'mosaik_pypower.mosaik:PyPower',
        # 'cmd': 'mosaik-pypower %(addr)s',
    },
}

# start time, duration, config file
START = '2014-01-01 00:00:00'
DUR = 3600  # 1 hour
PERIOD = 900 # 15 mins
NUM_OF_SIM = DUR / PERIOD
PV_DATA = 'data/pv_10kw.csv'
PROFILE_FILE = 'data/profiles.data.gz'
GRID_NAME = 'demo_lv_grid'
GRID_FILE = 'data/%s.json' % GRID_NAME
PRICE_RATIO = 1

def register_nodes(test_id):
    with open(GRID_FILE, 'r') as f:
        grid_config = json.load(f)
        print(json.dumps(grid_config))
    bus_info = grid_config['bus']
    print(bus_info)
    bus_ids = [bus[0] for bus in bus_info]
    print(bus_ids)
    for bus_id in bus_ids:
        usr_name = bus_id + '_' + test_id
        sawtooth_client_interact.key_gen(usr_name)
        p = sawtooth_client_interact.open_cli(usr_name)
        sawtooth_client_interact.register_participant_account(p, usr_name)
        sawtooth_client_interact.close_cli(p, usr_name)

def read_config_file():
    with open(GRID_FILE, 'r') as f:
        grid_config = json.load(f)
        print(json.dumps(grid_config))
    # bus
    bus_info = grid_config['bus']
    bus_ids = [bus[0] for bus in bus_info]
    # branch
    branch_info = grid_config['branch']
    branch_link_info = {}
    for branch in branch_info:
        branch_link_info[branch[0]] = (branch[1], branch[2])
    return bus_ids, branch_link_info

def transactions_between_nodes(test_id, bus_dict):
    branch_flow = read_mosaik_hdf5.read('branch')
    print(branch_flow)
    for branch in branch_flow.keys():
        print(branch)
        idx = bus_dict.get(branch_link_info[branch][0])
        bus_dict[branch_link_info[branch][0]] = bus_dict.get(branch_link_info[branch][0]) + 1
        sawtooth_client_interact.create_exchange_offer(idx, branch_link_info[branch][0] + '_' + test_id, int(branch_flow[branch][0]), PRICE_RATIO, 
                branch_link_info[branch][1] + '_' + test_id, int(-branch_flow[branch][1]))

if __name__ == '__main__':
    #register_nodes('1')
    bus_ids, branch_link_info = read_config_file()
    bus_dict = {}
    for bus in bus_ids:
        bus_dict[bus] = 0
    #for i in range(int(NUM_OF_SIM)):
    #    start_time = datetime.datetime.strptime(START, "%Y-%m-%d %H:%M:%S")
    #    print(start_time)
    #    start_time += datetime.timedelta(seconds=900*i)
    #    print(start_time)
    #    NEW_START = start_time.strftime("%Y-%m-%d %H:%M:%S")
    #    print(NEW_START)
    #    print('#'*100)
    #    print('A new simulation!')
    #    run_mosaik_demo.main(sim_config, NEW_START, PERIOD, PV_DATA, PROFILE_FILE, GRID_NAME, GRID_FILE)
    #    transactions_between_nodes('1', bus_dict)
