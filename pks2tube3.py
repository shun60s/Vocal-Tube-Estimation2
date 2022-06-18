#coding:utf-8

# A trial transform from peak and drop frequency to tube length and reflection coefficient of two three four tube
# by grid search and scipy's optimize.fmin, downhill simplex algorithm.
#
# This version is using frequency ratio.

import sys
import os
import argparse
import numpy as np
from scipy import signal
from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches


from tube_peak3 import *
from pre_compute3 import *

# Check version
# Python 3.10.4, 64bit on Win32 (Windows 10)
# numpy 1.22.3
# matplotlib  3.5.2
# scipy 1.8.0



def show_figure1(tube, peaks_target, drop_peaks_target, fmin0, LA0):
    # comparison frequency response of tube with target
    
    NUM_TUBE= tube.NUM_TUBE
    
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    plt.title('frequency response: blue tube, green wav: min cost ' + str( round(fmin0,1)) )
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [dB]')
    # tube spectrum
    ax1.semilogy(tube.f, tube.response, 'b', ms=2)
    ax1.semilogy(tube.f[tube.peaks_list] , tube.response[tube.peaks_list], 'ro', ms=3)
    if drop_peaks_target is not None:
        ax1.semilogy(tube.f[tube.drop_peaks_list] , tube.response[tube.drop_peaks_list], 'co', ms=3)
    
    
    xw= 2.0 * np.pi * peaks_target
    ax1.semilogy( peaks_target , tube( LA0, xw_input=xw) , 'x', ms=3)
    
    plt.grid()
    
    ax2 = fig.add_subplot(212)
    if len(LA0) == 8 or len(LA0) == 7:  # X=[L1,L2,L3,L4,A1,A2,A3,A4] or X=[L1,L2,L3,L4,r1,r2,r3]   when four tube model
        L1= LA0[0]
        L2= LA0[1]
        L3= LA0[2]
        L4= LA0[3]
        
        if len(LA0) == 8:
            A1= LA0[4]
            A2= LA0[5]
            A3= LA0[6]
            A4= LA0[7]
        else:
            A1, A2, A3, A4 = get_A1A2A3A4( LA0[4], LA0[5], LA0[6] )
        
        print ('L1,L2,L3,L4', L1, L2, L3, L4)
        print ('A1,A2,A3,A4', A1, A2, A3, A4)
    elif len(LA0) == 6 or len(LA0) == 5:  # X=[L1,L2,L3,A1,A2,A3] or X=[L1,L2,L3,r1,r2]   when three tube model
        L1= LA0[0]
        L2= LA0[1]
        L3= LA0[2]
        L4= 0
        if len(LA0) == 6:
            A1= LA0[3]
            A2= LA0[4]
            A3= LA0[5]
        else:
            A1, A2, A3 = get_A1A2A3( LA0[3], LA0[4] )
        A4=0
        print ('L1,L2,L3', L1, L2, L3)
        print ('A1,A2,A3', A1, A2, A3)
        
        
    elif len(LA0) == 4 or len(LA0) == 3:  # L1,L2,r1 X=[L1,L2,A1,A2] or X=[L1,L2,r1] two tube model
        L1= LA0[0]
        L2= LA0[1]
        L3= 0
        L4= 0
        if len(LA0) == 4:
            A1= LA0[2]
            A2= LA0[3]
        else:
            A1, A2 = get_A1A2( LA0[2] )
        A3=0
        A4=0
        
        print ('L1,L2', L1, L2)
        print ('A1,A2', A1, A2)
        
    ax2.add_patch( patches.Rectangle((0, -0.5* A1), L1, A1, hatch='/', fill=False))
    ax2.add_patch( patches.Rectangle((L1, -0.5* A2), L2, A2, hatch='/', fill=False))
    ax2.add_patch( patches.Rectangle((L1+L2, -0.5* A3), L3, A3, hatch='/', fill=False))
    ax2.add_patch( patches.Rectangle((L1+L2+L3, -0.5* A4), L4, A4, hatch='/', fill=False))
    ax2.set_xlim([0, L1+L2+L3+L4+5])
    ax2.set_ylim([(max(A1,A2,A3,A4)*0.5+5)*-1, max(A1,A2,A3,A4)*0.5+5 ])
    
    
    ax2.set_title('cross-section area')
    plt.xlabel('Length [cm]')
    plt.ylabel('Cross-section area [ratio]')
    plt.grid()
    plt.tight_layout()
    
    plt.show()
    




if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(description='estimation two three four tube model ')
    parser.add_argument('--peaks',  nargs="*",  type=float, help='a list of peak frequency. example --peak 770 1100 or --peak 531 673 815  or --peak 770 1100 2600 3300') 
    args = parser.parse_args()
    
    
    # set expect target value
    if args.peaks is not None:
        if len(args.peaks) == 4:
            peaks_target=np.array(args.peaks)
            NUM_TUBE=4
        elif len(args.peaks) == 3:
            peaks_target=np.array(args.peaks)
            NUM_TUBE=3
        elif len(args.peaks) == 2:
            peaks_target=np.array(args.peaks)
            NUM_TUBE=2
        else:
            print ('error: len(peaks) must be 2 or 3 or 4, due to two three four tube.')
            sys.exit()
        
    else:  # defualt peaks value
        peaks_target=np.array([531,673,815 ])
        NUM_TUBE=3
        
    # instance three tube model
    tube= compute_tube_peak(NUM_TUBE=NUM_TUBE)  #, disp=True)
    # load pre-computed grid data
    path0= 'pks_dpks_stack_tube_use_ratio' + str(NUM_TUBE) + '.npz'
    pc1=pre_comute(tube, path0=path0)
    
    
    # drop_peaks_target=np.array([590,750,1350])
    drop_peaks_target=None 
    
    
    # get minimun cost at grid
    X = pc1.get_min_cost_candidate(peaks_target,drop_peaks_target, symmetry=True, disp=False)
    
    # try to minimize the function
    #   by "fmin" that is minimize the function using the downhill simplex algorithm.
    args1=(peaks_target,drop_peaks_target, -1)
    res_brute = optimize.fmin( tube.calc_cost, X, args=args1, full_output=True, disp=False)
    
    print ( 'min cost %f LA ' % (res_brute[1]) , res_brute[0] ) 
    #print ( 'minimum ', res_brute[0] )  # minimum
    #print ( 'function value ', res_brute[1] )  # function value at minimum
    if res_brute[4] != 0:  # warnflag
        print ('warnflag is not 0')
        
    tube(res_brute[0]) 
    show_figure1(tube, peaks_target, drop_peaks_target, res_brute[1], res_brute[0])
