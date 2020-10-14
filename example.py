from section import CrossSection

# Specify the points of the outer boundary of the cross-section, listed either in the clockwise or counterclockwise direction.
points = [
	[0,0],
    [0,1],
    [1,1],
    [1,0]
]

# Create a new cross-section object:
cs = CrossSection()

# Define the geometry of the cross-section:
cs.setBoundaryPoints(points)
# cs.addCircularHole(centre=[0.5,0.5], r=0.2, n=50)
# cs.addRectangularHole(centre=[0.5,0.5], height=0.25, width=0.75)
# cs.addCustomHole(inside_point=[0.5,0.5], hole_points=[[0.1,0.1],[0.5,0.9],[0.9,0.1]])

# Triangulate the section:
cs.setElementArea(0.01) # NOTE: The smaller the element size, the better the calculated results. Defaults to 0.001 if this line is omitted.
cs.TriangulateSection()

# Plot the mesh:
cs.PlotMesh()

# Calculate the properties:
print("Area:", cs.Area())
print("Centroid (X, Y):", cs.Centroid())
print("Moment of inertia (XX, YY):", cs.MomentOfInertia())
