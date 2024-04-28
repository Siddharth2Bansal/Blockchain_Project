from verkle_tree import VerkleTree
from merkle_tree import MerkleTree
import time
import matplotlib.pyplot as plt

# leaves = []
# for i in range(0, 1<<8):
#     leaves.append(str(i))

# st1 = time.time()
# mt = MerkleTree(leaves, 36)
# e1 = time.time()

# print("time taken for merkle = ", e1-st1)

# st1 = time.time()
# vt = VerkleTree(leaves, 36)
# e1 = time.time()

# print("time taken for verkle = ", e1-st1)

# # mt.print_tree()
# element = mt.leaves[190].data
# print(element)
# # vt.print_tree()

# print(mt.present(element, 190, hash=mt.root.hash))
# print(vt.present(element,190, hash=vt.root.hash))

# compare the tree creation times for merkle and verkle trees for different number of leaves
merkle_times = []
verkle_times = []
leaves = []
for i in range(0, 1<<12):
    leaves.append(str(i))

for i in range(1, 13):
    st1 = time.time()
    mt = MerkleTree(leaves[:1<<i], 36)
    print("number of leaves = ", 1<<i)
    e1 = time.time()
    merkle_times.append(e1-st1)
    print("time taken for merkle = ", e1-st1)

    st1 = time.time()
    vt = VerkleTree(leaves[:1<<i], 36)
    e1 = time.time()
    verkle_times.append(e1-st1)
    print("time taken for verkle = ", e1-st1)


# plt.plot([1<<i for i in range(1, 13)], merkle_times, label="Merkle Tree")
# plt.plot([1<<i for i in range(1, 13)], verkle_times, label="Verkle Tree")

# make a separate y axis for merkle tree and verkle tree
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot([str(1<<i) for i in range(1, 13)], merkle_times, label="Merkle Tree", color='r')
ax2.plot([str(1<<i) for i in range(1, 13)], verkle_times, label="Verkle Tree", color='b')
ax1.set_xlabel("Number of Leaves")
ax1.set_ylabel("Time taken to create Merkle Tree", color='r')
ax1.set_ylim(0, 0.005)
ax2.set_ylabel("Time taken to create Verkle Tree", color='b')
ax2.set_ylim(0, 5)
# plt.show()
plt.savefig("tree_creation_time3.png", dpi=300)