import pyglet
from pyglet import gl

import graphicutils as gu
from app import colors


def draw_lines(vertices):
    pyglet.graphics.draw(
        len(vertices) // 2,
        gl.GL_LINES,
        ('v2f', vertices),
    )


def draw_circle(x, y, r, color, mode=gl.GL_LINE_LOOP, resolution=16):
    gl.glColor4f(*color)
    gu.draw_circle(int(x), int(y), int(r), resolution, mode)


class Render:
    def __init__(self, camera):
        self.camera = camera
    
    def draw_grid(self, x, y):
        cam_x = int(self.camera.centerx)
        cam_y = int(self.camera.centery)
        size = int(30 * self.camera.zoom)
        if size > 0:
            gl.glColor3f(*colors.CONTEXT_GRID_COLOR)
            gu.draw_grid(
                self.camera.w,
                self.camera.h,
                cam_x,
                cam_y,
                size,
                x,
                y
            )

    def draw_axes(self, x, y):
        center_x = self.camera.centerx + x
        center_y = self.camera.centery + y

        gl.glColor3f(1, 0, 0)
        gu.draw_arrow(x + 60, y + 60, 40, 0)
        draw_lines((x, center_y, self.camera.w + x, center_y))

        gl.glColor3f(0, 1, 0)
        gu.draw_arrow(x + 60, y + 60, 0, 40)
        draw_lines((center_x, y, center_x, self.camera.h + y))

    def draw_path(self, obj):
        gl.glColor4f(0.8, 0.8, 0.8, 0.4)
        gl.glBegin(gl.GL_LINES)
        for x, y in obj.path[:100]:
            pos_x = int(x * self.camera.zoom + self.camera.centerx)
            pos_y = int(y * self.camera.zoom + self.camera.centery)
            gl.glVertex2d(pos_x, pos_y)
        gl.glEnd()
    
    def draw_object(self, obj, offset_x, offset_y):
        objx = int(obj.x * self.camera.zoom + self.camera.centerx + offset_x)
        objy = int(obj.y * self.camera.zoom + self.camera.centery + offset_y)
        
        gl.glColor4f(0, 1, 0, 1)
        
        for force in obj.forces:
            if any(force):
                w = int(force[0] * self.camera.zoom)
                h = int(force[1] * self.camera.zoom)
                gu.draw_arrow(objx, objy, w, h)

        gl.glColor4f(0, 0, 1, 1)

        if any(obj.velocity):
            w = int(obj.velocity[0] * self.camera.zoom)
            h = int(obj.velocity[1] * self.camera.zoom)
            gu.draw_arrow(objx, objy, w, h)

        gl.glColor4f(1, 0, 0, 1)

        if any(obj.acceleration):
            w = int(obj.acceleration[0] * self.camera.zoom)
            h = int(obj.acceleration[1] * self.camera.zoom)
            gu.draw_arrow(objx, objy, w, h)
        
        draw_circle(
            objx,
            objy, 
            20 * self.camera.zoom,
            (0.2, 1, 0.2, 0.1),
            mode=gl.GL_POLYGON
        )
        draw_circle(
            objx,
            objy,
            20 * self.camera.zoom,
            (0, 1, 0, 0.5)
        )
