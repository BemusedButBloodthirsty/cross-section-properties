from section import CrossSection


# Create a new cross-section:
# ---------------------------------
points = [ 
    # Specify the points of the outer boundary of the cross-section, 
    # listed either in the clockwise or counterclockwise direction.
    [0,0],
    [0,1],
    [1,1],
    [1,0]
]
cs = CrossSection(points)


# Add optional holes to the cross-section:
# ---------------------------------------
# cs.AddCircularHole(
#   centre=[0.5,0.5], 
#   r=0.2, 
#   n=50
# )
#
cs.AddRectangularHole(
  centre=[0.5,0.5], 
  height=0.25, 
  width=0.75
)
# 
# cs.AddCustomHole(
#   inside_point=[0.5,0.5], 
#   hole_points=[[0.1,0.1],[0.5,0.9],[0.9,0.1]]
# )


# Yout can change the element area of each triangle:
# -------------------------------------------------
# cs.ChangeElementArea(0.01)


# Plot the triangulated mesh:
# --------------------------
cs.Plot()


# Calculate the properties:
# ------------------------
print("Area:", cs.Area())
print("Centroid (X, Y):", cs.Centroid())
print("Moment of Inertia (XX, YY, XY):", cs.MomentOfInertia())
print("Moment of area: (Q top, Q bot, Clamped):", cs.MomentOfArea(y=0, plot_mesh=True))
