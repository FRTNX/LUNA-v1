"""class BinHeap:
    def __init__(self):
    	self.heap_list = [0]
    	self.current_size = 0
    def perc_up(self, i):
        while i // 2 > 0:
            if self.heap_list[i] < self.heap_list[i//2]:
                self.heap_list[i], self.heap_list[i//2] = self.heap_list[i//2], self.heap_list[i]
            i = i // 2
    def insert(self, k):
        self.heap_list.append(k)
        self.current_size += 1
        self.perc_ip(self.current_size)
    def perc_down(self, i):
        while (i * 2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                self.heap_list[i],self.heap_list[mc] = self.heap_list[mc],self.heap_list[i]
            i =mc
    def min_child(self, i):
        if i * 2 + 1 > self.current_size:
            return i * 2
        else:
        	if self.heap_list[i * 2] < self.heap_list[i * 2 + 1]:
                return i * 2
            else:
            	return i * 2 + 1
    def del_min(self):
        ret_val = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size -= 1
        self.heap_list.pop()
        self.perc_down(1)
        return ret_val
    def build_heap(self, a_list):
        i = len(a_list) // 2
        self.current_size = len(a_list)
        self.heap_list = [0] + a_list[:]
        while (i > 0):
            self.perc_down(i)
            i -= 1
"""

class Stack:
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)


