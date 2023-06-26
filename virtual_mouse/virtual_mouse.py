"""Main module."""
import imgui

import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer

from .opengl_tools import *


class VirtualMouse(object):
    def __init__(self):
        super().__init__()
        self.backgroundColor = (0, 0, 0, 1)
        self.window = impl_glfw_init()
        gl.glClearColor(*self.backgroundColor)
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        self.string = ""
        self.f = 0.5

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            imgui.new_frame()
            imgui.begin("Custom window", True)

            imgui.text("Hello, world!")

            if imgui.button("OK"):
                print(f"String: {self.string}")
                print(f"Float: {self.f}")

            _, self.string = imgui.input_text("A String", self.string, 256)

            _, self.f = imgui.slider_float("float", self.f, 0.25, 1.5)

            imgui.show_test_window()

            imgui.end()

            imgui.render()

            gl.glClearColor(*self.backgroundColor)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()