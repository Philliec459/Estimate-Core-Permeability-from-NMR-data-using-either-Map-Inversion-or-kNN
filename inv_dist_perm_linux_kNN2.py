# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a script file.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math


# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# # #           
# # #            Read in CMR log data
# # #                   
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

NMR_data = pd.read_csv('CMR.csv')

Dep = NMR_data['DEPTH']
Por = NMR_data['CMRP_3MS']
Cmff = NMR_data['CMFF']
#Bvi  = NMR_data['BVI']


# =============================================================================
# # ===========================================================================
# # #-------------------------------------------------------------------------- 
# # #        Read/Write Reference data (_r) using Excel spreadsheet
# # #        Read in Core and NMR data which has Core Kair and Cpor
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

core_NMR_data = pd.read_csv('RSWC_CMR.csv')
#core_NMR_data = pd.read_csv('RSWC_CMR.csv').to_numpy

# for index, row in core_NMR_data.iterrows():
#     print(row['DEPTH'], row['Kair'], row['Cpor'])


Dep_r = core_NMR_data['DEPTH']
Por_r = core_NMR_data['CMRP_3ms']
Cmff_r = core_NMR_data['CMFF']
Bvi_r = core_NMR_data['BVI']
Kair_r = core_NMR_data['Kair']
Porosity_r = core_NMR_data['Cpor']


# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# ##
# ##            This is the beginnin of Inverse Distance^2 
# ##
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

# Min and Max of Porosity data used in normalization    
Por_max = 0.5
Por_min = 0.0



deptharray = []
permarray  = []
porarray   = []

inv_dist_array = []

distance_knn_array = []


for k in range(0,len(NMR_data) ,1):  

        # Normalize the log data of por and ffi
        por = ((Por[k] -  Por_min)/(Por_max - Por_min))
        ffi = ((Cmff[k] - Por_min)/(Por_max - Por_min))
        


        dist_inv    = []
        dist_phi    = []
        dist_ffi    = []
        Perm_weight = []
        Por_r_norm  = []
        Cmff_r_norm = []

        dist_inv_total = 0
        Perm_total     = 0

        
        # this is the core reference data being used 
        for i in range(0,len(core_NMR_data),1):
                
                # Normalize the core reference data of Por_r and Cmff_r
                Por_r_norm.append((Por_r[i]   -  Por_min)/(Por_max - Por_min))
                Cmff_r_norm.append((Cmff_r[i] -  Por_min)/(Por_max - Por_min))
            
            
                # Compute Euclidian Distance inverse distance
                dist_phi.append(abs(por - Por_r_norm[i]))
                dist_ffi.append(abs(ffi - Cmff_r_norm[i]))
                dist_inv.append(1/(math.sqrt(dist_phi[i]**2 + dist_ffi[i]**2) + 0.0000001))

                # Calculalte inverse distance weights for perm
                Perm_weight.append(dist_inv[i]  * Kair_r[i])

                inv_dist_array.append(dist_inv[i]);  # add items


        # =============================================================================
        ###                    KNN Array
        # # ===========================================================================
        # # #--------------------------------------------------------------------------
                distance_knn_array = [dist_inv, Perm_weight]
        #
        # # #--------------------------------------------------------------------------
        # # ===========================================================================
        # =============================================================================
        xnorm=np.array(Por_r)
        ynorm=np.array(Cmff_r)
        
        
        # =============================================================================
        # # ===========================================================================
        # # #--------------------------------------------------------------------------
        # # #           
        # # #               Transpose and Sort new kNN array
        # # #                   
        # # #--------------------------------------------------------------------------
        # # ===========================================================================
        # =============================================================================
        
        #knn_array = np.transpose array
        knn_array = np.transpose(distance_knn_array)
        
        #matsor x[x[:,column].argsort()[::-1]] and -1 us reverse order
        mat_sort = knn_array[knn_array[:,0].argsort()[::-1]] #firt column reverse sort (-1)
        
        
        # =============================================================================
        # # ===========================================================================
        # # #--------------------------------------------------------------------------
        # # #           
        # # #               Calculate knn Thomeer Parameters
        # # #                   
        # # #--------------------------------------------------------------------------
        # # ===========================================================================
        # =============================================================================

        #------------------------------------------------------------------------------
        #    Number of nearest Neighbors
        #------------------------------------------------------------------------------
        n_neighbors = 3
        #------------------------------------------------------------------------------
        
        dist_inv_total_knn = 0
        Perm_total_knn = 0


        #kNN Estimates for first 3 rows
        
        for i in range(0,n_neighbors,1):
            dist_inv_total_knn = dist_inv_total_knn + mat_sort[i][0]
            Perm_total_knn  = Perm_total_knn + mat_sort[i][1]

        #back to k values and calculate estimations now
        Perm_est_knn  = Perm_total_knn  / dist_inv_total_knn


        deptharray.append(Dep[k]); #add items 
        permarray.append(Perm_est_knn); #add items 


x=np.array(permarray)
y=np.array(deptharray)


plt.figure(figsize=(8,11))    
plt.semilogx(x, y)
plt.semilogx(Kair_r, Dep_r, 'ro')
plt.xlim(0.01, 10000)


plt.gca().invert_yaxis()

plt.title("Permeability Estimation using kNN")
plt.ylabel('Depth (feet)')
plt.xlabel('kNN Estimated Perm')
plt.grid(True)


plt.show()
