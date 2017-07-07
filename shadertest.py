import glfw
from pygame.locals import *
import pygame
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from sys import getsizeof
import time

def main():
    pygame.init()
    infoObject = pygame.display.Info()

    WIDTH = infoObject.current_w
    HEIGHT = infoObject.current_h
    PHASE = 0

    FPS = 1/60.0
    drawpoint = [WIDTH/2, HEIGHT/2]
    if not glfw.init():
        return

    window = glfw.create_window(WIDTH,HEIGHT, "window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)



    quad = [-1.0,-1.0, 0.0,
            1.0, -1.0, 0.0,
            1.0, 1.0, 0.0,
            -1.0, 1.0, 0.0]

    quad = np.array(quad, dtype = np.float32)

    indices = [0, 1, 2,
                2, 3, 0]

    indices = np.array(indices, dtype = np.uint32)


    vertex_shader = """
    #version 330
    in vec3 position;
    void main(){
        gl_Position = vec4 (position, 1.0f);
    }
    """

    fragment_shader = """
    #version 330

    uniform float pointX;
    uniform float pointY;
    uniform float phase;
    uniform float step;
    void main(){
        vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
        float x = gl_FragCoord.x;
        float y = gl_FragCoord.y;
        float distance = sqrt(pow(x-pointX, 2) + pow(y-pointY, 2));
        float sini = distance*0.01745 - phase;
        float r = sin(sini)*0.5 + 0.25;
        float g = sin(sini + step)*0.5 + 0.25;
        float b = sin(sini + step*2)*0.5 + 0.25;
        color.r = r;
        color.g = g;
        color.b = b;
        gl_FragColor = color;
    }

    """

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)

    glBufferData(GL_ARRAY_BUFFER, getsizeof(quad), quad, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)

    glBufferData(GL_ELEMENT_ARRAY_BUFFER, getsizeof(indices), indices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)


    glUseProgram(shader)

    glUniform1f(glGetUniformLocation(shader, "pointX"), drawpoint[0])
    glUniform1f(glGetUniformLocation(shader, "pointY"), drawpoint[1])
    glUniform1f(glGetUniformLocation(shader, "phase"), PHASE)
    glUniform1f(glGetUniformLocation(shader, "step"), (2*3.14)/3)

    direction = 1
    while not glfw.window_should_close(window):


        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        PHASE = (PHASE + 0.05)%360
        glUniform1f(glGetUniformLocation(shader, "phase"), PHASE)
        time.sleep(FPS)



    glfw.terminate()

if __name__ == "__main__":
    main()
