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
