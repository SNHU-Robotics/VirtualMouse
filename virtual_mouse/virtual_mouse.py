"""Main module."""
import imgui

import glfw
import random
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer

from .opengl_tools import *


class VirtualMouse(object):
    def __init__(self):
        super().__init__()
        self.backgroundColor = (0.2, 0.2, 0.2, 1)
        self.window = impl_glfw_init(window_name="Virtual Mouse")
        gl.glClearColor(*self.backgroundColor)
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        self.string = ""
        self.f = 0.5

        # Robot current position
        self.rpos = [100, 100]

        # Rand maze
        self.maze = Maze()

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            imgui.new_frame()

            # Save and Load Maze
            imgui.begin("Maze Controls", True)

            imgui.text("Hello, world!")

            if imgui.button("OK"):
                print(f"String: {self.string}")
                print(f"Float: {self.f}")

            _, self.string = imgui.input_text("A String", self.string, 256)

            _, self.f = imgui.slider_float("float", self.f, 0.25, 1.5)

            imgui.end()

            self.drawMaze()

            # Render to screen
            imgui.render()

            gl.glClearColor(*self.backgroundColor)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()

    def compute_rel(
        self,
        current_pos,
        start=(0, 0),
        end=(0, 0),
        color=(0.4, 0.4, 0.4, 0.5),
        thick=3,
    ):
        offset = 25  # Global offset

        return (
            current_pos.x + start[0] + offset,
            current_pos.y + start[1] + offset,
            current_pos.x + end[0] + offset,
            current_pos.y + end[1] + offset,
            imgui.get_color_u32_rgba(*color),
            thick,
        )

    def randColor(self):
        if random.randint(0, 1):
            return (0.6, 0.1, 0.1, 0.8)
        else:
            return (0.4, 0.4, 0.4, 0.5)

    def drawMaze(self):
        imgui.begin("Actual Maze", True)  # Create a new imgui box
        cp = imgui.get_window_position()  # Get our current position

        draw_list = imgui.get_window_draw_list()

        # Draw a grid
        mzsz = 600  # overall how many pixels the entire maze is
        gdsize = 16  # how many actual grid squares we need
        dv = mzsz / gdsize  # Division size between blocks

        for col in range(gdsize + 1):
            for i in range(gdsize):
                # Drawing the vertical lines
                draw_list.add_line(
                    *self.compute_rel(
                        cp,
                        (dv * col, dv * i),
                        (dv * col, dv * (i + 1)),
                    ),
                )

            # Drawing the horizontal Lines
            for row in range(gdsize):
                draw_list.add_line(
                    *self.compute_rel(
                        cp,
                        ((row * dv), (col * dv)),
                        (((row + 1) * dv), (col * dv)),
                    )
                )

        # Draw a robot!
        self.rpos[0] = self.rpos[0] + 0.05
        robot_width = 20
        draw_list.add_rect_filled(
            *self.compute_rel(
                cp,
                (self.rpos[0] - robot_width / 2, self.rpos[1] - robot_width / 2),
                (self.rpos[0] + robot_width / 2, self.rpos[1] + robot_width / 2),
                (0.9, 0.9, 0.9, 1),
            )
        )
        draw_list.add_rect_filled(
            *self.compute_rel(
                cp,
                (self.rpos[0] - robot_width / 2, self.rpos[1] - robot_width / 2),
                (self.rpos[0] - robot_width / 4, self.rpos[1] + robot_width / 4),
                (0, 0.9, 0, 1),
            )
        )
        draw_list.add_rect_filled(
            *self.compute_rel(
                cp,
                (
                    self.rpos[0] + robot_width / 4,
                    self.rpos[1] - robot_width / 2,
                ),
                (
                    (self.rpos[0] + robot_width) - robot_width / 2,
                    self.rpos[1] + robot_width / 4,
                ),
                (0.9, 0, 0, 1),
            )
        )

        imgui.end()


class Square:
    def __init__(self):
        self.north = False
        self.south = False
        self.east = False
        self.west = False


class Maze:
    def __init__(self):
        self.data = []

    def generateMaze(self, grid=16):
        """Generate a terrible random maze"""
        for col in range(grid):
            for row in range(grid):
                randSquare = Square()
                randSquare.north = random.randint(0, 1)
                randSquare.south = random.randint(0, 1)
                randSquare.east = random.randint(0, 1)
                randSquare.west = random.randint(0, 1)
                self.data[col][row] = randSquare
