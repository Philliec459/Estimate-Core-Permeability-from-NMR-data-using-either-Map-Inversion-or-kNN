# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script file.
"""

import matplotlib.pyplot as plt
import xlrd
import numpy as np


# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# # #           
# # #            Read in CMR data
# # #                   
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================
#
book = xlrd.open_workbook("CMR.xls")  # Katmai log data
sh = book.sheet_by_index(0)
print(sh.name, sh.nrows, sh.ncols)

import win32com.client

o = win32com.client.Dispatch("Excel.Application")
# o.Visible = 1
# o.Workbooks.Add() 

rows_data = sh.nrows

Dep = []
Por = []
Cmff = []
Bvi = []

print(rows_data)

for i in range(0, rows_data, 1):
    Dep.append(sh.cell_value(rowx=i, colx=0))
    Por.append(sh.cell_value(rowx=i, colx=1))
    Cmff.append(sh.cell_value(rowx=i, colx=2))
    Bvi.append(sh.cell_value(rowx=i, colx=2))
    

# =============================================================================
# # ===========================================================================
# # #-------------------------------------------------------------------------- 
# # #        Read/Write Reference data using Excel spreadsheet
# # #        Read in Core and NMR data which has Core Kair 
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

book = xlrd.open_workbook("RSWC_CMR.xls") 

sh = book.sheet_by_index(0)
print(sh.name, sh.nrows, sh.ncols)
print()

import win32com.client

o = win32com.client.Dispatch("Excel.Application")
o.Visible = 1
o.Workbooks.Add()

Dep_r  = []
Por_r  = []
Cmff_r = []
Bvi_r  = []
Kair_r = []
Porosity_r=[]



for i in range(0, sh.nrows, 1):
    Dep_r.append(sh.cell_value(rowx=i, colx=0))
    Por_r.append(sh.cell_value(rowx=i, colx=1))
    Cmff_r.append(sh.cell_value(rowx=i, colx=2))
    Bvi_r.append(sh.cell_value(rowx=i, colx=3))
    Kair_r.append(sh.cell_value(rowx=i, colx=4))
    Porosity_r.append(sh.cell_value(rowx=i, colx=5))
# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# ##
# ##            This is the beginnin of Inverse Distance^2 
# ##
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================
    
unc_phi=0.01
unc_ffi=0.01


deptharray = []
permarray  = []
porarray   = []

for k in range(0,rows_data ,1):  

        por = Por[k]
        ffi = Cmff[k]
        


        dist_inv    = []
        dist_phi    = []
        dist_ffi    = []
        Perm_weight = []

        dist_inv_total = 0
        Perm_total     = 0

        
        #this is the mapinv_reference_data being used using the mapinv Porosity and Permeability vs. por and perm
        for i in range(0,sh.nrows,1):
                #compute distance and Inverse Distance for por vs Porosity[i] and perm vs Permeability[i]
                dist_phi.append(max(unc_phi,abs(por - Por_r[i])))
                dist_ffi.append(max(unc_ffi,abs(ffi - Cmff_r[i])))



                dist_inv.append(1/(((dist_phi[i]/unc_phi)**4 + (dist_ffi[i]/unc_ffi)**4)))
                dist_inv_total = dist_inv_total +  dist_inv[i]

                
                #calculalte weights for each
                Perm_weight.append(dist_inv[i]  * Kair_r[i])
                
                #now total distance * Weights
                Perm_total  = Perm_total  + Perm_weight[i]


        #calculate estimations 
        Perm_est  =  (Perm_total  / dist_inv_total)
 


        deptharray.append(Dep[k]); #add items 
        permarray.append(Perm_est); #add items 


#------------------------------------------------------------------------------ 
#            Write Data to Spreadsheet
#------------------------------------------------------------------------------
   
#---------------------------------
#                Header
#---------------------------------
    
        o.Cells(2,1).Value = " Depth "    
        o.Cells(2,2).Value = " CMF_3MS "    
        o.Cells(2,3).Value = " CMFF "
        o.Cells(2,4).Value = " Perm_est"   
        
#----------------------------------
#                Data
#----------------------------------
        
        o.Cells(k+3,1).Value = Dep[k]
        o.Cells(k+3,2).Value = por
        o.Cells(k+3,3).Value = ffi
        o.Cells(k+3,4).Value = Perm_est
# 


x=np.array(permarray)
y=np.array(deptharray)


plt.figure(figsize=(8,11))    
plt.semilogx(x, y)

plt.xlim(0.01, 10000)


plt.gca().invert_yaxis()

plt.title("Permeability Estimation Inv Dist**4")
plt.ylabel('Depth (feet)')
plt.xlabel('Estimated Perm')
plt.grid(True)


plt.show()

 
