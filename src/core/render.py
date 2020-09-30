import pyglet
from pyglet.gl import *

import graphicutils as gu
from app import colors

def draw_lines(vertices, color):
    glColor3f(*color)
    pyglet.graphics.draw(
        len(vertices) // 2,
        GL_LINES,
        ('v2f', vertices),
    )


def draw_circle(x, y, r, color, mode=pyglet.gl.GL_LINE_LOOP, resolution=16):
    glColor4f(*color)
    gu.draw_circle(int(x), int(y), int(r), resolution, mode)


class Render:
    def __init__(self, camera):
        self.camera = camera
        self.show_vector_mesh = False
    
    def draw_grid(self):
        cam_x = int(self.camera.centerx)
        cam_y = int(self.camera.centery)
        size = int(30 * self.camera.zoom)
        if size > 0:
            glColor3f(*colors.CONTEXT_GRID_COLOR)
            gu.draw_grid(self.camera.w, self.camera.h, cam_x, cam_y, size)

    def draw_axes(self):
        center_x = self.camera.centerx
        center_y = self.camera.centery

        glColor3f(1, 0, 0)
        gu.draw_arrow(20, 20, 40, 0)
        draw_lines((0, center_y, self.camera.w, center_y), (1, 0, 0))
        glColor3f(0, 1, 0)
        gu.draw_arrow(20, 20, 0, 40)
        draw_lines((center_x, 0, center_x, self.camera.h), (0, 1, 0))
    
    def draw_vector_mesh(self, mesh):
        if self.show_vector_mesh:
            for x in range(mesh.shape[0]):
                for y in range(mesh.shape[1]):
                    pos = (x * 40, y * 40)
                    ang = get_ang(mesh[x, y, 0], mesh[x, y, 1])
                    i = mesh[x, y, 2]

                    if 100 > i > -100:
                        color = (150, 150, 150)
                    elif i > 100:
                        color = (250, 0, 0)
                    else:
                        color = (0, 0, 255)

                    draw_vector(surface, pos, 50, ang, color)

    def draw_path(self, obj):
        glColor4f(0.8, 0.8, 0.8, 0.4)
        glBegin(GL_LINES)
        for x, y in obj.path[:100]:
            pos_x = int(x * self.camera.zoom + self.camera.centerx)
            pos_y = int(y * self.camera.zoom + self.camera.centery)
            glVertex2d(pos_x, pos_y)
        glEnd()
    
    def render(self, obj):
        objx = int(obj.x * self.camera.zoom + self.camera.centerx)
        objy = int(obj.y * self.camera.zoom + self.camera.centery)
        
        glColor4f(0, 1, 0, 1)
        
        for force in obj.forces:
            if any(force):
                w = int(force[0] * self.camera.zoom)
                h = int(force[1] * self.camera.zoom)
                gu.draw_arrow(objx, objy, w, h)

        glColor4f(0, 0, 1, 1)

        if any(obj.velocity):
            w = int(obj.velocity[0] * self.camera.zoom)
            h = int(obj.velocity[1] * self.camera.zoom)
            gu.draw_arrow(objx, objy, w, h)

        glColor4f(1, 0, 0, 1)

        if any(obj.acceleration):
            w = int(obj.acceleration[0] * self.camera.zoom)
            h = int(obj.acceleration[1] * self.camera.zoom)
            gu.draw_arrow(objx, objy, w, h)
        
        draw_circle(
            objx,
            objy, 
            20 * self.camera.zoom,
            (0.2, 1, 0.2, 0.1),
            mode=GL_POLYGON
        )
        draw_circle(
            objx,
            objy,
            20 * self.camera.zoom,
            (0, 1, 0, 0.5)
        )
