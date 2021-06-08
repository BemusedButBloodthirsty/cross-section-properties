## cross-section-properties  
##### Synopsis:
Structural engineers often need to determine the second moment of area (aka the moment of inertia) for a specific cross-section. 
This is necessary for evaluation of the strains and stresses at the outermost fibres of a structural element or for determining the anticipated deflections during serviceability conditions.

For common shapes such as a rectangular section, the hand-calculation is elementary, even in the case where the transformed section of a reinforced concrete beam needs to be analysed.
However, calculations for more complex shapes (such as T-sections or even triangular sections) are not necessarily difficult to calculate, the process just becomes very cumbersome and tedious especially for a complex reinforced concrete beam that contains many rebars. The odds of making an error in the calculation of the moment of inertia is increased significantly and could result in the overestimation of the design capacity of a structural member (which is not good).

To make this problem much easier to solve, a Python script was made that calculates the second moment of area about the x and y axis (I<sub>x</sub> and I<sub>y</sub>) as well as the product of inertia I<sub>xy</sub> of any polygonal shape. 
The script allows for more complex polygonal shapes with holes (circular, square, or even a custom user-defined shape) to be specified.  

##### Required Python modules:
- triangle: https://rufat.be/triangle/installing.html or https://github.com/drufat/triangle
- numpy
- matplotlib

##### Technical details of the algorithm:
The computation of the moment of inertia is accomplished as follows:
- The polygonal shape defined by the user is triangulated,
- The moment of inertia is calculated on a per-triangle basis according to the following relationships:

<p align="center">
  <img width=400 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/ix_tri.png?raw=true">
</p>

<p align="center">
  <img width=400 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/iy_tri.png?raw=true">
</p>

<p align="center">
  <img width=600 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/ixy_tri.png?raw=true">
</p>

<p align="center">
  <img width=250 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/ai.png?raw=true">
</p>

where x<sub>i</sub> and y<sub>i</sub> denote the i<sup>th</sup> vertex coordinates of the triangle currently being evaluated (n=3). For the unique case where i = n+1, the first vertex is used again.

- It is important to note that the value calculated from the above expressions is with respect to the origin (0,0).
- All triangle moments of inertia are summed to a single value which represents the section as a whole about the origin:

<p align="center">
  <img width=225 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/i00x.png?raw=true">
</p>
<p align="center">
  <img width=225 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/i00y.png?raw=true">
</p>
<p align="center">
  <img width=225 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/i00xy.png?raw=true">
</p>

where j denotes the j<sup>th</sup> triangle and N the total number of triangles from the triangulation process.

- The final moments of inertia about the section centroid are simply determined using the Parallel Axis theorem as follows:

<p align="center">
  <img width=300 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/ix.png?raw=true">
</p>

<p align="center">
  <img width=300 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/Iy.png?raw=true">
</p>

<p align="center">
  <img width=300 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/ixy.png?raw=true">
</p>

<p align="center">
  <img width=200 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/a_sec.png?raw=true">
</p>

where d<sub>x</sub> and d<sub>y</sub> denote the distance from the origin to the x- and y-centroids of the polygonal area respectively.

##### Current features:
- Calculates the area of a polygon cross-section, 
- Calculates the x- and y-centroid coordinates,
- Calculates the moment of inertia about the x- and y-centroid axes (I<sub>x</sub> and I<sub>y</sub> respectively),
- Calculates the product of inertia I<sub>xy</sub>,
- Supports adding holes to the polygon geometry using the Triangle module.
- The polar moment of inertia can simply be calculated from the output of the algorithm:

<p align="center">
  <img width=150 src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/math/j0.png?raw=true">
</p>

##### How to use:
An example of a square section has been defined with a circular hole in the middle:

<p align="center">
  <img width="450" src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/example_section.png?raw=true">
</p> 

- To determine the moments of inertia, see `example.py`.

##### Test case for accuracy evaluation:
The value calculated from this script must be assessed in terms of accuracy.
A simplistic triangular section was chosen. 

<p align="center">
  <img width="350" src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/tri_1.png?raw=true">

  <img width="350" src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/tri_777.png?raw=true">
</p> 

The triangle was triangulated using different values for the element areas (see the `triangle` module's documentation for more information) such that different numbers of individual triangles are obtained. The relative errors for each triangulation were determined and plotted:

<p align="center">
  <img width="450" src="https://github.com/BemusedButBloodthirsty/cross-section-properties/blob/master/images/rel_error.png?raw=true">
</p>

As can be seen, the relative error generally increases for increasing number of triangles due to compounding rounding errors, but the maximum error made is surprisingly small (E-14). 

- See `relative_error_test.py`

##### References:
https://en.wikipedia.org/wiki/Second_moment_of_area
