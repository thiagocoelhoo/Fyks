#define _USE_MATH_DEFINES
#define MIN(a, b) (((a) < (b)) ? (a) : (b))

#include <iostream>
#include <math.h>

#include <GL/glut.h>

#include "g_utils_functions.h"

using namespace std;

void draw_circle(const int x, const int y, const int r, const int vertices, const int mode)
{
    glBegin(mode);
	for (int i = 0; i < vertices; i++)
	{
        double n = 2 * M_PI * i / vertices;
		glVertex2d(x + r * cos(n), y + r * sin(n));
	}
    glEnd();
}

void draw_grid(const int width, const int height, const int cam_x, const int cam_y, const int size, const int pos_x, const int pos_y)
{   
    // center of the grid coords
    int origin_x = MIN(width, cam_x);
    int origin_y = MIN(height, cam_y);
    int top = pos_y + height;
    int right = pos_x + width;

    glBegin(GL_LINES);
    for (int i = -cam_x / size; i < (width - origin_x) / size; ++i)
    {
        int x = i * size + cam_x;
        glVertex2d(x + pos_x, pos_y);
        glVertex2d(x + pos_x, top);
    }
    
    for (int i = -cam_y / size; i < (height - origin_y) / size; ++i)
    {
        int y = i * size + cam_y;
        glVertex2d(pos_x, y + pos_y);
        glVertex2d(right, y + pos_y);
    }
    glEnd();
}

void draw_arrow(const int x, const int y, const int w, const int h)
{
    double arrow_angle = atan2(h, w);
    int x2 = x + w;
    int y2 = y + h;
    glBegin(GL_LINES);
    
    glVertex2d(x, y);
    glVertex2d(x2, y2);
    
    glVertex2d(x2, y2);
    glVertex2d(x2 - 10 * (cos(arrow_angle) - sin(arrow_angle)), y2 - 10 * (sin(arrow_angle) + cos(arrow_angle)));
    
    glVertex2d(x2, y2);
    glVertex2d(x2 - 10 * (cos(-arrow_angle) - sin(-arrow_angle)), y2 + 10 * (sin(-arrow_angle) + cos(-arrow_angle)));
    
    glEnd();
}

void draw_arc(const int x, const int y, const int r, const float start_ang, const float ang, const int vertices)
{
    for (int i = 0; i < vertices; ++i) 
    {
        float n = start_ang + ang * i / vertices;
        glVertex2d(x + r * cos(n), y + r * sin(n));
    }
}

int main() {
    return 0;
}

void draw_rounded_rect(const int x, const int y, const int w, const int h, const int border_radius, const int mode)
{
    glBegin(mode);
    draw_arc(x + border_radius, y + border_radius, border_radius, M_PI, M_PI_2, 4);
    draw_arc(x + w - border_radius, y + border_radius, border_radius, -M_PI_2, M_PI_2, 4);
    draw_arc(x + w - border_radius, y + h - border_radius, border_radius, 0, M_PI_2, 4);
    draw_arc(x + border_radius, y + h - border_radius, border_radius, M_PI_2, M_PI_2, 4);
    glEnd();
}

void draw_rect(const int x, const int y, const int w, const int h, const int mode)
{
    glBegin(mode);
    glVertex2d(x, y);
    glVertex2d(x + w, y);
    glVertex2d(x + w, y + h);
    glVertex2d(x, y + h);
    glEnd();
}

void draw_dashed_line(const int x1, const int y1, const int x2, const int y2) {
    float width = x2 - x1;
    float height = y2 - y1;
    float size = hypot(width, height);
    float cos = width / size;
    float sin = height / size;
    float x = x1;
    float y = y1;

    glBegin(GL_LINES);
    for (int i = 0; i < size / 8; i++) {
        glVertex2f(x, y);
        x += cos*8;
        y += sin*8;
    }
    glEnd();
}