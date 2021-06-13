import matplotlib.pyplot as plt
from numpy import sin, cos, pi, zeros
import triangle as tr

class CrossSection:

	def __init__(self, points_list):
		self.__pts = []
		self.__segs = []
		self.__hls = []
		self.__data = []
		self.__element_area = 10_000 # High as possible number to reduce number of tris.
		self.__tris = []
		# self.__section_boundary_specified = False
		self.__areas = []
		self.__x_centroids = []
		self.__y_centroids = []
		self.__x_coords = []
		self.__y_coords = []
		self.__moi_x = []
		self.__moi_y = []
		self.__moi_xy = []
		self.__tri_q = []

		self.__set_boundary_points(points_list)
		self.__triangulate_section()

	# def GetBoundaryPoints(self):
	# 	return self.__pts

	# def GetStatus(self):
	# 	print(self.__triangulated)
	# 	print(self.__section_boundary_specified)

	def __clamp(self, var, var_min, var_max):
		if var < var_min:
			return var_min, True
		elif var > var_max:
			return var_max, True
		else:
			return var, False


	# def __clear_data(self, ):
	# 	self.__areas = []
	# 	self.__x_centroids = []
	# 	self.__y_centroids = []
	# 	self.__x_coords = []
	# 	self.__y_coords = []
	# 	self.__moi_x = []
	# 	self.__moi_y = []
	# 	self.__moi_xy = []
	# 	return


	def __create_segments(self, geom_pts, closed=True):
		segments = []
		start = len(self.__segs)
		for i in range(len(geom_pts)):
			if i == len(geom_pts)-1:
				if closed:
					self.__segs.append([start + i, start])
			else:
				self.__segs.append([start + i, start + (i+1)])
		return segments


	def __set_boundary_points(self, boundary_points):
		# if len(boundary_points) > 3:
		# 	self.__section_boundary_specified = True
		self.__pts.extend(boundary_points)
		self.__segs.extend(self.__create_segments(self.__pts))
	

	def __triangulate_section(self):
		self.__data = []
		self.__tris = []

		# self.__triangulated = True
		if len(self.__hls) >  0:
			self.__data = dict(vertices=self.__pts, segments=self.__segs, holes=self.__hls)
		else:
			self.__data = dict(vertices=self.__pts, segments=self.__segs)
		self.__tris = tr.triangulate(self.__data, opts=f"qpa{self.__element_area}")
		# self.__areas = zeros(len(self.__tris['triangles']))
	
	
	def __create_coords_lists(self):
		self.__x_coords = []
		self.__y_coords = []
		
		for t in self.__tris['triangles']:
			tri_points = self.__tris['vertices'][t]
			x1, y1 = tri_points[0][0], tri_points[0][1]
			x2, y2 = tri_points[1][0], tri_points[1][1]
			x3, y3 = tri_points[2][0], tri_points[2][1]
			self.__x_coords.append([x1, x2, x3])
			self.__y_coords.append([y1, y2, y3])


	def __calculate_tri_areas(self):
		self.__areas = []
		
		for t in self.__tris['triangles']:
			tri_points = self.__tris['vertices'][t]
			x1, y1 = tri_points[0][0], tri_points[0][1]
			x2, y2 = tri_points[1][0], tri_points[1][1]
			x3, y3 = tri_points[2][0], tri_points[2][1]
			self.__areas.append( 0.5*((x1*y2 - x2*y1) + (x3*y1 - x1*y3) + (x2*y3 - x3*y2)) )


	def __calculate_tri_centroids(self):
		self.__x_centroids = []
		self.__y_centroids = []

		for t in self.__tris['triangles']:
			tri_points = self.__tris['vertices'][t]
			x1, y1 = tri_points[0][0], tri_points[0][1]
			x2, y2 = tri_points[1][0], tri_points[1][1]
			x3, y3 = tri_points[2][0], tri_points[2][1]
			self.__x_centroids.append( (x1 + x2 + x3) / 3 )
			self.__y_centroids.append( (y1 + y2 + y3) / 3 )


	def __tri_moi(self, tri_points):
		"""
		tri_points: List or tuple containing the three (x,y) points of a tri in Cartesian coordinates, listed in the counter-clockwise direction.  
		Returns: Ix, Iy, and Ixy about the origin of the Cartesian axes.
		Units: Specified by units of triangle points.

		Reference: https://en.wikipedia.org/wiki/Second_moment_of_area#Any_cross_section_defined_as_polygon
		"""

		# MOI about the origin:
		# --------------------
		# dx: float = 0
		# dy: float = 0

		Ix_origin:  float = 0
		Iy_origin:  float = 0
		Ixy_origin: float = 0
		for i in range(3): # 3 points of tri.
			# Get the x and y point of the current vertex:
			x_i, x_iplus1 = tri_points[i][0], tri_points[(i+1) % 3][0] # Making sure n+1 = 1.
			y_i, y_iplus1 = tri_points[i][1], tri_points[(i+1) % 3][1]
			
			# # Data for the centroid calculations:
			# dx += x_i
			# dy += y_i 
			
			# Formula for 2x the signed area of the elementary tri: a_i = x_i * y_i+1 - x_i+1 * y_i
			a_i = x_i * y_iplus1 - x_iplus1 * y_i # This is 2x the area of the triangle.

			# Formulas for the individual moments of area:
			Ix_origin  += a_i * (y_i**2 + y_i*y_iplus1 + y_iplus1**2)
			Iy_origin  += a_i * (x_i**2 + x_i*x_iplus1 + x_iplus1**2)
			Ixy_origin += a_i * (x_i*y_iplus1 + 2*x_i*y_i + 2*x_iplus1*y_iplus1 + x_iplus1*y_i)

		# Correcting the moments of area of the tri (about the origin):
		Ix_origin  /= 12
		Iy_origin  /= 12
		Ixy_origin /= 24

		# # Centroid of tri:
		# # ---------------
		# dx /= 3
		# dy /= 3
		# # print(dx, dy)

		# # MOI about the centroid of the tri:
		# # ---------------------------------
		# Ix:  float = 0
		# Iy:  float = 0
		# Ixy: float = 0

		# x_1, x_2, x_3 = tri_points[0][0], tri_points[1][0], tri_points[2][0]
		# y_1, y_2, y_3 = tri_points[0][1], tri_points[1][1], tri_points[2][1]
		# tri_area = abs( 0.5 * ( x_1*(y_2 - y_3) + x_2*(y_3 - y_1) + x_3*(y_1 - y_2) ) )

		# Ix  = Ix_origin  - tri_area * dy**2
		# Iy  = Iy_origin  - tri_area * dx**2
		# Ixy = Ixy_origin - tri_area * dx*dy

		return Ix_origin, Iy_origin, Ixy_origin


	def AddCustomHole(self, inside_point, hole_points):
		# if not self.__section_boundary_specified:
		# 	print("Cross section boundary points have not been specified yet. Use the __object__.setBoundaryPoints() method first.")

		# if self.__triangulated:
		# 	print("Section has already been triangulated. First add all holes before __object__.TriangulateSection() is used.")

		self.__pts.extend(hole_points)
		self.__segs.extend(self.__create_segments(hole_points))
		self.__hls.append(inside_point)
		self.__triangulate_section()


	def AddRectangularHole(self, centre, height, width):
		# if not self.__section_boundary_specified:
		# 	print("Cross section boundary points have not been specified yet. Use the __object__.setBoundaryPoints() method first.")

		# if self.__triangulated:
		# 	print("Section has already been triangulated. First add all holes before __object__.TriangulateSection() is used.")

		x, y = centre[0], centre[1]

		rectangle_points = [
			[x - width/2, y - height/2],
			[x + width/2, y - height/2],
			[x + width/2, y + height/2],
			[x - width/2, y + height/2]
		]

		self.__pts.extend(rectangle_points)
		self.__segs.extend(self.__create_segments(rectangle_points))
		self.__hls.append(centre)
		self.__triangulate_section()


	def AddCircularHole(self, centre, r, n=50):
		"""
		centre: list containing the x and y coordinates of the centre of the circle to be cut out of the section,
		r: radius of the circle, and
		n: number of points which define the circumference of the circle.
		"""
		# if not self.__section_boundary_specified:
		# 	print("Cross section boundary points have not been specified yet. Use the __object__.setBoundaryPoints() method first.")

		# if self.__triangulated:
		# 	print("Section has already been triangulated. First add all holes before __object__.TriangulateSection() is used.")

		x0, y0 = centre[0], centre[1]
		circle_pts = [[ x0 + cos(2*pi/n*x)*r, y0 + sin(2*pi/n*x)*r ] for x in range(0,n)]
		self.__pts.extend(circle_pts)
		self.__segs.extend(self.__create_segments(circle_pts))
		self.__hls.append(centre)
		self.__triangulate_section()


	def ChangeElementArea(self, area: float):
		self.__element_area = area
		self.__triangulate_section()


	def Plot(self, tris_only=False):
		# if not self.__triangulated:
		# 	print("Mesh for the section has not been triangulated yet. Use the __object__.TriangulateSection() method first.")
		# else:
		if tris_only:
			plt.figure()
			plt.axis('equal')
			plt.triplot(self.__tris['vertices'][:, 0], self.__tris['vertices'][:, 1], self.__tris['triangles'])
			plt.show()
		else:
			tr.compare(plt, self.__data, self.__tris)
			plt.show()

	
	def Area(self):
		# if not self.__triangulated:
		# 	print("Mesh for the section has not been triangulated yet. Use the __object__.TriangulateSection() method first.")
		# self.__clear_data()
		
		self.__calculate_tri_areas()
		return sum(self.__areas)


	def Centroid(self):
		# if not self.__triangulated:
		# 	print("Mesh for the section has not been triangulated yet. Use the __object__.TriangulateSection() method first.")
		# self.__clear_data()
		
		self.__calculate_tri_areas()
		self.__calculate_tri_centroids()

		sum_areas = sum(self.__areas)
		sum_x_centroid_mult_areas = sum([xc * a for xc, a in zip(self.__x_centroids, self.__areas)])
		sum_y_centroid_mult_areas = sum([yc * a for yc, a in zip(self.__y_centroids, self.__areas)])

		return sum_x_centroid_mult_areas / sum_areas, sum_y_centroid_mult_areas / sum_areas


	def MomentOfInertia(self):
		# if not self.__triangulated:
		# 	print("Mesh for the section has not been triangulated yet. Use the __object__.TriangulateSection() method first.")
		self.__moi_x  = []
		self.__moi_y  = []
		self.__moi_xy = []

		self.__create_coords_lists()

		A 	   = self.Area()
		dx, dy = self.Centroid()

		# Sum I for each triangle, about the origin:
		for x, y in zip(self.__x_coords, self.__y_coords):

			# Reformat the list:
			t = [
				[x[0], y[0]],
				[x[1], y[1]],
				[x[2], y[2]]
			]

			Ix_tri, Iy_tri, Ixy_tri = self.__tri_moi(t)

			self.__moi_x.append(Ix_tri)
			self.__moi_y.append(Iy_tri)
			self.__moi_xy.append(Ixy_tri)

		# The I values about the section centroid are given as follows:
		Ix  = sum(self.__moi_x)  - A * dy**2
		Iy  = sum(self.__moi_y)  - A * dx**2
		Ixy = sum(self.__moi_xy) - A * abs(dx)*abs(dy)

		return Ix, Iy, Ixy


	def MomentOfArea(self, y=0, extra_hole=None, plot_mesh=True):
		"""
		y: Distance specified above or below the neutral axis of the section. Clamped to the min and max y-coordinate specified in the boundary points.
		
		Defaults to the centroid if not specified (i.e. maximum moment of area).
		"""
		self.__tri_q_top = []
		self.__tri_q_bot = []

		yc = self.Centroid()[1]
		if y == 0:
			y = yc
		else:
			y += yc

		x_vals = [row[0] for row in self.__pts]
		y_vals = [row[1] for row in self.__pts]

		x_min, x_max = min(x_vals), max(x_vals)
		y_min, y_max = min(y_vals), max(y_vals)

		y, clamped = self.__clamp(y, y_min, y_max) # Restrict the value of the y coordinate to the min/max possible.

		boundary = [[x_min, y], [x_max, y]]

		old_pts = self.__pts.copy()
		old_segs = self.__segs.copy()
		old_hls = self.__hls.copy()

		self.__pts.extend(boundary)
		self.__segs.extend(self.__create_segments(boundary))

		if extra_hole != None:
			self.__hls.append(extra_hole)

		self.__triangulate_section()
		yc = self.Centroid()[1]
		
		if plot_mesh:
			self.Plot()
		# print("Clamped:", clamped)

		# Q = 0
		# Q_top = 0
		# Q_bot = 0
		if not clamped:
			# If the value was clamped, this means that the boundary edges are selected,
			# thus it means that the Q value will be zero.
		
			for tri_area, tri_y_centroid in zip(self.__areas, self.__y_centroids):
				if tri_y_centroid > yc:
					# This can be used to calculate the Q value:
					# self.__tri_q.append( abs(tri_y_centroid - yc) * tri_area )
					self.__tri_q_top.append( abs(tri_y_centroid - yc) * tri_area )

				if tri_y_centroid < yc:
					self.__tri_q_bot.append( abs(tri_y_centroid - yc) * tri_area )

		# Restore the previous triangulation:
		self.__pts = old_pts
		self.__segs = old_segs
		self.__hls = old_hls
		self.__triangulate_section()
		# self.Plot()

		# print("BOOL (E-3):", abs(Q_bot - sum(self.__tri_q)) < 1e-3)

		return sum(self.__tri_q_top), sum(self.__tri_q_bot), clamped	
