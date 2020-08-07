import numpy as np
import triangle as tr
from matplotlib import pyplot as plt

# ---------------EDIT HERE: (1/2)-------------
pts = [
	[0,0],
	[5.5,0],
	[5.5,0.9],
	[8,0.9],
	[8,1.2],
	[-2.5,1.2],
	[-2.5,0.9],
	[0,0.9]
]
# --------------------------------------------

hls = []
segs = []
for i in range(len(pts)):
	if i == len(pts)-1:
		segs.append([i, 0])
	else:
		segs.append([i, i+1])

def addCircularHole(centre, r=1, n=20):
	"""
	centre: list containing the x and y coordinates of the centre of the circle to be cut out of the section,
	r: radius of the circle, and
	n: number of points which define the circumference of the circle.
	"""

	x0, y0 = centre[0], centre[1]
	circle_pts = [[ x0 + np.cos(2*np.pi/n*x)*r, y0 + np.sin(2*np.pi/n*x)*r ] for x in range(0,n)]
    
	# Generate the segment index list:
	circle_segs = []
	start = len(pts)
	for i in range(n):
		if i == n-1:
			circle_segs.append([start + i, start])
		else:
			circle_segs.append([start + i, start + (i+1)])
	
	pts.extend(circle_pts)
	segs.extend(circle_segs)
	hls.append(centre)
	return None

# ---------------EDIT HERE: (2/2)---------------
addCircularHole([0.92,0.6],     r=0.3, n=100)
addCircularHole([2.14,0.6],     r=0.3, n=100)
addCircularHole([5.5-2.14,0.6], r=0.3, n=100)
addCircularHole([5.5-0.92,0.6], r=0.3, n=100)
# ----------------------------------------------

if len(hls) >  0:
	data_for_triangulation = dict(vertices=pts, segments=segs, holes=hls)
else:
	data_for_triangulation = dict(vertices=pts, segments=segs)

tris = tr.triangulate(data_for_triangulation, opts='qpa0.001')

# Display the data using Matplotlib:
"""
tr.compare(plt, A, tris)
"""
x_vals_plot = [x[0] for x in pts]
y_vals_plot = [x[1] for x in pts]
plt.plot(x_vals_plot, y_vals_plot, '--')
plt.axis('equal')
plt.show()

areas = np.zeros(len(tris['triangles']))
x_centroids = np.zeros(len(areas))
y_centroids = np.zeros(len(areas))

x_coords = []
y_coords = []

for indx, t in enumerate(tris['triangles']):
	tri_points = tris['vertices'][t]
	x1, y1 = tri_points[0][0], tri_points[0][1] 
	x2, y2 = tri_points[1][0], tri_points[1][1]
	x3, y3 = tri_points[2][0], tri_points[2][1]
	x_coords.append([x1, x2, x3])
	y_coords.append([y1, y2, y3])
	areas[indx] = 0.5*((x1*y2 - x2*y1) + (x3*y1 - x1*y3) + (x2*y3 - x3*y2))
	x_centroids[indx] = (x1 + x2 + x3) / 3
	y_centroids[indx] = (y1 + y2 + y3) / 3

section_x_centroid = sum(areas*x_centroids) / sum(areas)
section_y_centroid = sum(areas*y_centroids) / sum(areas)

print("Area of polygon cross-section =", sum(areas))
print("x centroid =", section_x_centroid)
print("y centroid =", section_y_centroid)

# Calculating the moment of inertia of the section:
moi_x = np.zeros(len(areas))
moi_y = np.zeros(len(areas))

for indx, (x, y) in enumerate(zip(x_coords, y_coords)):
	x_max, x_min = max(x), min(x)
	y_max, y_min = max(y), min(y)
	b = abs(x_max - x_min)
	h = abs(y_max - y_min)
	x_sorted = sorted(x)
	a = abs(x_sorted[1] - x_sorted[0])

	moi_x[indx] = b*h**3/36 + areas[indx]*(y_centroids[indx] - section_y_centroid)**2
	moi_y[indx] = (b**3*h - b**2*h*a + b*h*a**2)/36 + areas[indx]*(x_centroids[indx] - section_x_centroid)**2

print("Moment of inertia (x) =", sum(moi_x))
print("Moment of inertia (y) =", sum(moi_y))