## moment-of-inertia
### Python script that calculates the moment of inertia (second moment of area) of a section about its centroid.

The basic concept is to triangulate the complex region using the Triangle module and to then determine the moment of inertia of each triangle, with the final result simply being the summation of the MOI's of all triangles.

Required modules:
- triangle -> https://rufat.be/triangle/installing.html or https://github.com/drufat/triangle
- numpy
- matplotlib

Current features:
- Calculates the area of a polygon cross-section, 
- Calculates the x- and y-centroid coordinates,
- Calculates the moment of inertia about the x- and y-centroid axes,
- Supports adding holes to the polygon geometry using the Triangle module.

Planned features:
- First moment of area,
- Product of inertia,
- Radius of gyration,
- Polar moment of inertia,
- Moment of inertia about any axis specified (including inclined axes).

How to use:
- See `example.py`.

NOTE:
- The calculated results are only approximate. It's recommended to use a sufficient amount of triangles for useful results.
