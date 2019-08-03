# Gcode Layer Writer

As part of the 3D bioprinting project, this image analysis software was created to augment the capabilities of the bioprinter. It can analyze several images and convert them into a customized gcode coordinate map for the bioprinter’s microprocessor to interpret. A k-nearest neighbor search was implemented for the path planning, resulting in a massive increase in runtime performance when compared against an iterative single pass solution.

![path building demo](/images/pathdemo.gif)

A sample demonstration with the Cal logo. Runtime performance was increased by 186.55%.
