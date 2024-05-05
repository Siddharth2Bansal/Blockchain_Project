from hashlib import sha256
import sys


def get_commitment(nodes):
    s = ""
    for n in nodes: 
        s = s + n.hash
    return sha256(s.encode()).hexdigest()

def sort_nodes(nodes):
    nodes.sort(key = lambda cur_node: cur_node.data)
    return nodes

class Node:
    def __init__(self, data:str = None, hash = None) -> None:
        self.data = data
        if self.data != None:
            self.hash = sha256(data.encode()).hexdigest()
        else:
            self.hash = hash


class MerkleTree:
    def __init__(self, leaves:list[str], k) -> None:
        self.leaves = [Node(data=x) for x in leaves.copy()]
        self.leaves = sort_nodes(self.leaves)
        self.k = k
        self.__build_tree(k)

    # building Merkle Tree from given leaves and branching factor
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
                parent = Node(hash = get_commitment(children_nodes))
                upper_layer.append(parent)
            nodes = upper_layer
        self.all_nodes.append(nodes)
        # setting root
        self.all_nodes.reverse()
        self.root = nodes[0]

    
    def print_tree(self):
        print([x.data for x in self.leaves])


    def __get_siblings(self, index, level):
        i = index // self.k
        return self.all_nodes[level][i*self.k : (i+1)*self.k]

    def present(self, node_to_check: str, position, hash, size_of_leaves = None):
        if size_of_leaves==None:
            size_of_leaves = self.leaves.__len__()
        hash_node_to_check = sha256(node_to_check.encode()).hexdigest()
        level = self.all_nodes.__len__() - 1
        while level > 0:
            siblings = self.__get_siblings(position, level)
            siblings[position%self.k] = Node(hash=hash_node_to_check)
            hash_node_to_check = get_commitment(siblings)
            position = position // self.k
            level -= 1
 
        if hash_node_to_check == hash:
            return 1, self.all_nodes.__len__()*self.k*256


        return 0, self.all_nodes.__len__()*self.k*256
        

    def find_index(self, nodes, check_node: str):
        n = nodes.__len__()
        for i in range(n):
            if nodes[i].data > check_node:
                break
        prev = i-1
        next = i
        if i == 0:
            prev = None
            next = i
        if nodes[n-1].data < check_node:
            prev = n - 1
            next = None
        return prev, next

    def not_present(self, node_to_check: str):
        prev, next = self.find_index(self.leaves, node_to_check)
        ret_val = {}
        if prev != None:
            assert self.present(node_to_check, prev, self.root.hash) == 0, "hash sent to not_present is in the leaves!!!."
        if prev != None:
            ret_val["prev"] = {"node": self.leaves[prev], "index": prev}
            print(f"previous node data {self.leaves[prev].data} and index {prev}")
        if next != None:
            ret_val["next"] = {"node": self.leaves[next], "index": next}
            print(f"next node data {self.leaves[next].data} and index {next}")
        return ret_val





# start_leaves = []
# for i in range(10):
#     # new_node = Node(data=str(10-i))
#     # new_node = Node(2*i, [])
#     start_leaves.append(str(10-i))

# new_tree = MerkleTree(start_leaves, 3)
# new_tree.print_tree()

# # sorted_nodes = sort_nodes(start_leaves)
# # level = [node.hash for node in sorted_nodes]
# # print(" ".join(str(level)))


# # new_tree.present("9", 9, new_tree.root.hash)
# new_tree.not_present("5.5")


# def find_index(nodes, check_node):
#     n = nodes.__len__()
#     for i in range(n):
#         if nodes[i].hash > check_node.hash:
#             break
#     prev = i-1
#     next = i
#     if i == 0:
#         prev = None
#         next = i
#     if nodes[n-1].hash < check_node.hash:
#         prev = n - 1
#         next = None
#     return prev, next

# print(find_index(start_leaves, Node(15, [])))
# print(find_index(start_leaves, Node(35, [])))
# print(find_index(start_leaves, Node(-5, [])))
# print(find_index(start_leaves, Node(8, [])))
# print(find_index(start_leaves, Node(20, [])))