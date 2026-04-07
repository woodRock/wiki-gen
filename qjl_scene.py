from manim import *
import numpy as np

class QJLExplanation(Scene):
    def construct(self):
        # Title
        title = Text("QJL: 1-Bit Quantized JL Transform", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Vector space representation (3D-ish looking 2D)
        vector_label = Text("High-Dim Vector x", font_size=24, color=YELLOW).to_edge(LEFT)
        v = Arrow(ORIGIN, [2, 1, 0], color=YELLOW, buff=0)
        self.play(Create(v), Write(vector_label))
        self.wait(1)

        # Random Projection Hyperplane
        plane_line = Line([-3, 3, 0], [3, -3, 0], color=BLUE)
        plane_label = Text("Random Hyperplane", font_size=24, color=BLUE).next_to(plane_line, UR)
        self.play(Create(plane_line), Write(plane_label))
        self.wait(1)

        # Projection and Sign
        proj_dot = Dot([1, -1, 0], color=RED)
        proj_line = DashedLine(v.get_end(), proj_dot.get_center(), color=RED)
        self.play(Create(proj_line), FadeIn(proj_dot))
        
        sign_label = Text("Sign(Projection)", font_size=32, color=GREEN).next_to(proj_dot, DOWN)
        bits_label = Text("Binary Code: 1 or -1", font_size=32, color=GREEN).to_edge(RIGHT)
        
        self.play(Write(sign_label))
        self.play(ReplacementTransform(sign_label, bits_label))
        self.wait(2)
