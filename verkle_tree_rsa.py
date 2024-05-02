from commitment_rsa import Commitment_RSA
import random
from hashlib import sha256
import sys


def sort_nodes(nodes):
    nodes.sort(key = lambda cur_node: cur_node.data)
    return nodes

class Node:
    def __init__(self, data:str = None, hash = None) -> None:
        self.proof = None
        self.data = data
        if self.data != None:
            self.hash = int(sha256(data.encode()).hexdigest(), 16)
        else:
            self.hash = hash


class VerkleTree_RSA:
    def __init__(self, leaves:list[str], k, size_domain, size_proof) -> None:
        self.leaves = [Node(data=x) for x in leaves.copy()]
        self.leaves = sort_nodes(self.leaves)
        self.k = k
        # q = random.randint(pow(10, level), 9 * pow(10, level))
        self.commitment_scheme = Commitment_RSA()
        self.commitment_scheme.key_gen(size_domain,self.k, size_proof)
        self.__build_tree(k)
    
    # building Verkle Tree from given leaves and branching factor
    def __build_tree(self,k):
        nodes = self.leaves.copy()
        self.all_nodes = []
        # building tree layer wise from bottom
        while(nodes.__len__() > 1):
            upper_layer = []

            # adding extra nodes to fill last node
            temp = nodes.__len__() % k
            if temp != 0:
                for i in range(k - temp):
                    nodes.append(Node(data="-1"))
            self.all_nodes.append(nodes)
            # creating parent nodes for all sets of childern
            for i in range(nodes.__len__()//k):
                children_nodes = nodes[i*k:(i+1)*k]
                children_node_hash = [s.hash for s in children_nodes]
                # parent = Node(get_commitment(children_nodes), children_nodes)
                commited_hash = self.commitment_scheme.commit(children_node_hash, self.k)
                parent = Node(hash=commited_hash)
                # for child_index in range(children_nodes.__len__()):
                #     children_nodes[child_index].proof = self.commitment_scheme.produce_proof(children_nodes[child_index].hash, child_index, children_node_hash, self.k)
                upper_layer.append(parent)
            nodes = upper_layer
        self.all_nodes.append(nodes)
        # setting root
        self.all_nodes.reverse()
        self.root = nodes[0]

    
    def print_tree(self):
        # for level in self.all_nodes:
        #     level = [node.data for node in level]
        #     print("".join(str(level)))
        print([x.data for x in self.leaves])


    def __get_siblings(self, index, level):
        i = index // self.k
        return self.all_nodes[level][i*self.k : (i+1)*self.k]

    def __get_values(self, position, level):
        e = self.commitment_scheme.E[position % self.k]
        if self.all_nodes[level][position].proof == None:
            siblings = self.__get_siblings(position, level)
            sibling_hash = [s.hash for s in siblings]
            self.all_nodes[level][position].proof = self.commitment_scheme.produce_proof(self.all_nodes[level][position].hash, position % self.k, sibling_hash, self.k)
        proof = self.all_nodes[level][position].proof
        cur_commitment = self.all_nodes[level-1][position//self.k].hash
        return e, proof, cur_commitment

    def present(self, node_to_check, position, hash, size_of_leaves = None):
        if size_of_leaves==None:
            size_of_leaves = self.leaves.__len__()
        hash_node_to_check = int(sha256(node_to_check.encode()).hexdigest(), 16)
        level = self.all_nodes.__len__() - 1
        while level > 0:
            h, proof, parent_commitment = self.__get_values(position, level)
            if (self.commitment_scheme.verify(parent_commitment, hash_node_to_check, position%self.k, proof)) == 0:
                break
            hash_node_to_check = parent_commitment
            position = position // self.k
            level -= 1
        # print(hash_node_to_check.value)
        # print(hash)
        if hash_node_to_check == hash:
            # print("Same data\n")
            return 1
        # print("Data changed!!!!\n")
        return 0
        

    def find_index(self, nodes, check_value: str):
        n = nodes.__len__()
        for i in range(n):
            if nodes[i].data > check_value:
                break
        prev = i-1
        next = i
        if i == 0:
            prev = None
            next = i
        if nodes[n-1].data < check_value:
            prev = n - 1
            next = None
        return prev, next

    def not_present(self, node_to_check):
        prev, next = self.find_index(self.leaves, node_to_check)
        ret_val = {}
        if prev != None:
            assert self.present(node_to_check, prev, self.root.hash) == 0, "Value sent to not_present is in the leaves!!!."
        if prev != None:
            ret_val["prev"] = {"node": self.leaves[prev], "index": prev}
            print(f"previous node data {self.leaves[prev].data} and index {prev}")
        if next != None:
            ret_val["next"] = {"node": self.leaves[next], "index": next}
            print(f"next node data {self.leaves[next].data} and index {next}")
        return ret_val

start_leaves = []
for i in range(10):
#     # new_node = Node(data=str(10 - i))
    # new_node = Node(2*i)
    start_leaves.append(str(10-i))
new_tree = VerkleTree_RSA(start_leaves, 3, 20, 5)

new_tree.print_tree()

# # sorted_nodes = sort_nodes(start_leaves)
# # level = [node.value for node in sorted_nodes]
# # print(" ".join(str(level)))


print(new_tree.present("1", 0, new_tree.root.hash))
new_tree.not_present("-55")


# def find_index(nodes, check_node):
#     n = nodes.__len__()
#     for i in range(n):
#         if nodes[i].value > check_node.value:
#             break
#     prev = i-1
#     next = i
#     if i == 0:
#         prev = None
#         next = i
#     if nodes[n-1].value < check_node.value:
#         prev = n - 1
#         next = None
#     return prev, next

# print(find_index(start_leaves, Node(15)))
# print(find_index(start_leaves, Node(35)))
# print(find_index(start_leaves, Node(-5)))
# print(find_index(start_leaves, Node(8)))
# print(find_index(start_leaves, Node(20)))