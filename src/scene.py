from manim import *
from sortingMethods.insertionSort import InsertionSort
from sortingMethods.heapSort import HeapSort
from indexArrow import IndexArrow
import random

class GenericSort(Scene):
    def __init__(self, element_height = 3, element_width = .4, element_margin = .2, element_offset = ORIGIN, font_size = 12, element_number_offset = .15):
        super().__init__()
        self.element_height = element_height
        self.element_width = element_width
        self.element_margin = element_margin
        self.element_offset = element_offset
        self.font_size = font_size
        self.element_number_offset = element_number_offset

    def generate_array(self):
        self.element_array = [8, 3, 1, 6, 2, 9, 4, 7, 5, 10]
        self.biggest_element = max(self.element_array)
        self.scale_y = self.biggest_element / self.element_height
        self.mid_index = (len(self.element_array) / 2) / 2

    def construct(self):
        self.generate_array()

        self.element_rectangles = []
        self.element_texts = []
        
        for i in range(len(self.element_array)):
            element = self.element_array[i]
            element_height = element / self.scale_y
            shift_x = -self.mid_index + (i * (self.element_width + self.element_margin))

            rect = Rectangle(width=self.element_width, height=element_height)
            rect.shift((shift_x * RIGHT) + ((element_height / 2) * UP) + self.element_offset)

            rect_text = Text(str(element), font_size=self.font_size)
            rect_text.shift(rect.get_bottom() + (self.element_number_offset * UP))

            self.element_rectangles.append(rect)
            self.element_texts.append(rect_text)
        
        self.play(AnimationGroup(*[Create(rect) for rect in self.element_rectangles], lag_ratio=1, run_time=5))
        self.play(AnimationGroup(*[Create(text) for text in self.element_texts], lag_ratio=1, run_time=5))
    
    def swap_elements(self, index1, index2):
        bottom_x1 = self.element_rectangles[index1].get_x() * RIGHT
        bottom_x2 = self.element_rectangles[index2].get_x() * RIGHT

        index1_rect_pos = bottom_x2 + self.element_rectangles[index1].get_y() * UP
        index2_rect_pos = bottom_x1 + self.element_rectangles[index2].get_y() * UP
        index1_text_pos = self.element_texts[index2].get_x() * RIGHT + self.element_texts[index1].get_y() * UP
        index2_text_pos = self.element_texts[index1].get_x() * RIGHT + self.element_texts[index2].get_y() * UP

        self.play(
            AnimationGroup(
                self.element_rectangles[index1].animate.move_to(index1_rect_pos),
                self.element_rectangles[index2].animate.move_to(index2_rect_pos),
                self.element_texts[index1].animate.move_to(index1_text_pos),
                self.element_texts[index2].animate.move_to(index2_text_pos),
            )
        )

        temp = self.element_rectangles[index1]
        self.element_rectangles[index1] = self.element_rectangles[index2]
        self.element_rectangles[index2] = temp

        temp = self.element_texts[index1]
        self.element_texts[index1] = self.element_texts[index2]
        self.element_texts[index2] = temp

    def get_object_coords(self, object):
        return object.get_x() * RIGHT + object.get_y() * UP

    def credits(self):
        credits = Text("Made by Filip Holmgren (fihl24)")
        credits.font = 16
        credits.move_to(2 * DOWN)

        self.play(Create(credits))
        self.wait(2)
        self.play(Uncreate(credits))

class InsertionSortScene(GenericSort):
    def construct(self):
        super().construct()

        sorter = InsertionSort(self.element_array)
        sorter.run()
        steps = sorter.get_steps()

        index_i_arrow = IndexArrow("i", 0, -.2)
        index_j_arrow = IndexArrow("j", 0, -.2)
        text = None        


        for i in range(len(steps)):
            step = steps[i]

            if "i" in step:
                index_i_arrow.move_to(self, self.element_rectangles, step["i"])
        
            elif "j" in step:
                index_j_arrow.move_to(self, self.element_rectangles, step["j"])
            
            elif "check" in step:
                index_j, key, result1, result2, arr_value = step["check"]
                was_none = False
                if text is not None:
                    self.remove(text)
                else:
                    was_none = True
                
                latex = r"j & \geq 0 \quad \text{(result: }" + str(result1) + r") \\ " + \
                        str(key) + r"& < " + str(arr_value) + r" \quad \text{(result: }" + str(result2) + r")"

                text = MathTex(latex)
                text.font_size = 24
                text.move_to(2 * LEFT + 3.5 * UP)

                if was_none:
                    self.play(Create(text))
                else:
                    self.add(text)
                
                swap_line = ArcBetweenPoints(
                    self.element_rectangles[index_j + 1].get_bottom(),
                    self.element_rectangles[index_j].get_bottom(),
                    angle = -PI / 2
                )
                
                self.play(Create(swap_line))
                self.wait(0.5)
                self.play(Uncreate(swap_line))

            elif "swap" in step:
                index1, index2 = step["swap"]
                self.swap_elements(index1, index2)
        
        self.play(Uncreate(text))
        index_j_arrow.un_create(self)
        index_i_arrow.un_create(self)

        super().credits()

class HeapSortScene(GenericSort):
    def __init__(self):
        super().__init__(1.5, 0.2, .1, 2 * LEFT + 2 * UP, 10, .1)
        self.created_heap = False
        self.heap = []

    def create_heap(self, arr):
        if self.created_heap:
            return

        self.heap = [None] * len(arr) * 4
        offset = 2 * UP + RIGHT * 2
        draw_i = 0
        
        def add_heap_obj(i, x, y):
            nonlocal draw_i
            
            circle = Circle(.2, WHITE)
            circle.shift(x * RIGHT * 1.2 + y * DOWN + offset)

            text = Text(str(arr[i]), font_size=10)
            text.shift(x * RIGHT * 1.2 + y * DOWN + offset)

            self.heap[draw_i] = circle
            self.heap[draw_i+1] = text
            draw_i += 4
        
        n = len(arr)
        max_level = int(np.floor(np.log2(n - 1)))
        total_width = (2 ** max_level) * 0.5

        for i in range(n):
            if i == 0:
                level = 0
                index_in_level = 0
                nodes_in_level = 1
            else:
                level = int(np.floor(np.log2(i+1)))
                index_in_level = i - (2 ** level - 1)
                nodes_in_level = 2 ** level

            # compute horizontal spread for this level
            spacing = total_width / (nodes_in_level + 1)
            x = -total_width/2 + (index_in_level + 1) * spacing
            y = level

            add_heap_obj(i, x, y)
        
        draw_i = 0
        for i in range(n // 2):
            left_index = i * 2 + 1
            right_index = i * 2 + 2

            if left_index < n:
                left_node_pos = self.get_object_coords(self.heap[left_index * 4])
                root_node_pos = self.get_object_coords(self.heap[i * 4])
                line_left = Line(root_node_pos + .2 * DOWN, left_node_pos + .2 * UP)
                self.heap[i * 4 + 2] = line_left

            if right_index < n:
                right_node_pos = self.get_object_coords(self.heap[right_index * 4])
                root_node_pos = self.get_object_coords(self.heap[i * 4])
                line_right = Line(root_node_pos + .2 * DOWN, right_node_pos + .2 * UP)
                self.heap[i * 4 + 3] = line_right

        self.play(AnimationGroup(*[Create(heap_obj) for heap_obj in self.heap if heap_obj is not None], lag_ratio=.2, run_time=1))
        self.created_heap = True
    
    def update_heap(self, index1, index2):
        index1 = index1*4+1
        index2 = index2*4+1
        
        index1_heap_pos = self.heap[index1].get_x() * RIGHT + self.heap[index1].get_y() * UP
        index2_heap_pos = self.heap[index2].get_x() * RIGHT + self.heap[index2].get_y() * UP

        self.play(
            AnimationGroup(
                self.heap[index1].animate.move_to(index2_heap_pos),
                self.heap[index2].animate.move_to(index1_heap_pos)
            )
        )

        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def construct(self):
        super().construct()

        sorter = HeapSort(self.element_array)
        sorter.run()
        steps = sorter.get_steps()

        file = open("pseudo_code/heapSort.py")
        pseudo_code = file.read()
        file.close()

        text = Text(pseudo_code, font_size=12)
        text.shift(3 * LEFT + .5 * DOWN)
        self.play(Create(text))

        # line_arrow = Arrow()
        # line_arrow.put_start_and_end_on(4 * LEFT + .5 * DOWN, 3 * LEFT + .5 * DOWN)
        # self.play(Create(line_arrow))

        for i in range(len(steps)):
            step = steps[i]

            if "swap" in step:
                index1, index2, arr = step["swap"]
                self.create_heap(arr)
                self.update_heap(index1, index2)
                self.swap_elements(index1, index2)
        
        self.wait(0.5)
        self.play(Uncreate(text))
        super().credits()