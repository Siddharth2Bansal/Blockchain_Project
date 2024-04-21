
def get_commitment(nodes):
    s = ""
    for n in nodes: 
        s = s + n.value
    return s

def sort_nodes(nodes):
    nodes.sort(key = lambda cur_node: cur_node.value)
    return nodes

class Node:
    def __init__(self, value, children, parent = 1) -> None:
        self.value = value
        self.children = children
        self.parent = parent


class VerkleTree:
    def __init__(self, leaves:list[Node], k) -> None:
        self.leaves = leaves.copy()
        self.leaves = sort_nodes(self.leaves)
        self.k = k
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
                    nodes.append(Node("-1", []))
            self.all_nodes.append(nodes)
            # creating parent nodes for all sets of childern
            for i in range(nodes.__len__()//k):
                children_nodes = nodes[i*k:(i+1)*k]
                parent = Node(get_commitment(children_nodes), children_nodes)
                upper_layer.append(parent)
            nodes = upper_layer
        self.all_nodes.append(nodes)
        # setting root
        self.all_nodes.reverse()
        self.root = nodes[0]

    
    def print_tree(self):
        for level in self.all_nodes:
            level = [node.value for node in level]
            print(" ".join(level))


    def __get_siblings(self, index, level):
        i = index // self.k
        return self.all_nodes[level][i*self.k : (i+1)*self.k]

    def present(self, node_to_check, position, hash, size_of_leaves = None):
        if size_of_leaves==None:
            size_of_leaves = self.leaves.__len__()

        level = self.all_nodes.__len__() - 1
        while level > 0:
            siblings = self.__get_siblings(position, level)
            siblings[position%self.k] = node_to_check
            node_to_check = Node(get_commitment(siblings), [])
            position = position // self.k
            level -= 1
        # print(node_to_check.value)
        # print(hash)
        if node_to_check.value == hash:
            # print("Same data\n")
            return 1
        # print("Data changed!!!!\n")
        return 0
        

    def find_index(self, nodes, check_node):
        n = nodes.__len__()
        for i in range(n):
            if nodes[i].value > check_node.value:
                break
        prev = i-1
        next = i
        if i == 0:
            prev = None
            next = i
        if nodes[n-1].value < check_node.value:
            prev = n - 1
            next = None
        return prev, next

    def not_present(self, node_to_check):
        prev, next = self.find_index(self.leaves, node_to_check)
        ret_val = {}
        if prev != None:
            assert self.present(node_to_check, prev, self.root.value) == 0, "Value sent to not_present is in the leaves!!!."
        if prev != None:
            ret_val["prev"] = {"node": self.leaves[prev], "index": prev}
            print(f"previous node hash {self.leaves[prev].value} and index {prev}")
        if next != None:
            ret_val["next"] = {"node": self.leaves[next], "index": next}
            print(f"next node hash {self.leaves[next].value} and index {next}")
        return ret_val





start_leaves = []
for i in range(10):
    new_node = Node(str(10-i), [])
    # new_node = Node(2*i, [])
    start_leaves.append(new_node)

new_tree = VerkleTree(start_leaves, 3)
new_tree.print_tree()

# sorted_nodes = sort_nodes(start_leaves)
# level = [node.value for node in sorted_nodes]
# print(" ".join(str(level)))


new_tree.present(Node("9",[]), 9, new_tree.root.value)
new_tree.not_present(Node("15", []))


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

# print(find_index(start_leaves, Node(15, [])))
# print(find_index(start_leaves, Node(35, [])))
# print(find_index(start_leaves, Node(-5, [])))
# print(find_index(start_leaves, Node(8, [])))
# print(find_index(start_leaves, Node(20, [])))