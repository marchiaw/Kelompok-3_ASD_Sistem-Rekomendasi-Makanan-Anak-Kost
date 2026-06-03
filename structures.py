class Kuliner:
    def __init__(self, nama, harga, kategori):
        self.nama = nama
        self.harga = int(harga)
        self.kategori = kategori

class WarungMakan(Kuliner):
    def __init__(self, nama, harga, kategori, nama_warung, lokasi, rating):
        super().__init__(nama, harga, kategori)
        self.nama_warung = nama_warung
        self.lokasi = lokasi
        self.rating = float(rating)

class NodeLL:
    def __init__(self, data):
        self.data = data
        self.next = None

class QueueHistoryLinkedList:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def add_history_queue(self, item_text):
        new_node = NodeLL(item_text)
        if self.rear is None:
            self.front = self.rear = new_node
            self.size = 1
            return
        self.rear.next = new_node
        self.rear = new_node
        self.size += 1
        if self.size > 5:
            self.dequeue_oldest()

    def dequeue_oldest(self):
        if self.front is None:
            return
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1

    def get_all(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result[::-1]
class StackFavoriteLinkedList:
    def __init__(self):
        self.top = None

    def push(self, item_text):
        new_node = NodeLL(item_text)
        if self.top is None:
            self.top = new_node
        else:
            new_node.next = self.top
            self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        popped_node = self.top
        self.top = self.top.next
        return popped_node.data

    def remove_item(self, item_text):
        current = self.top
        prev = None
        while current:
            if current.data == item_text:
                if prev is None:
                    self.top = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False

    def is_exist(self, item_text):
        current = self.top
        while current:
            if current.data == item_text:
                return True
            current = current.next
        return False

    def get_all(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result
