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
