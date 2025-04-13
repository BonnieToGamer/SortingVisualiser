from manim import *
from sortingMethods.insertionSort import InsertionSort
from sortingMethods.heapSort import HeapSort
from indexArrow import IndexArrow
import random

class GenericSort(Scene):   
    def generate_array(self):
        self.element_array = [8, 3, 1, 6, 2, 9, 4, 7, 5, 10]
        self.biggest_element = max(self.element_array)
        self.scale_y = self.biggest_element / self.element_height
        self.mid_index = (len(self.element_array) // 2) / 2

    def construct(self):
        self.element_height = 3
        self.element_width = .4
        self.element_margin = .2

        self.generate_array()

        self.element_rectangles = []
        self.element_texts = []
        
        for i in range(len(self.element_array)):
            element = self.element_array[i]
            element_height = element / self.scale_y
            shift_x = -self.mid_index + (i * (self.element_width + self.element_margin))

            rect = Rectangle(width=self.element_width, height=element_height)
            rect.shift((shift_x * RIGHT) + ((element_height / 2) * UP))

            rect_text = Text(str(element), font_size=12)
            rect_text.shift(rect.get_bottom() + (.15 * UP))

            self.element_rectangles.append(rect)
            self.element_texts.append(rect_text)
        
        self.play(AnimationGroup(*[Create(rect) for rect in self.element_rectangles], lag_ratio=1, run_time=5))
        self.play(AnimationGroup(*[Create(text) for text in self.element_texts], lag_ratio=1, run_time=5))
    
    def credits(self):
        credits = Text("Made by Filip (fihl24)")
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
        
        self.play(Uncreate(text))
        index_j_arrow.un_create(self)
        index_i_arrow.un_create(self)

        super().credits()

class HeapSortScene(GenericSort):
    def construct(self):
        super().construct()

        sorter = HeapSort(self.element_array)
        sorter.run()
        steps = sorter.get_steps()