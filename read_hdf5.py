import h5py
import numpy as np

if __name__ == "__main__":
    f = h5py.File('demo.hdf5', 'r')
    print(list(f.keys()))

    relation_dataset = f['Relations']
    series_dataset = f['Series']
    print(list(relation_dataset.keys()))

    for entity in list(relation_dataset.keys()):
        tmp = relation_dataset[entity]
        #print(tmp.shape)
        #print(tmp.dtype)
        

    for entity in list(series_dataset.keys()):
        if 'node_d9' in entity:
            print('#'*100)
            print(entity)
            tmp = series_dataset[entity]
            print(list(tmp.keys()))
            for ele in list(tmp.keys()):
                print(tmp[ele].shape)
                for i in range(tmp[ele].shape[0]):
                    print(tmp[ele][i])
