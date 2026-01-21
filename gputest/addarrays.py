import numba as nb
from numba import cuda
import numpy as np

# connect to the gpu
gpu = cuda.get_current_device()
print(f'Connected to {gpu.name}')
print(f'Max blocks: {gpu.MAX_GRID_DIM_X} x {gpu.MAX_GRID_DIM_Y} x {gpu.MAX_GRID_DIM_Z}')
print(f'Max threads per block: {gpu.MAX_BLOCK_DIM_X} x {gpu.MAX_BLOCK_DIM_Y} x {gpu.MAX_BLOCK_DIM_Z}')

# kernel function
# adds arrays a and b together, stores result in c
@cuda.jit   # equivalent to __global__
def addArrays(a,b,c):
    # access threadIdx and blockDim via cuda
    i = cuda.threadIdx.x

    # result must be stored in an argument as no return value
    # at least lists are impllicitly pointers already
    c[i] = a[i] + b[i]

# create arrays
# arrays are automatically copied to GPU when the kernel is launched
a = np.asarray([5,3,2,9,6,10,77,3,0])
b = np.asarray([4,2,0,8,49,1,7,11,6])
c = np.zeros(len(a))

# launch kernel
# block and thread counts can be a value or a tuple for multidimensional
num_blocks = 1
num_threads = len(a)
# very similar to c++ syntax but with [] instead of <<<>>>
addArrays[num_blocks,num_threads](a,b,c) # type: ignore

print(f'{a}\n+\n{b}\n=\n{c}')
