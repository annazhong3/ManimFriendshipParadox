# imports

!sudo apt update
!sudo apt install libcairo2-dev ffmpeg \
    texlive texlive-latex-extra texlive-fonts-extra \
    texlive-latex-recommended texlive-science \
    tipa libpango1.0-dev
!pip install manim==0.16.0
!pip install IPython --upgrade

from manim import *

# for rendering
%%manim -qm -v WARNING Friendship

# SCENE 1
class FP(Scene):
    def construct(self):
        
        text = Text("The Friendship Paradox", slant = ITALIC)
        self.play(AddTextLetterByLetter(text, font_size = 36))
        self.play(Uncreate(text))
        

        %%manim -qm LargeTreeGeneration

# SCENE 2
class LargeTreeGeneration(MovingCameraScene):
    
    DEPTH = 4
    CHILDREN_PER_VERTEX = 2
    LAYOUT_CONFIG = {"vertex_spacing": (0.5, 1)}
    VERTEX_CONF = {"radius": 0.15, "color": BLUE_B, "fill_opacity": 1}

    def expand_vertex(self, g, vertex_id: str, depth: int):
         
        new_vertices = [f"{vertex_id}/{i}" for i in range(self.CHILDREN_PER_VERTEX)]
        new_edges = [(vertex_id, child_id) for child_id in new_vertices]
        g.add_edges(
            *new_edges,
            vertex_config=self.VERTEX_CONF,
            positions={
                k: g.vertices[vertex_id].get_center() + 0.1 * DOWN for k in new_vertices
            },
        )
        if depth < self.DEPTH:
            for child_id in new_vertices:
                self.expand_vertex(g, child_id, depth + 1)

        return g

    def construct(self):
        g = Graph(["ROOT"], [], vertex_config=self.VERTEX_CONF)
        g = self.expand_vertex(g, "ROOT", 1)
        self.add(g)

        self.play(
            g.animate.change_layout(
                "tree",
                root_vertex="ROOT",
                layout_config=self.LAYOUT_CONFIG,
            )
        )
        self.play(self.camera.auto_zoom(g, margin=1), run_time=4)

# SCENE 3
import math

%%manim -qm -v WARNING Friendship

class Friendship(MovingCameraScene):
   def construct(self):

     self.camera.frame.save_state()

     # create text that lists the source of our data
     text = Text("Source: Ugander, Johan & Karrer, Brian & Backstrom, Lars & Marlow, Cameron. (2011). The Anatomy of the Facebook Social Graph. arXiv preprint. 1111.4503.", font_size=8).to_edge(DOWN)
     self.add(text)
     
     # set up the coordinate grid
     axes = Axes(
         x_range=[0, 1000, 200],
         y_range=[0, 1000, 200],
         x_axis_config={"numbers_to_include": np.arange(0, 1000, 200)},
         y_axis_config={"numbers_to_include": np.arange(0, 1000, 200)}
     )
     labels = axes.get_axis_labels(x_label="\# Friends You Have", y_label="Average \# Friends Your Friends Have")
     
     # graph our function
     def func(x):
       return 216.27 * math.sqrt(0.014*x + 1.859)
     graph = axes.plot(func, color=MAROON)

     # create dots
     moving_dot = Dot(axes.i2gp(graph.t_min, graph), color=ORANGE)
     dot_1 = Dot(axes.i2gp(graph.t_min, graph))
     dot_2 = Dot(axes.i2gp(graph.t_max, graph))

     # make stuff appear on screen
     # self.wait(3)
     self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))
     self.add(axes, labels, graph, dot_1, dot_2, moving_dot)
     
     def update_curve(mob):
       mob.move_to(moving_dot.get_center())

     self.camera.frame.add_updater(update_curve)
     self.play(MoveAlongPath(moving_dot, graph, rate_func=linear))
     self.camera.frame.remove_updater(update_curve)

     self.play(Restore(self.camera.frame))

     self.wait(3)
