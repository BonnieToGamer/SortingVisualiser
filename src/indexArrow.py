from manim import *

class IndexArrow:
    def __init__(self, text, offset_x = 0, offset_y = 0):
        self.arrow = Arrow()
        self.text = Text(text)
        self.text.font_size = 24
        self.text_offset = 1.5 * DOWN
        self.created = False
        self.offset = (offset_x * RIGHT) + (offset_y * UP)
    
    def create(self, scene):
        scene.play(
            AnimationGroup(
                Create(self.arrow), 
                Create(self.text)
            )
        )
        self.created = True

    def un_create(self, scene: Scene):
        scene.play(
            AnimationGroup(
                Uncreate(self.arrow),
                Uncreate(self.text)
            )
        )

    def move_to(self, scene, rects, index):
        pos_x, pos_y = self._get_arrow_position(rects, index)
        
        if not self.created:
            self.arrow.put_start_and_end_on(pos_x, pos_y)
            self.text.move_to(pos_x * RIGHT + pos_y * UP + self.text_offset)
            self.create(scene)
        else:
            scene.play(
                AnimationGroup(
                    self.arrow.animate.put_start_and_end_on(pos_x, pos_y),
                    self.text.animate.move_to(pos_x * RIGHT + pos_y * UP + self.text_offset)
                )
            )
        
    def _get_arrow_position(self, rects, index, length = 1):
        bottom = rects[index].get_bottom()
        return bottom + (length * DOWN) + self.offset, bottom + self.offset
    