import h5py
import numpy as np

def read(entity_type):

    f = h5py.File('demo.hdf5', 'r')
    relation_dataset = f['Relations']
    series_dataset = f['Series']

    # for entity in list(relation_dataset.keys()):
    #     tmp = relation_dataset[entity]

    dic = {}

    for entity in list(series_dataset.keys()):
        if entity_type in entity:
            tmp = series_dataset[entity]
            entity = entity.split('-')
            entity_name = entity[2]###
            #print(list(tmp.keys()))
            #for ele in list(tmp.keys()):
            #    print(tmp[ele][0])###
            if entity_type == 'branch':
                dic[entity_name] = (tmp['P_from'][0], tmp['P_to'][0])

    print(dic)
    return dic


if __name__ == "__main__":
    read('branch')
