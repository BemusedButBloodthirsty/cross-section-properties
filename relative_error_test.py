from section import CrossSection
import numpy as np
from matplotlib import pyplot as plt

triangle = [
    [0,0],
    [1,0],
    [0.5,1]
]

cs = CrossSection()
cs.setBoundaryPoints(triangle)

real = 1/36 # The real Ix value for the triangle.

triangle_count = []
relative_errors = []

for el_area in np.linspace(0.00001, 0.1, 1000, endpoint=True):
    cs.setElementArea(el_area)
    cs.TriangulateSection()

    triangle_count.append(len(cs.tris['triangles']))
    relative_errors.append(abs(cs.MomentOfInertia()[0] - real) / real)
    # print(f"Tris = {len(cs.tris['triangles'])}: {cs.MomentOfInertia()[0]}" )

plt.xlabel("Number of triangles")
plt.ylabel("Relative error")
plt.title(f"Max relative error = {max(relative_errors)}")
plt.plot(triangle_count, relative_errors, ".")
plt.show()