from sortRecorder import SortRecorder

class InsertionSort(SortRecorder):
    def __init__(self, element_array):
        super().__init__()
        self.array = element_array.copy()
    
    def run(self):
        self._sort()
    
    def _record_i(self, i):
        self.steps.append({ "i": i })
    
    def _record_j(self, j):
        self.steps.append({ "j": j })
    
    def _record_swap(self, index1, index2):
        self.steps.append({ "swap": [index1, index2] })
        
        temp = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = temp
    
    def _record_comparison(self, j, key):
        self.steps.append({ "check": [j, key, j >= 0, key < self.array[j], self.array[j]] })

    def _sort(self):
        for i in range(1, len(self.array)):
            self._record_i(i)
            key = self.array[i]
            j = i - 1

            self._record_j(j) # small hack :P
            self._record_comparison(j, key)
            while j >= 0 and key < self.array[j]:
                self._record_swap(j + 1, j)
                j -= 1
                if j >= 0: # also hack :)
                    self._record_j(j)
                    self._record_comparison(j, key)
            
            self.array[j + 1] = key