from random import randint
import json
import math



def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

with open("random_numbers.txt", mode='w', encoding='utf-8') as f:
    json.dump({}, f)

for i in range(200):
    if i == 0:
        continue
    prime1 = randint(1<<i-1, 1<<i)
    while not is_prime(prime1):
        prime1 = randint(1<<i-1, 1<<i)
    prime2 = randint(1<<i-1, 1<<i)
    while not is_prime(prime2):
        prime2 = randint(1<<i-1, 1<<i)
    with open("random_numbers.txt") as f:
        data = json.load(f)
        # data.append(prime)
        data[i] = {'number1': prime1, 'number2': prime2}
    with open("random_numbers.txt", mode='w', encoding='utf-8') as f:
        json.dump(data, f)
