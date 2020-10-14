import matplotlib.pyplot as plt
from numpy import sin, cos, pi, zeros
import triangle as tr

class CrossSection:

	def __init__(self):
		self.pts = []
		self.segs = []
		self.hls = []
		self.data = None
		self.element_area = 0.001
		self.triangulated = False
		self.tris = None
		self.section_boundary_specified = False
		self.areas = None
		self.x_centroids = None
		self.y_centroids = None
		self.x_coords = None
		self.y_coords = None
		self.moi_x = None
		self.moi_y = None

	def getStatus(self):
		print(self.triangulated)
		print(self.section_boundary_specified)

	def setBoundaryPoints(self, boundary_points):
		if len(boundary_points) > 3:
			self.section_boundary_specified = True
		self.pts.extend(boundary_points)
		self.segs.extend(self.__createSegments(self.pts))

	def getBoundaryPoints(self):
		return self.pts

	def setElementArea(self, area: float):
		self.element_area = area

	def addCustomHole(self, inside_point, hole_points):
		if not self.section_boundary_specified:
			print("Cross section boundary points have not been specified yet. Use the __object__.setBoundaryPoints() method first.")

		if self.triangulated:
			print("Section has already been triangulated. First add all holes before __object__.TriangulateSection() is used.")

		self.pts.extend(hole_points)
		self.segs.extend(self.__createSegments(hole_points))
		self.hls.append(inside_point)

	def addRectangularHole(self, centre, height, width):
		if not self.section_boundary_specified:
			print("Cross section boundary points have not been specified yet. Use the __object__.setBoundaryPoints() method first.")

		if self.triangulated:
			print("Section has already been triangulated. First add all holes before __object__.TriangulateSection() is used.")

		x, y = centre[0], centre[1]

		rectangle_points = [
			[x - width/2, y - height/2],
			[x + width/2, y - height/2],
			[x + width/2, y + height/2],
			[x - width/2, y + height/2]
		]

		self.pts.extend(rectangle_points)
		self.segs.extend(self.__createSegments(rectangle_points))
		self.hls.append(centre)

	def addCircularHole(self, centre, r, n=50):
		"""
		centre: list containing the x and y coordinates of the centre of the circle to be cut out of the section,
		r: radius of the circle, and
		n: number of points which define the circumference of the circle.
		"""
		if not self.section_boundary_specified:
			print("Cross section boundary points have not been specified yet. Use the __object__.setBoundaryPoints() method first.")

		if self.triangulated:
			print("Section has already been triangulated. First add all holes before __object__.TriangulateSection() is used.")

		x0, y0 = centre[0], centre[1]
		circle_pts = [[ x0 + cos(2*pi/n*x)*r, y0 + sin(2*pi/n*x)*r ] for x in range(0,n)]
		self.pts.extend(circle_pts)
		self.segs.extend(self.__createSegments(circle_pts))
		self.hls.append(centre)

	def TriangulateSection(self):
		self.triangulated = True
		if len(self.hls) >  0:
			self.data = dict(vertices=self.pts, segments=self.segs, holes=self.hls)
		else:
			self.data = dict(vertices=self.pts, segments=self.segs)
		self.tris = tr.triangulate(self.data, opts=f"qpa{self.element_area}")
		self.areas = zeros(len(self.tris['triangles']))

	def PlotMesh(self):
		if not self.triangulated:
			print("Mesh for the section has not been triangulated yet. Use the __object__.TriangulateSection() method first.")
		else:
			plt.figure()
			plt.axis('equal')
			plt.triplot(self.tris['vertices'][:, 0], self.tris['vertices'][:, 1], self.tris['triangles'])
			plt.show()

	def __createSegments(self, geom_pts, closed=True):
		segments = []
		start = len(self.segs)
		for i in range(len(geom_pts)):
			if i == len(geom_pts)-1:
				if closed:
					self.segs.append([start + i, start])
			else:
				self.segs.append([start + i, start + (i+1)])
		return segments

	def __create_coords_lists(self):
		self.x_coords = []
		self.y_coords = []

		for indx, t in enumerate(self.tris['triangles']):
			tri_points = self.tris['vertices'][t]
			x1, y1 = tri_points[0][0], tri_points[0][1]
			x2, y2 = tri_points[1][0], tri_points[1][1]
			x3, y3 = tri_points[2][0], tri_points[2][1]
			self.x_coords.append([x1, x2, x3])
			self.y_coords.append([y1, y2, y3])

	def __calculate_tri_areas(self):
		for indx, t in enumerate(self.tris['triangles']):
			tri_points = self.tris['vertices'][t]
			x1, y1 = tri_points[0][0], tri_points[0][1]
			x2, y2 = tri_points[1][0], tri_points[1][1]
			x3, y3 = tri_points[2][0], tri_points[2][1]
			self.areas[indx] = 0.5*((x1*y2 - x2*y1) + (x3*y1 - x1*y3) + (x2*y3 - x3*y2))

	def __calculate_tri_centroids(self):
		self.x_centroids = zeros(len(self.areas))
		self.y_centroids = zeros(len(self.areas))

		for indx, t in enumerate(self.tris['triangles']):
			tri_points = self.tris['vertices'][t]
			x1, y1 = tri_points[0][0], tri_points[0][1]
			x2, y2 = tri_points[1][0], tri_points[1][1]
			x3, y3 = tri_points[2][0], tri_points[2][1]
			self.x_centroids[indx] = (x1 + x2 + x3) / 3
			self.y_centroids[indx] = (y1 + y2 + y3) / 3

	def Area(self):
		if not self.triangulated:
			print("Mesh for the section has not been triangulated yet. Use the __object__.TriangulateSection() method first.")
		self.__calculate_tri_areas()
		return sum(self.areas)

	def Centroid(self):
		if not self.triangulated:
			print("Mesh for the section has not been triangulated yet. Use the __object__.TriangulateSection() method first.")
		self.__calculate_tri_areas()
		self.__calculate_tri_centroids()
		return sum(self.areas*self.x_centroids) / sum(self.areas), sum(self.areas*self.y_centroids) / sum(self.areas)

	def MomentOfInertia(self):
		if not self.triangulated:
			print("Mesh for the section has not been triangulated yet. Use the __object__.TriangulateSection() method first.")

		self.__calculate_tri_areas()
		self.__calculate_tri_centroids()
		self.__create_coords_lists()

		section_x_centroid, section_y_centroid = self.Centroid()

		self.moi_x = zeros(len(self.areas))
		self.moi_y = zeros(len(self.areas))

		for indx, (x, y) in enumerate(zip(self.x_coords, self.y_coords)):
			x_max, x_min = max(x), min(x)
			y_max, y_min = max(y), min(y)
			b = abs(x_max - x_min)
			h = abs(y_max - y_min)
			x_sorted = sorted(x)
			a = abs(x_sorted[1] - x_sorted[0])

			self.moi_x[indx] = b*h**3/36 + self.areas[indx]*(self.y_centroids[indx] - section_y_centroid)**2
			self.moi_y[indx] = (b**3*h - b**2*h*a + b*h*a**2)/36 + self.areas[indx]*(self.x_centroids[indx] - section_x_centroid)**2

		return sum(self.moi_x), sum(self.moi_y)
