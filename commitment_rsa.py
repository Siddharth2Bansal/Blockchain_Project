from random import randint
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

class Commitment_RSA:
    def key_gen(self, k, q, l):
        p1 = randint(1<<int(k/2), 1<<(int(k/2)+1))
        p2 = randint(1<<int(k/2), 1<<(int(k/2)+1))
        self.N = p1 * p2
        self.phi_N = (p1 - 1) * (p2 - 1)
        while not is_prime(p1):
            p1 = randint(1<<int(k/2), 1<<(int(k/2)+1))
        while not is_prime(p2):
            p2 = randint(1<<int(k/2), 1<<(int(k/2)+1))
        self.E = []
        for i in range(q):
            e_i = randint(1<<int(l+1), 1<<(int(l+2)))
            while (not is_prime(e_i)) or self.phi_N % e_i == 0:
                e_i = randint(1<<int(l+1), 1<<(int(l+2)))
            self.E.append(e_i)
        self.S = []
        self.a = randint(1, self.N-1)
        for i in range(q):
            power = 1
            for j in range(q):
                if j != i:
                    power = (power * self.E[j]) % self.phi_N
            s_i = pow(self.a, power, self.N)
            self.S.append(s_i)

    def commit(self, messages: list[int], q: int):
        assert messages.__len__() == q, "Incorrect number of messages to commit.\self.self.N"
        C = 1
        for i in range(q):
            C = (C * pow(self.S[i], messages[i], self.N)) % self.N    
        return C

    def produce_proof(self, message, index, auxiliary, q):
        proof = 1
        for i in range(q):
            if i != index:
                proof = (proof * pow(self.S[i], auxiliary[i], self.N)) % self.N
        
        e_i_inverse = pow(self.E[index], -1, self.phi_N)
        proof = pow(proof, e_i_inverse, self.N)
        return proof
    

    def verify(self, commitment, message: int, index: int, proof):
        RHS = pow(proof, self.E[index], self.N)
        RHS = (RHS * pow(self.S[index], message, self.N)) % self.N
        if commitment == RHS:
            return 1
        else:
            return 0
        
    def update(self, commitment, old_message: int, new_message: int, index: int):
        pass

    def update_proof(self, old_commitment, old_proof, new_message, j: int, U):
        pass