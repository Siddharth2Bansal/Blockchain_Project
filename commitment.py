# CDH Based implementation of Vector Commitment

class file:
    def __init__(self, id, file_name = "default"):
        self.file_name = file_name
        self.id = id

class Commitment:
    def key_gen(self):
        pass

    def commit(self, messages: list[file]):
        pass

    def produce_proof(self, message: file, index: int, auxiliary):
        pass

    def verify(self, commitment, message: file, index: int, proof):
        pass

    def update(self, commitment, old_message: file, new_message: file, index: int):
        pass

    def update_proof(self, commitment, old_proof, new_message, index, U):
        pass


# global values
# k, q