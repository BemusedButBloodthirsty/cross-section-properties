# moment-of-inertia
## Python script that calculates the moment of inertia (second moment of area) of a section about its centroid.

The basic concept is to triangulate the complex region using the Triangle module and to then determine the moment of inertia of each triangle, with the final result simply being the summation of the MOI's of all triangles.

Required modules:
- triangle -> https://rufat.be/triangle/installing.html or https://github.com/drufat/triangle
- numpy
- matplotlib

Features:
- Supports adding holes to any polygon geometry using the Triangle module.

Issues:
- The moment of inertia results are only approximate. It's recommended to use a sufficient amount of triangles for useful results.

Other comments:	
- If the code can be improved or expanded upon, I would highly appreciate it. This code (at its current state) primarily serves as a double-check to hand calculations.
