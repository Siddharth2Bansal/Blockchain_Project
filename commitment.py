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

def Zp_inverse(x, p):
    y = pow(x, -1, p)
    return y

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

    def verify(self, commitment, message: int, index: int, proof):
        e1 = get_bilinear_map(proof, self.g)
        temp = commitment*(self.H[index] ** (self.p - message))
        e2 = get_bilinear_map(temp, self.H[index])
        if (e1==e2):
            return 1
        return 0

    def update(self, commitment, old_message: int, new_message: int, index: int):
        temp = self.H[index] ** ((new_message - old_message) % self.p)
        new_commitment = commitment * temp
        U = [old_message, new_message, index]

        return new_commitment, U

    def update_proof(self, old_commitment, old_proof, new_message, j: int, U):
        old_message = U[0]
        i = U[2]
        temp = self.H[i] ** ((new_message - old_message) % self.p)
        new_commitment = old_commitment * temp
        if i!=j:
            new_proof = old_proof * (temp ** self.Z[j])
        else:
            new_proof = old_proof
    
        return new_commitment, new_proof


# global values
# k, q

