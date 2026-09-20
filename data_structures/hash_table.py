class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return sum(ord(char) for char in key) % self.size

    def insert(self, username, password, role):
        index = self.hash_function(username)

        for item in self.table[index]:
            if item[0] == username:
                item[1] = password
                item[2] = role
                return

        self.table[index].append(
            [username, password, role]
        )

    def search(self, username):
        index = self.hash_function(username)

        for item in self.table[index]:
            if item[0] == username:
                return item

        return None

    def verify_login(self, username, password):
        user = self.search(username)

        if user and user[1] == password:
            return user[2]

        return None