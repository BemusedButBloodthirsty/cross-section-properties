# moment-of-inertia
## Python script that calculates the moment of inertia (second moment of area) of a section about its centroid.

The basic concept is to triangulate the complex region using the Triangle module and to then determine the moment of inertia of each triangle, with the final result simply being the summation of the MOI's of all triangles.

Required modules:
- triangle -> (https://rufat.be/triangle/installing.html) or (https://github.com/drufat/triangle)
- numpy
- matplotlib

Issues:
- The moment of inertia results are only approximate. It's recommended to use a sufficient amount of triangles for useful results.

Comments for the people of the internet:	
- If you can make it better in anyway, I would highly appreciate it. This code (at its current state) primarily serves as a double check to hand-calculations.
