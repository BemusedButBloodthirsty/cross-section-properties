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
- Supports adding circular holes to any polygon geometry using the Triangle module.

Planned features:
- Product of inertia,
- Radius of gyration,
- Polar moment of inertia,
- Moment of inertia about any axis specified (including inclined axes).

How to use:
1. Simply change the `pts` list by adding the coordinates which define the outer boundary of the cross-section. The `segments` list required for input in the `Triangle.triangulate()` function is generated automatically based on your `pts` list.
2. If a circular hole is to be added, the function `addCircularHole(centre, r, n)` can be called (see code for details on parameter input).

Issues:
- The moment of inertia results are only approximate. It's recommended to use a sufficient amount of triangles for useful results.

Other comments:	
- If the code can be improved or expanded upon, I would highly appreciate it. This code (at its current state) primarily serves as a double-check to hand calculations.
