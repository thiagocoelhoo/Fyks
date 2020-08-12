import pyglet

from graphicutils import graphicutils


def draw_lines(vertices, color):
    pyglet.gl.glColor3f(*color)
    pyglet.graphics.draw(
        len(vertices) // 2,
        pyglet.gl.GL_LINES,
        ('v2f', vertices),
    )


def draw_circle(x, y, r, color, mode=pyglet.gl.GL_LINE_LOOP, resolution=16):
    pyglet.gl.glColor4f(*color)
    graphicutils.draw_circle(int(x), int(y), int(r), resolution, mode)


class Render:
    def __init__(self, camera):
        self.camera = camera
        self.show_vector_mesh = False
    
    def draw_grid(self):
        color = (0.1, 0.1, 0.1)
        cam_x = int(self.camera.centerx)
        cam_y = int(self.camera.centery)
        size = int(20 * self.camera.zoom)
        if size > 0:
            pyglet.gl.glColor3f(*color)
            graphicutils.draw_grid(self.camera.w, self.camera.h, cam_x, cam_y, size)

    def draw_axes(self):
        center_x = self.camera.centerx
        center_y = self.camera.centery

        pyglet.gl.glColor3f(1, 0.2, 0.2)
        graphicutils.draw_arrow(20, 20, 40, 0)
        draw_lines((0, center_y, self.camera.w, center_y), (1, 0.2, 0.2))
        
        pyglet.gl.glColor3f(0.2, 1, 0.2)
        graphicutils.draw_arrow(20, 20, 0, 40)
        draw_lines((center_x, 0, center_x, self.camera.h), (0.2, 1, 0.2))
    
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

    def draw_paths(self, paths):
        color = (0.8, 0.8, 0.8, 0.4)
        for x, y in paths:
            pos_x = int(x * self.camera.zoom + self.camera.centerx)
            pos_y = int(y * self.camera.zoom + self.camera.centery)
            draw_circle(pos_x, pos_y, 3 * self.camera.zoom, color, resolution=5)
    
    def render(self, obj):
        objx = int(obj.x * self.camera.zoom + self.camera.centerx)
        objy = int(obj.y * self.camera.zoom + self.camera.centery)
        
        pyglet.gl.glColor4f(0, 1, 0, 1)
        
        for force in obj.forces:
            if any(force):
                w = int(force[0] * self.camera.zoom)
                h = int(force[1] * self.camera.zoom)
                graphicutils.draw_arrow(objx, objy, w, h)

        pyglet.gl.glColor4f(0, 0, 1, 1)

        if any(obj.velocity):
            w = int(obj.velocity[0] * self.camera.zoom)
            h = int(obj.velocity[1] * self.camera.zoom)
            graphicutils.draw_arrow(objx, objy, w, h)

        pyglet.gl.glColor4f(1, 0, 0, 1)

        if any(obj.acceleration):
            w = int(obj.acceleration[0] * self.camera.zoom)
            h = int(obj.acceleration[1] * self.camera.zoom)
            graphicutils.draw_arrow(objx, objy, w, h)
        
        draw_circle(
            objx,
            objy, 
            20 * self.camera.zoom,
            (0.2, 1, 0.2, 0.3),
            mode=pyglet.gl.GL_POLYGON
        )
        draw_circle(
            objx,
            objy,
            20 * self.camera.zoom,
            (0, 0, 0, 0.5)
        )
