# Verkle Trees: a bandwidth-efficient alternative to Merkle Trees

## Team Members

- Arya Avinash Phadke - 200101020
- Gunjan Dhanuka - 200101038
- Siddharth Bansal - 200101093
- Vani Krishna Barla - 200101101

## Video Link

[Watch our project video here](https://youtu.be/WSSflPblan4)

## Project Details

### Introduction

Verkle Trees, an efficient alternative to Merkle Trees, are introduced to address bandwidth consumption issues associated with the latter.

### Current Usage

Merkle Trees are widely utilized in various network applications such as consensus protocols, public-key directories, cryptocurrencies like Bitcoin, and Secure File Systems for sending membership proofs.

### Drawbacks of Merkle Trees

While effective, Merkle Trees' proofs grow logarithmically with the number of leaves (n), potentially dominating bandwidth consumption in large trees.

### Alternative Considerations

Vector Commitments (VCs) are proposed as a solution due to their constant-sized proofs. However, their construction time complexity (O(n^2)) limits their practicality for many applications.

### Introduction of Verkle Trees

Verkle Trees are introduced as a solution that combines the structure of Merkle Trees with the efficiency of Vector Commitments. Instead of cryptographic hash functions, Verkle Trees use Vector Commitments to construct parent nodes.

### Performance Metrics

A Verkle Tree with a branching factor k offers a construction time complexity of O(kn) and a membership proof-size of O(logkn). This allows for a tradeoff between computational power and bandwidth consumption.

### Bandwidth Reduction

The reduction in bandwidth consumption achieved by Verkle Trees is independent of the tree's depth and solely depends on the chosen branching factor (k).