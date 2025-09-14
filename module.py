# # from OpenGL.GL import *
# # from OpenGL.GLU import *
# # from pygame import *
# # import sys

# # init()
# # display.set_mode((800, 600), DOUBLEBUF | OPENGL)

# # # Setup camera (Perspective)
# # gluPerspective(45, (800/600), 0.1, 50.0)
# # glTranslatef(0.0, 0.0, -5)  # Move camera back

# # def draw_cube():
# #     glBegin(GL_QUADS)
# #     glColor3f(1, 0, 0)
# #     glVertex3f( 1, 1,-1)
# #     glVertex3f(-1, 1,-1)
# #     glVertex3f(-1, 1, 1)
# #     glVertex3f( 1, 1, 1)
# #     # ... các mặt còn lại
# #     glEnd()

# # while True:
# #     for e in event.get():
# #         if e.type == QUIT:
# #             quit()
# #             sys.exit()

# #     glRotatef(6, 0, 0, 0)  # Xoay vật thể
# #     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
# #     draw_cube()
# #     display.flip()
# #     time.wait(10)

# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import random

# arr = [random.randint(1, 50) for _ in range(32)]
# states = []
# MIN_RUN = 8

# def save_state(arr, color="blue"):
#     states.append((arr[:], [color] * len(arr)))

# def insertion_sort(arr, left, right):
#     for i in range(left + 1, right + 1):
#         temp = arr[i]
#         j = i - 1
#         while j >= left and arr[j] > temp:
#             arr[j + 1] = arr[j]
#             j -= 1
#             save_state(arr)
#         arr[j + 1] = temp
#         save_state(arr)

# def merge(arr, l, m, r):
#     left = arr[l:m + 1]
#     right = arr[m + 1:r + 1]
#     i = j = 0
#     k = l
#     while i < len(left) and j < len(right):
#         if left[i] <= right[j]:
#             arr[k] = left[i]
#             i += 1
#         else:
#             arr[k] = right[j]
#             j += 1
#         k += 1
#         save_state(arr, "green")
#     while i < len(left):
#         arr[k] = left[i]
#         i += 1
#         k += 1
#         save_state(arr, "green")
#     while j < len(right):
#         arr[k] = right[j]
#         j += 1
#         k += 1
#         save_state(arr, "green")

# def timsort(arr):
#     n = len(arr)
#     for start in range(0, n, MIN_RUN):
#         end = min(start + MIN_RUN - 1, n - 1)
#         insertion_sort(arr, start, end)
#     size = MIN_RUN
#     while size < n:
#         for left in range(0, n, 2 * size):
#             mid = min(n - 1, left + size - 1)
#             right = min((left + 2 * size - 1), (n - 1))
#             if mid < right:
#                 merge(arr, left, mid, right)
#         size *= 2

# save_state(arr, "red")
# timsort(arr)

# fig, ax = plt.subplots()
# bar_rects = ax.bar(range(len(arr)), states[0][0], color=states[0][1])
# ax.set_ylim(0, max(arr) + 5)
# ax.set_title("TimSort Visualization")

# def animate(i):
#     heights, colors = states[i]
#     for bar, h, c in zip(bar_rects, heights, colors):
#         bar.set_height(h)
#         bar.set_color(c)
#     return bar_rects

# ani = animation.FuncAnimation(fig, animate, frames=len(states), interval=150, blit=True)
# ani.save("timsort_animation.gif", writer='pillow', fps=10)
from random import randint
import time
a= randint(1,101)
print("đang random .....")
time.sleep(2)
print("kết quả: có, dậy sớm đi làm đồ ăn cho anh vớiiii hẹ hẹ :>")