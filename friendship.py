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

class FP(Scene):
    def construct(self):

        #SCENE 1
        text = Text("The Friendship Paradox", slant = ITALIC)
        self.play(AddTextLetterByLetter(text, font_size = 36))
        self.play(Uncreate(text))
