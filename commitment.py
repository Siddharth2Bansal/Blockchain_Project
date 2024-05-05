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

        self.pp = {"g": self.g, "H": self.H, "H2": self.H2}

    def commit(self, messages: list[int], q: int):
        assert messages.__len__() == q, "Incorrect number of messages to commit.\n"
        C = None
        for i in range(q):
            if C !=None:
                C = C * (self.H[i] ** messages[i])
            else:
                C = self.H[i] ** messages[i]
                
        return C

    def open(self, message, index, auxiliary, q):
        proof = (self.g ** Zp_multiply(self.Z[index], self.Z[index], self.p)) ** (self.p - auxiliary[index])
        arr = range(q)
        for j in arr:
            mult = Zp_multiply(self.Z[index], self.Z[j], self.p)
            proof = proof * (self.g ** Zp_multiply(mult, auxiliary[j], self.p))

        return proof

    def verify(self, commitment, message: int, index: int, proof):
        
        temp = commitment*(self.H[index] ** (self.p - message))
        e2 = get_bilinear_map(temp, self.H[index])
        e1 = get_bilinear_map(proof, self.g)

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

