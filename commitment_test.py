import commitment
import random
from time import time

def Test(level: int):
    VC = commitment.Commitment()
    q = random.randint(pow(10, level), 9 * pow(10, level))
    # q = 3
    print(q)
    start_time = time()
    VC.key_gen(256, q)
    # debug_1 = VC.g ** VC.p
    # debug2 = debug_1 * VC.g
    # print("hwllo")
    # pass
    end_time = time()
    print("Key Generation Time: ", end_time - start_time)
    messages = [random.randint(0, VC.p-1) for i in range(q)]
    start_time = time()
    C, messages = VC.commit(messages, q)
    indexes_to_sample = random.sample(range(q), min(10, q))
    proofs = {}
    time_for_proofs = {}
    for i in indexes_to_sample:
        
        start_time = time()
        proofs[i] = VC.produce_proof(messages[i], i, messages, q)    
        end_time = time()
        if i in indexes_to_sample:
            time_for_proofs[i] = end_time - start_time
    
    for i in indexes_to_sample:
        assert VC.verify(C, messages[i], i, proofs[i]) == 1, "Verification failed for message: " + str(i)
    print("test case done, moving out.")
for i in range(5):
    Test(i)
    