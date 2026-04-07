from manim import *
import numpy as np

class PolarQuantExplanation(Scene):
    def construct(self):
        # Title
        title = Text("PolarQuant: Polar Coordinate Quantization", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Create Coordinate System (No coordinates to avoid LaTeX)
        plane = ComplexPlane()
        self.play(Create(plane))

        # A random complex point
        z_val = 2 + 1.5j
        point = Dot(plane.n2p(z_val), color=YELLOW)
        label = Text("Point (r, theta)", font_size=24, color=YELLOW).next_to(point, UR)
        
        # Radius and Angle
        radius_line = Line(plane.n2p(0), plane.n2p(z_val), color=WHITE)
        
        self.play(FadeIn(point), Write(label))
        self.play(Create(radius_line))
        self.wait(1)

        # Show Quantization Grid (Polar)
        polar_grid = VGroup()
        for r in [1, 2, 3]:
            polar_grid.add(Circle(radius=r, color=BLUE, stroke_opacity=0.3))
        for a in range(8):
            polar_grid.add(Line(plane.n2p(0), plane.n2p(3 * np.exp(1j * a * PI / 4)), color=BLUE, stroke_opacity=0.3))
        
        self.play(Create(polar_grid))
        self.wait(1)

        # Snap to grid
        quant_z = 2 * np.exp(1j * np.round(np.arctan2(1.5, 2) / (PI / 4)) * (PI / 4))
        quant_point = Dot(plane.n2p(quant_z), color=GREEN)
        
        self.play(Transform(point, quant_point))
        self.play(label.animate.set_color(GREEN))
        self.wait(2)
