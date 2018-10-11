import random
import mosaik
from mosaik.util import connect_randomly, connect_many_to_one


def main(sim_config, START, END, PV_DATA, PROFILE_FILE, GRID_NAME, GRID_FILE):
    random.seed(0)
    world = mosaik.World(sim_config)
    create_scenario(world, START, END, PV_DATA, PROFILE_FILE, GRID_NAME, GRID_FILE)
    world.run(until=END)  # As fast as possilbe
    # world.run(until=END, rt_factor=1/60)  # Real-time 1min -> 1sec


def create_scenario(world, START, END, PV_DATA, PROFILE_FILE, GRID_NAME, GRID_FILE):

    # Start simulators
    pypower = world.start('PyPower', step_size=15*60)# run every 15 mins
    hhsim = world.start('HouseholdSim')
    pvsim = world.start('CSV', sim_start=START, datafile=PV_DATA)

    # Instantiate models
    grid = pypower.Grid(gridfile=GRID_FILE).children
    houses = hhsim.ResidentialLoads(sim_start=START,
                                    profile_file=PROFILE_FILE,
                                    grid_name=GRID_NAME).children
    pvs = pvsim.PV.create(20)

    # Connect entities
    connect_buildings_to_grid(world, houses, grid)
    connect_randomly(world, pvs, [e for e in grid if 'node' in e.eid], 'P')

    # Database
    db = world.start('DB', step_size=60, duration=END)
    hdf5 = db.Database(filename='demo.hdf5')
    connect_many_to_one(world, houses, hdf5, 'P_out')
    connect_many_to_one(world, pvs, hdf5, 'P')

    nodes = [e for e in grid if e.type in ('RefBus, PQBus')]
    connect_many_to_one(world, nodes, hdf5, 'P', 'Q', 'Vl', 'Vm', 'Va')

    branches = [e for e in grid if e.type in ('Transformer', 'Branch')]
    connect_many_to_one(world, branches, hdf5,
                        'P_from', 'Q_from', 'P_to', 'Q_to')


def connect_buildings_to_grid(world, houses, grid):
    buses = filter(lambda e: e.type == 'PQBus', grid)
    buses = {b.eid.split('-')[1]: b for b in buses}
    house_data = world.get_data(houses, 'node_id')
    for house in houses:
        node_id = house_data[house]['node_id']
        world.connect(house, buses[node_id], ('P_out', 'P'))


if __name__ == '__main__':
    main()
