from verkle_tree import VerkleTree
from merkle_tree import MerkleTree
import time
import matplotlib.pyplot as plt
from random import randint

# compare the tree creation times for merkle and verkle trees for different number of leaves
merkle_times = []
verkle_times = []

merkle_times_present = []
verkle_times_present = []

leaves = []
for i in range(0, 1<<16):
    leaves.append(str(i))

for i in range(4, 16):
    st1 = time.time()
    mt = MerkleTree(leaves[:1<<i], 36)
    print("-------------------------------Next Case----------------------------")
    print("number of leaves = ", 1<<i)
    e1 = time.time()
    merkle_times.append(e1-st1)
    print("time taken for merkle = ", e1-st1)

    st1 = time.time()
    vt = VerkleTree(leaves[:1<<i], 36)
    e1 = time.time()
    verkle_times.append(e1-st1)
    print("time taken for verkle = ", e1-st1)

    nodes_ret = 0
    for j in range(i):
        index = randint(0, (1<<i)-1)
        nodes_ret = nodes_ret + vt.membership(leaves[index], index, hash=vt.root.hash)[1]

    verkle_times_present.append(nodes_ret//i)
    print("Average proof size(in bits) for verkle Tree membership = ", nodes_ret//i)


    nodes_ret = 0
    for j in range(i):
        index = randint(0, (1<<i)-1)
        nodes_ret = nodes_ret + mt.present(leaves[index], index, hash=mt.root.hash)[1]

    e1 = time.time()
    merkle_times_present.append(nodes_ret//i)
    print("Average proof size(in bits) for merkle Tree membership = ", nodes_ret//i)

# make a separate y axis for merkle tree and verkle tree
# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot([str(1<<i) for i in range(4, 16)], merkle_times, label="Merkle Tree", color='r')
# ax2.plot([str(1<<i) for i in range(4, 16)], verkle_times, label="Verkle Tree", color='b')
# ax1.set_xlabel("Number of Leaves")
# ax1.set_ylabel("Time taken to create Merkle Tree", color='r')
# ax1.set_ylim(0, 0.05)
# ax2.set_ylabel("Time taken to create Verkle Tree", color='b')
# ax2.set_ylim(0, 40)
# # plt.show()
# plt.savefig("tree_creation_time.png", dpi=300)




# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot([str(1<<i) for i in range(6, 16)], merkle_times_present, label="Merkle Tree", color='r')
# ax2.plot([str(1<<i) for i in range(6, 16)], verkle_times_present, label="Verkle Tree", color='b')
# ax1.set_xlabel("Number of Leaves")
# ax1.set_ylabel("Merkle Tree membership: Proof Size", color='r')

# ax2.set_ylabel("Verkle Tree membership: Proof Size", color='b')

# plt.savefig("tree_membership.png", dpi=300)

