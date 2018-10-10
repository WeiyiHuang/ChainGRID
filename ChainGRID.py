import json
import random
import mosaik
from mosaik.util import connect_randomly, connect_many_to_one
import sawtooth_client_interact

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
    'WebVis': {
        'cmd': 'mosaik-web -s 0.0.0.0:8000 %(addr)s',
    },
}

# start time, duration, config file
START = '2014-01-01 00:00:00'
DUR = 24 * 3600  # 1 day
PV_DATA = 'data/pv_10kw.csv'
PROFILE_FILE = 'data/profiles.data.gz'
GRID_NAME = 'demo_lv_grid'
GRID_FILE = 'data/%s.json' % GRID_NAME

def register_nodes():
    with open(GRID_FILE, 'r') as f:
        grid_config = json.load(f)
        print(json.dumps(grid_config))
    bus_info = grid_config['bus']
    print(bus_info)
    bus_ids = [bus[0] for bus in bus_info]
    print(bus_ids)
    for bus_id in bus_ids:
        usr_name = bus_id
        sawtooth_client_interact.key_gen(usr_name)
        p = sawtooth_client_interact.open_cli(usr_name)
        sawtooth_client_interact.register_participant_account(p, usr_name)
        sawtooth_client_interact.close_cli(p, usr_name)

if __name__ == '__main__':
    #register_nodes()

