from commitment import Commitment
from hashlib import sha256

# the field size of the pairing group used in our implementation, SS512, is 159 bits.
Field_size = 159

def sort_nodes(nodes):
    nodes.sort(key = lambda cur_node: cur_node.data)
    return nodes

class Node:
    def __init__(self, data:str = None, hash = None) -> None:
        self.proof = None
        self.data = data
        if self.data != None:
            self.hash = sha256(data.encode()).hexdigest()
        else:
            self.hash = hash

class VerkleTree:
    def __init__(self, leaves:list[str], k) -> None:
        self.leaves = [Node(data=x) for x in leaves.copy()]
        self.leaves = sort_nodes(self.leaves)
        self.k = k
        # q = random.randint(pow(10, level), 9 * pow(10, level))
        self.commitment_scheme = Commitment()
        self.commitment_scheme.key_gen(256,self.k)
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
                children_node_hash = [int(s.hash, 16) for s in children_nodes]
                C = self.commitment_scheme.commit(children_node_hash, self.k)
                commited_hash = sha256(self.commitment_scheme.pairing.serialize(C)).hexdigest()
                parent = Node(hash=commited_hash)
                parent.C = C
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

    def __get_values(self, position, level):
        h = self.commitment_scheme.H[position % self.k]
        if self.all_nodes[level][position].proof == None:
            siblings = self.__get_siblings(position, level)
            sibling_hash = [int(s.hash, 16) for s in siblings]
            self.all_nodes[level][position].proof = self.commitment_scheme.open(self.all_nodes[level][position].hash, position % self.k, sibling_hash, self.k)
        proof = self.all_nodes[level][position].proof
        cur_commitment = self.all_nodes[level-1][position//self.k].C
        return h, proof, cur_commitment

    def membership(self, node_to_check, position, hash, size_of_leaves = None):
        if size_of_leaves==None:
            size_of_leaves = self.leaves.__len__()
        hash_node_to_check = int(sha256(node_to_check.encode()).hexdigest(), 16)
        level = self.all_nodes.__len__() - 1
        while level > 0:
            h, proof, parent_commitment = self.__get_values(position, level)
            if (self.commitment_scheme.verify(parent_commitment, hash_node_to_check, position%self.k, proof)) == 0:
                break
            hash_node_to_check = int(sha256(self.commitment_scheme.pairing.serialize(parent_commitment)).hexdigest(), 16)
            position = position // self.k
            level -= 1

        if hash_node_to_check == int(hash, 16):
            return 1, (self.all_nodes.__len__())*(Field_size*2)*3
        return 0, (self.all_nodes.__len__())*(Field_size*2)*3
        

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

    def non_membership(self, node_to_check):
        prev, next = self.find_index(self.leaves, node_to_check)
        ret_val = {}
        if prev != None:
            assert self.membership(node_to_check, prev, self.root.hash) == 0, "Value sent to not_present is in the leaves!!!."
        if prev != None:
            ret_val["prev"] = {"node": self.leaves[prev], "index": prev}
            print(f"previous node data {self.leaves[prev].data} and index {prev}")
        if next != None:
            ret_val["next"] = {"node": self.leaves[next], "index": next}
            print(f"next node data {self.leaves[next].data} and index {next}")
        return ret_val
