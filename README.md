## cross-section-properties  
Required Python modules:
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
