import numpy as np

with open('path_x.npy', 'rb') as f:
    path_x = np.load(f)
    print(path_x)
    
with open('path_y.npy', 'rb') as f:
    path_y = np.load(f)
    print(path_y)

print(path_x[0])