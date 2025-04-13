from sortRecorder import SortRecorder

class HeapSort(SortRecorder):
    def __init__(self, element_array):
        super().__init__()
        self.array = element_array.copy()
    
    def run(self):
        self._sort()

    def _record_swap(self, index1, index2):
        self.steps.append({"swap": [index1, index2]})
        self.array[index1], self.array[index2] = self.array[index2], self.array[index1]

    def _heapify(self, arr, n, i):
        largest = i

        l = i * 2 + 1
        r = i * 2 + 2

        if l < n and arr[l] > arr[largest]:
            largest = l
        
        if r < n and arr[r] > arr[largest]:
            largest = r
        
        if largest != i:
            self._record_swap(i, largest)
            self._heapify(arr, n, largest)

    def _sort(self):
        n = len(self.array)
        
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(self.array, n, i)
        
        for i in range(n - 1, 0, -1):
            self._record_swap(0, i)
            self._heapify(self.array, i, 0)