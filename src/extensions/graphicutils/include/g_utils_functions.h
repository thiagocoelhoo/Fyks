#pragma once

void draw_circle(const int x, const int y, const int r, const int vertices, const int mode);

void draw_grid(const int width, const int height, const int cam_x, const int cam_y, const int size, const int pos_x, const int pos_y);

void draw_arrow(const int x, const int y, const int w, const int h);

void draw_arc(const int x, const int y, const int r, const float start_ang, const float ang, const int vertices);

void draw_rounded_rect(const int x, const int y, const int w, const int h, const int border_radius, const int mode);

void draw_rect(const int x, const int y, const int w, const int h, const int mode);

void draw_dashed_line(const int x1, const int y1, const int x2, const int y2);
