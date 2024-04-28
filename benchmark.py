from verkle_tree import VerkleTree
from merkle_tree import MerkleTree
from verkle_tree import Node
import time


leaves = []
for i in range(0, 1<<8):
    leaves.append(str(i))

st1 = time.time()
mt = MerkleTree(leaves, 36)
e1 = time.time()

print("time taken for merkle = ", e1-st1)

st1 = time.time()
vt = VerkleTree(leaves, 36)
e1 = time.time()

print("time taken for verkle = ", e1-st1)

# mt.print_tree()
element = mt.leaves[190].data
print(element)
# vt.print_tree()

print(mt.present(element, 190, hash=mt.root.hash))
print(vt.present(element,190, hash=vt.root.hash))