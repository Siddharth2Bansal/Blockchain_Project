# CDH Based implementation of Vector Commitment

from charm.toolbox.pairinggroup import PairingGroup, pair
from charm.toolbox.pairinggroup import ZR, G1, G2, GT
from random import randint

def make_bilinear_pair():
    # Initialize the pairing group
    group = PairingGroup('SS512')

    # Generate a random generator for G1
    g1 = group.random(G1)
    return g1, group


def get_bilinear_map(g1, g2):
    return pair(g1,g2)

def get_group_order(g):
    return g.order()

def Zp_multiply(x, y, p):
    z = (x*y) % p
    return z

class file:
    def __init__(self, id, file_name = "default"):
        self.file_name = file_name
        self.id = id
        # convert file type to Zp function

class Commitment:
    def key_gen(self, k, q):
        self.g, self.pairing = make_bilinear_pair()
        self.p = get_group_order(self.pairing)

        self.Z = [randint(0, self.p-1) for i in range(q)]
        self.H = []
        self.H2 = []

        for i in range(q):
            self.H.append(self.g ** self.Z[i])
        
        
        for i in range(q):
            temp = []
            for j in range(q):
                x = self.g ** Zp_multiply(self.Z[i], self.Z[j], self.p)

        self.pp = {"g": self.g, "H": self.H, "H2": self.H2}


    def commit(self, messages: list[int], q: int):
        assert messages.__len__() == q, "Incorrect number of messages to commit.\n"
        C = None
        for i in range(q):
            if C !=None:
                C = C * (self.H[i] ** messages[i])
            else:
                C = messages[i]
                
        return C, messages

    def produce_proof(self, message: int, index: int, auxiliary: list[int], q: int):
        proof = None
        for j in range(q):
            if (j!=index):
                if proof!= None:
                    proof = proof * (self.H2[index][j] ** auxiliary[j])
                else:
                    proof = auxiliary[j]

        return proof

    def verify(self, commitment, message: file, index: int, proof):
        pass

    def update(self, commitment, old_message: file, new_message: file, index: int):
        pass

    def update_proof(self, commitment, old_proof, new_message, index, U):
        pass


# global values
# k, q

