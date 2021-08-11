class MinHeap:
    def __init__(self) -> None:
        self.heap = []
        self.size = 0

    def compareTo(self, that):
        return ((self > that) - (self < that))

    @classmethod
    def compare(cls, a, b):
        return (a > b) - (a < b)

    def size(self):
        return self.size
    
    def isEmpty(self):
        return len(self.heap) == 0
    
    def min(self):
        return self.heap[1]

    def __greater(self, i, j):
        return self.compare(self.heap[i], self.heap[j]) > 0
    
    def __exch(self, i, j):
        swap = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = swap

    def __swim(self, k):
        while (k > 1 and self.__greater(k/2, k)):
            self.exch(k, k/2)
            k = k/2
    
    def __sink(self, k):
        while 2*k <= self.size:
            j = 2*k - 1 
            if j < self.size and self.__greater(j, j+1):
                j +=1
            if not self.__greater(k, j): 
                break
            self.__exch(k,j)
            k = j

    def delete_min(self):
        if self.isEmpty(): raise ValueError('Priority queue underflow')
        min = self.heap[1]
        self.__exch(1, self.size-1)
        self.__sink(1)
        self.heap[self.size+1] = None
        if self.size > 0 and self.size == (len(self.heap) - 1) / 4:
            self.__resize(len(self.heap) / 2)
        return min

    def __resize(self, capacity):
        temp = capacity * [None]
        for i in range(1, self.size):
            temp[i] = self.heap[i]

        self.heap = temp

    def insert(self, x):
        if (self.size == len(self.heap) - 1): 
            self.__resize(2 * len(self.heap))
        self.size += 1 
        self.heap[self.size] = x
        self.__swim(self.size)

    def print_heap(self):
        for val in self.heap:
            print(val, sep=' ', end=' ', flush=True)
        print("\n")


    def min_pq(self, keys):
        n = len(keys)  

        self.size = len(keys) + 1
        self.heap.append(0)

        for i in range(n):
            self.heap.append(keys[i])

        for k in range(int(n/2), 0, -1):
            self.__sink(k)

# keys = ['f', 'e', 'z', 'd', 'q', 'w', 'j', 'a', 'x', 'b']
# # keys = [35, 33, 42, 10, 14, 19, 27, 44, 26, 31]

# min_heap = MinHeap()
# min_heap.min_pq(keys)
# print("Min: " + str(min_heap.min()))


