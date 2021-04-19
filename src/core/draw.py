import math

import pyglet
from pyglet import gl

import graphicutils as gu
from app import colors
from .camera import Camera


def draw_lines(vertices):
    pyglet.graphics.draw(
        len(vertices) // 2,
        gl.GL_LINES,
        ('v2f', vertices),
    )


def draw_circle(x, y, r, color, mode=gl.GL_LINE_LOOP, resolution=32):
    gl.glColor4f(*color)
    gu.draw_circle(int(x), int(y), int(r), resolution, mode)


def draw_grid():
    camera = Camera.get_active()
    size = int(20 * camera.zoom)
    if size > 0:
        gl.glColor3f(*colors.CONTEXT_GRID_COLOR)
        gu.draw_grid(
            camera.w,
            camera.h, 
            int(camera.centerx),
            int(camera.centery),
            size, 
            0,
            0
        )


def draw_axes():
    camera = Camera.get_active()
    center_x = int(camera.centerx)
    center_y = int(camera.centery)
    gl.glColor3f(1, 0, 0)
    gu.draw_arrow(20, 40, 40, 0)
    draw_lines((0, center_y, camera.w, center_y))

    gl.glColor3f(0, 1, 0)
    gu.draw_arrow(20, 40, 0, 40)
    draw_lines((center_x, 0, center_x, camera.h))


def draw_path(obj):
    camera = Camera.get_active()

    gl.glColor4f(1, 0.76, 0.12, 0.8)
    gl.glBegin(gl.GL_LINES)
    for x, y in obj.path[:100]:
        pos_x = int(x * camera.zoom + camera.centerx)
        pos_y = int(y * camera.zoom + camera.centery)
        gl.glVertex2d(pos_x, pos_y)
    gl.glEnd()


def draw_object(obj):
    camera = Camera.get_active()
    
    pos = (obj.position * camera.zoom)
    x = int(pos[0] + camera.centerx)
    y = int(pos[1] + camera.centery)

    gl.glColor4f(0, 1, 0, 1)
    for force in obj.forces:
        if any(force):
            w = int(force[0] * camera.zoom)
            h = int(force[1] * camera.zoom)
            gu.draw_arrow(x, y, w, h)

    gl.glColor4f(0.2, 0.5, 1, 1)
    if any(obj.velocity):
        w = int(obj.velocity[0] * camera.zoom)
        h = int(obj.velocity[1] * camera.zoom)
        gu.draw_arrow(x, y, w, h)

    gl.glColor4f(0.9, 0.29, 0.58, 1)
    if any(obj.acceleration):
        w = int(obj.acceleration[0] * camera.zoom)
        h = int(obj.acceleration[1] * camera.zoom)
        gu.draw_arrow(x, y, w, h)
    
    draw_circle(
        x,
        y, 
        20 * camera.zoom,
        colors.RIGIDBODY_COLOR,
        mode=gl.GL_POLYGON
    )
    draw_circle(
        x,
        y,
        20 * camera.zoom,
        colors.RIGIDBODY_BORDER_COLOR,
    )


def draw_ruler(x1, y1, x2, y2):
    camera = Camera.get_active()

    vx1 = int(x1 * camera.zoom + camera.centerx)
    vy1 = int(y1 * camera.zoom + camera.centery)
    vx2 = int(x2 * camera.zoom + camera.centerx)
    vy2 = int(y2 * camera.zoom + camera.centery)
    
    gl.glColor4f(0.27, 0.63, 0.78, 0.8)
    gu.draw_dashed_line(vx2, vy2, vx1, vy1)
    gu.draw_circle(vx1, vy1, 4, 8, gl.GL_LINE_LOOP)
    gu.draw_circle(vx2, vy2, 4, 8, gl.GL_LINE_LOOP)

    size = math.hypot(x2 - x1, y2 - y1)
    label = pyglet.text.Label(
        font_name='verdana', 
        font_size=12,
        color=(255, 255, 255, 200))
    label.text = f'{size:.2f}m'
    label.x = (vx1 + vx2) // 2
    label.y = (vy1 + vy2) // 2
    label.draw()


def draw_select_area(x1, y1, x2, y2):
    rect = (x1, y1, x2, y1, x2, y2, x1, y2)
    gl.glColor4f(0.1, 0.2, 0.3, 0.2)
    pyglet.graphics.draw(4, gl.GL_QUADS, ('v2f', rect))
    gl.glColor4f(0.3, 0.5, 0.8, 0.5)
    pyglet.graphics.draw(4, gl.GL_LINE_LOOP, ('v2f', rect))