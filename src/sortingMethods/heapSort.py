from sortRecorder import SortRecorder

class HeapSort(SortRecorder):
    def __init__(self, element_array):
        super().__init__(element_array)
    
    def run(self):
        self._sort()

    def _record_swap(self, index1, index2):
        self.steps.append({"swap": [index1, index2, self.array.copy()]})
        self.array[index1], self.array[index2] = self.array[index2], self.array[index1]
    
    def _record_line(self, index):
        self.steps.append({"line": index})

    def _heapify(self, arr, n, i):
        self._record_line(2)
        largest = i

        self._record_line(3)
        l = i * 2 + 1
        self._record_line(4)
        r = i * 2 + 2

        self._record_line(6)
        if l < n and arr[l] > arr[largest]:
            self._record_line(7)
            largest = l

        self._record_line(9)
        if r < n and arr[r] > arr[largest]:
            self._record_line(10)
            largest = r
        
        self._record_line(12)
        if largest != i:
            self._record_line(13)
            self._record_swap(i, largest)
            self._record_line(14)
            self._heapify(arr, n, largest)

    def _sort(self):
        self._record_line(17)
        n = len(self.array)
        
        self._record_line(19)
        for i in range(n // 2 - 1, -1, -1):
            self._record_line(20)
            self._heapify(self.array, n, i)
        
        self._record_line(22)
        for i in range(n - 1, 0, -1):
            self._record_line(23)
            self._record_swap(0, i)
            self._record_line(24)
            self._heapify(self.array, i, 0)