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

class NodeBST:
    def __init__(self, warung_obj):
        self.warung = warung_obj
        self.left = None
        self.right = None

class BSTHarga:
    def __init__(self):
        self.root = None

    def insert(self, warung_obj):
        if not self.root:
            self.root = NodeBST(warung_obj)
        else:
            self._insert_recursive(self.root, warung_obj)

    def _insert_recursive(self, current, warung_obj):
        if warung_obj.harga < current.warung.harga:
            if current.left is None:
                current.left = NodeBST(warung_obj)
            else:
                self._insert_recursive(current.left, warung_obj)
        else:
            if current.right is None:
                current.right = NodeBST(warung_obj)
            else:
                self._insert_recursive(current.right, warung_obj)

    def cari_di_bawah_harga(self, harga_maks):
        hasil = []
        self._inorder_filter(self.root, harga_maks, hasil)
        return hasil

    def _inorder_filter(self, current, harga_maks, hasil):
        if current:
            self._inorder_filter(current.left, harga_maks, hasil)
            if current.warung.harga <= harga_maks:
                hasil.append(current.warung)
            self._inorder_filter(current.right, harga_maks, hasil)
