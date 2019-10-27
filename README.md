# Estimate-Core-Permeability-from-NMR-data
Estimate Core-based Permeability from NMR well log data

The objective of this project is to use the map inversion (inverse distance**4) to estimate core-based Permeability from NMR data. The following Cross Plot is made from the NMR Effective Porosity (CMRP_3MS, x-axis) vs. the NMR Free Fluid (CMFF, y-axis).  On the z-axis there are some core Permeability measurements shown as colored dots. This method uses the distribution of these core permeability measurements in our map inversion process to estimate core analysis Permeability.  The NMR data in this instance is being used as a road map to make our permeability estimation.

![TS_Image](NMR.png)

The program used in this instance is inv_dist_perm.py. For this program we read in all of the NMR data from a particular well, read in the reference core data with associated NMR values and then estimate core-based Permeability from the NMR Effective Porosity and Free Fluid over the entire well.  The blue curve below shows the estimated permeability for our subject well. 

![Summary_Image](PermEstimate.png) 
