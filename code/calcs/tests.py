import numpy as np

SWAP = np.array([[1, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1]])

CNOT = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]])

I = np.array([[1, 0],
              [0, 1]])

X = np.array([[0, 1],
              [1, 0]])

Y = np.array([[0, -1j],
              [1j, 0]])

Z = np.array([[1, 0],
              [0, -1]])

def tensorproduct(a, b):
     """Returns the tensor product of two matrices."""
     return np.kron(a, b)

def partialtrace(a, i):
     """Returns the partial trace of a matrix."""
     
     dims = int(np.log2(len(a)))
     shape = [2] * (2 * dims)

     a = np.reshape(a, shape)
     a = np.trace(a, axis1=i, axis2=i + dims)

     a = np.reshape(a, [2 ** (dims - 1), 2 ** (dims - 1)])
     return a

def trace(a):
     """Returns the trace of a matrix."""
     return np.trace(a)


def order(a):
     i = 0
     for b in [I, X, Y, Z]:
          res = partialtrace(a @ tensorproduct(b, I), 0)
          if (res != 0).any():
               i = i + 1

     return i

CNOTR = SWAP @ CNOT @ SWAP

print('SWAP: ', order(SWAP))
print('CNOT: ', order(CNOT))
print('X⊗X: ', order(tensorproduct(X, X)))

print('CNOT CNOTR: ', order(CNOT @ CNOTR))

# res = tensorproduct(tensorproduct(I, I), I)

# res = res @ tensorproduct(CNOT, I)
# res = res @ tensorproduct(I, CNOTR)

# res = res @ tensorproduct(CNOTR, I)
# res = res @ tensorproduct(I, CNOT)

# res = res @ tensorproduct(CNOT, I)
# res = res @ tensorproduct(I, CNOTR)

# res = res @ tensorproduct(CNOTR, I)
# res = res @ tensorproduct(I, CNOT)

# print(partialtrace(res, 1))






