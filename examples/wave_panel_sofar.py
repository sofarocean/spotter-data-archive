#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
wave_panel_sofar.py

VERSION AND LAST UPDATE:
 v1.0  09/12/2024

PURPOSE:
 This program reads a pickle file (.pkl) containing Sofar buoy data and 
 generates a panel with: (1) position of the drifting buoy; (2) power
 spectrum; (3) directional spectrum; (4) time series of significant wave
 height (Hs); (5) time series of wave period, including both peak and mean
 periods; (6) time series of wave direction, including both peak and mean.

USAGE:
 The script generates multiple plots for each time, for one specific buoy.
 Two arguments are requested, the file name, and buoy ID.
 Uncomment the line matplotlib.use('Agg') below if you don't want to have 
 each plot being displayed (runs faster).

 Example (from linux terminal command line):
  python3 wave_panel_sofar.py spotters.pkl 010349
  nohup python3 wave_panel_sofar.py campos_hurricane_spotters_2022_spectra_with_direction_coefficients.pkl 010349 >> nohup_panel_sofar_010349.out 2>&1 &

OUTPUT:
 .png figures, one for each time.
 Name format SofarPanel_ID_YYYYMMDDHH.png
 for example, SofarPanel_SPOT010349_2023091308.png

DEPENDENCIES:
 See the imports below.

AUTHOR and DATE:
 09/12/2024: Ricardo M. Campos, first version.

PERSON OF CONTACT:
 Ricardo M Campos: ricardo.campos@noaa.gov

"""

import matplotlib
# matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
import cartopy.crs as ccrs
import cartopy
from matplotlib import ticker
import matplotlib.colors as colors
import pickle
import warnings; warnings.filterwarnings("ignore")
palette = plt.cm.jet
dpalette = plt.cm.RdBu_r

fname = str(sys.argv[1]) # fname = 'campos_hurricane_spotters_2022_spectra_with_direction_coefficients.pkl'
bid = str(sys.argv[2]) # bid = '010349' bid = '010445'

with open(fname, "rb") as handle:
    data_dictionary = pickle.load(handle)

sids = np.array(list(data_dictionary.keys())).astype('str')

ind = np.where(sids == "SPOT-"+bid)
if np.size(ind)>0:
    ind=int(ind[0][0])

# Read buoy data
print("  "); print(" ================== ")
print(sids[ind])

# Sofar buoy dictionary
sdf = data_dictionary[sids[ind]]

# Process time.
bdate = pd.to_datetime(sdf['time'])
btime = ((bdate - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')).to_numpy()

# Position
blat = np.array(sdf['latitude'][:]).astype('float')
blon = np.array(sdf['longitude'][:]).astype('float')

# Parameters
bhs = np.array(sdf['significantWaveHeight']).astype('float')
btp = np.array(sdf['peakPeriod']).astype('float')
btm = np.array(sdf['meanPeriod']).astype('float')
bdm = np.array(sdf['meanDirection']).astype('float')
bdp = np.array(sdf['peakDirection']).astype('float')

# Spectrum
# Frequency array and Power spectrum
freq = np.array(sdf['frequency']); pspec = np.array(sdf['e'])
# Fourier components
a1 = np.array(sdf['a1']); b1 = np.array(sdf['b1'])
a2 = np.array(sdf['a2']); b2 = np.array(sdf['b2'])

# Directional Spectra
theta = np.linspace(0, 2 * np.pi, 360)
dirspec = np.zeros((len(btime), len(freq), len(theta)))
for t in range(0,len(btime)):
    for j in range(len(freq)):
        D = (1 + a1[t,j] * np.cos(theta) + b1[t,j] * np.sin(theta) +
            a2[t,j] * np.cos(2 * theta) + b2[t,j] * np.sin(2 * theta)) / (2 * np.pi)

        dirspec[t,j,:] = pspec[t,j] * D
        del D

theta = np.linspace(0, 360, 360) # degrees
del ind

# FIGURES ----------------
# lowest period (upper limit frequency) for the dir spectra (2D) polat plot and power spectra
lper=3.5; lperps=2.5
dtp = 200

# for the 2D polar plot:
indf=int(np.where(abs(freq-(1/lper))==min(abs(freq-(1/lper))))[0][0])
indfps=int(np.where(abs(freq-(1/lperps))==min(abs(freq-(1/lperps))))[0][0])
ndire=np.zeros((theta.shape[0]+2),'f'); ndire[1:-1]=theta[:]; ndire[0]=0; ndire[-1]=360
angle = np.radians(ndire)
r, theta = np.meshgrid(freq[0:indf], angle)
# ----------------------------------------

dlevels = np.linspace(-0.2,0.2,101); dlevelsp = np.linspace(0.,10.,101)

ind = np.where(bhs>0.0)
if np.size(ind)>0:
    ind=np.array(ind[0]).astype('int')

btime = btime[ind]; bdate = bdate[ind]
blat = blat[ind]; blon = blon[ind]
pspec = pspec[ind,:]; dirspec = dirspec[ind,:,:]
bhs = bhs[ind]
btp = btp[ind]; btm = btm[ind]
bdm = bdm[ind]; bdp = bdp[ind]

# for t in range(3300,len(btime),6):
for t in range(0,len(btime)):

    # Plot
    fig, axs = plt.subplots(nrows=2,ncols=3,subplot_kw={'projection': ccrs.PlateCarree()},figsize=(19,11))
    # Buoy position
    axs[0,0].set_extent([blon.min()-1,blon.max()+1,blat.min()-1,blat.max()+1], crs=ccrs.PlateCarree())  
    gl = axs[0,0].gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5, color='grey', alpha=0.5, linestyle='--')
    gl.xlabel_style = {'size': 9, 'color': 'k','rotation':0}; gl.ylabel_style = {'size': 9, 'color': 'k','rotation':0}
    gl.ylabels_right = False; gl.xlabels_top = False
    axs[0,0].add_feature(cartopy.feature.OCEAN,facecolor=("white"))
    axs[0,0].add_feature(cartopy.feature.LAND,facecolor=("lightgrey"), edgecolor='grey',linewidth=0.5)
    axs[0,0].add_feature(cartopy.feature.BORDERS, edgecolor='grey', linestyle='-',linewidth=0.5, alpha=1)
    axs[0,0].coastlines(resolution='110m', color='grey',linewidth=0.5, linestyle='-', alpha=1)
    axs[0,1].remove(); axs[0,2].remove()
    axs[1,0].remove(); axs[1,1].remove(); axs[1,2].remove()

    # buoy position
    axs[0, 0].plot(blon, blat, marker='o', color='lightblue', markersize=6, zorder=3)
    axs[0, 0].plot(blon[t], blat[t], marker='o', color='navy', markersize=6, zorder=3)
    axs[0,0].set_title(pd.to_datetime(bdate[t]).strftime('%Y/%m/%d %H')+'Z') 

    # Power Spectra
    axs[0,1] = fig.add_subplot(2, 3, 2, projection='rectilinear')
    axs[0,1].plot(freq[0:indfps],pspec[t,0:indfps], color='k', linestyle='-',linewidth=2.0, zorder=3)
    axs[0,1].fill_between(freq[0:indfps], 0.,pspec[t,0:indfps], color='silver', alpha=0.7, zorder=1)
    axs[0,1].grid(linewidth=0.5, color='grey', alpha=0.5, linestyle='--', zorder=1)
    axs[0,1].set_xlabel('Frequency (Hz)', fontsize=12); axs[0,1].set_ylabel('Power Spectrum (m$^2$/Hz)', fontsize=12) 
    axs[0,1].set_ylim(ymin = -0.001)
    axs[0,1].axis('tight')

    # Dir Wave Spectra -----------------
    slevels = np.unique(np.linspace(0.1,np.nanpercentile(dirspec[t,:,:],99.99),201))

    axs[0,2] = fig.add_subplot(2, 3, 3, projection='polar')
    axs[0,2].set_theta_zero_location('N')
    axs[0,2].set_theta_direction(-1)
    axs[0,2].set_rlabel_position(-135)
    axs[0,2].set_rticks([0.1,0.15,0.20,0.25,0.3]); axs[0,2].set_rmax(1/lper)

    ndspec=np.zeros((len(freq),len(theta)),'f')
    ndspec[:,1:-1]=dirspec[t,:,:]
    for i in range(0,len(freq)):
        ndspec[i,-1]=float((ndspec[i,-2]+ndspec[i,1])/2.)
        ndspec[i,0]=float((ndspec[i,-2]+ndspec[i,1])/2.)

    im = axs[0,2].contourf(theta, r, ndspec[0:indf,:].T,slevels,cmap=plt.cm.gist_stern_r,norm=colors.PowerNorm(gamma=0.5), extend="max")
    # axs[0,1].set_title("SPOT-"+bid+", "+pd.to_datetime(bdate[t]).strftime('%Y/%m/%d %H')+"Z",size=11) 
    cax = axs[0,2].inset_axes([1.13, 0.2, 0.05, 0.6], transform=axs[0,2].transAxes)
    cbar = plt.colorbar(im, ax=axs[0,1], cax=cax)
    tick_locator = ticker.MaxNLocator(nbins=6); cbar.locator = tick_locator; cbar.update_ticks()
    del im

    # Time-Series -----------------
    tin=t-dtp; tfin=t+dtp
    if tin<0:
        tin=0
    if tfin>=(len(btime)-1):
        tfin=(len(btime)-1)

    # Significant Wave Height
    axs[1,0] = fig.add_subplot(2, 3, 4, projection='rectilinear')
    axs[1,0].plot_date(bdate[tin:tfin],bhs[tin:tfin],color='dimgrey', linestyle='-',marker='',linewidth=2.0, zorder=3)
    axs[1,0].plot_date(bdate[tin:tfin],bhs[tin:tfin],color='k', marker='.',linewidth=2.0, zorder=3)
    axs[1,0].xaxis.set_major_formatter( DateFormatter('%b%d') ); axs[1,0].fmt_xdata = DateFormatter('%b%d')
    axs[1,0].axvline(x=bdate[t],color='grey', zorder=1)
    axs[1,0].grid(linewidth=0.5, color='grey', alpha=0.5, linestyle='--', zorder=1)
    axs[1,0].set_xlabel('Date', fontsize=12); axs[1,0].set_ylabel('Hs (m)', fontsize=12) 
    axs[1,0].axis('tight')
    axs[1,0].set_xlim(bdate[tin:tfin].min(), bdate[tin:tfin].max() )

    # Wave Period
    axs[1,1] = fig.add_subplot(2, 3, 5, projection='rectilinear')
    axs[1,1].plot_date(bdate[tin:tfin],btp[tin:tfin],color='blue', linestyle='-',marker='',label="Tp", linewidth=2.0, zorder=3)
    axs[1,1].plot_date(bdate[tin:tfin],btp[tin:tfin],color='navy', marker='.',linewidth=2.0, zorder=3)
    axs[1,1].plot_date(bdate[tin:tfin],btm[tin:tfin],color='red', linestyle='-',marker='',label="Tm", linewidth=2.0, zorder=3)
    axs[1,1].plot_date(bdate[tin:tfin],btm[tin:tfin],color='firebrick', marker='.',linewidth=2.0, zorder=3)
    axs[1,1].xaxis.set_major_formatter( DateFormatter('%b%d') ); axs[1,1].fmt_xdata = DateFormatter('%b%d')
    axs[1,1].axvline(x=bdate[t],color='grey', zorder=1)
    axs[1,1].grid(linewidth=0.5, color='grey', alpha=0.5, linestyle='--', zorder=1)
    axs[1,1].legend(loc='best', fontsize=9)
    axs[1,1].set_xlabel('Date', fontsize=12); axs[1,1].set_ylabel('Wave Period (s)', fontsize=12) 
    axs[1,1].axis('tight')
    axs[1,1].set_xlim(bdate[tin:tfin].min(), bdate[tin:tfin].max() )

    # Wave Direction
    axs[1,2] = fig.add_subplot(2, 3, 6, projection='rectilinear')
    axs[1,2].plot_date(bdate[tin:tfin],bdp[tin:tfin],color='blue', linestyle='-',marker='',label="Dp", linewidth=2.0, zorder=3)
    axs[1,2].plot_date(bdate[tin:tfin],bdp[tin:tfin],color='navy', marker='.',linewidth=2.0, zorder=3)
    axs[1,2].plot_date(bdate[tin:tfin],bdm[tin:tfin],color='red', linestyle='-',marker='',label="Dm", linewidth=2.0, zorder=3)
    axs[1,2].plot_date(bdate[tin:tfin],bdm[tin:tfin],color='firebrick', marker='.',linewidth=2.0, zorder=3)
    axs[1,2].xaxis.set_major_formatter( DateFormatter('%b%d') ); axs[1,2].fmt_xdata = DateFormatter('%b%d')
    axs[1,2].axvline(x=bdate[t],color='grey', zorder=1)
    axs[1,2].grid(linewidth=0.5, color='grey', alpha=0.5, linestyle='--', zorder=1)
    axs[1,2].legend(loc='best', fontsize=9)
    axs[1,2].set_xlabel('Date', fontsize=12); axs[1,2].set_ylabel('Wave Direction (°)', fontsize=12) 
    axs[1,2].axis('tight')
    axs[1,2].set_xlim(bdate[tin:tfin].min(), bdate[tin:tfin].max() )

    # fig.canvas.draw() # https://github.com/SciTools/cartopy/issues/1207
    fig.tight_layout()

    plt.savefig("SofarPanel_SPOT"+bid+"_"+str(pd.to_datetime(bdate[:][t]).strftime('%Y%m%d%H'))+".png", dpi=200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format='png',transparent=False, pad_inches=0.1)
        
    plt.close('all'); del axs, fig
    print("SofarPanel_SPOT"+bid+"_"+str(pd.to_datetime(bdate[:][t]).strftime('%Y%m%d%H')))


