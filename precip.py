#Generate precipitation pic
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib as mpl
import lfmViz as lfmv
import mpl_toolkits
from mpl_toolkits.basemap import Basemap

#Convert lon (in degrees) to MLT string
def lon2mlt(lon):
	hrs = np.int(lon/15.0) + 12
	if (hrs>24):
		hrs = hrs-24
	lonStr = "MLT %d:00"%(np.int(hrs))
	return lonStr
fPkl = "Precip.pkl"
fname="precipmap.png"

#Load data from pickle
with open(fPkl,"rb") as f:
	phi = pickle.load(f)
	lam = pickle.load(f)
	TLoss = pickle.load(f)
	K = pickle.load(f)

figSize = (12,4)
dpiQ = 300

HUGE = 1.0e+8
tMin = -60
tMax = 240


Np = 180
Nl = Np/2

I = (TLoss>=tMin) & (TLoss<=tMax)
print("Displaying precipitation for %d particles ..."%(I.sum()))
#vNorm = LogNorm(vmin=1.0e-3,vmax=1.0e-2)
vNorm = mpl.colors.Normalize(vmin=0.,vmax=1.e-3)

#------------
#Rectilinear plot

fig = plt.figure(figsize=figSize)
plt.hist2d(phi[I],lam[I],(Np,Nl),normed=True,norm=vNorm)

plt.xlabel('Phi [deg]')
plt.ylabel("Magnetic Latitude [deg]")
plt.xlim([-180,180])
plt.ylim([0,90])
plt.axis('scaled')
cb = plt.colorbar(orientation='horizontal',fraction=0.1)
cb.set_label("Probability Density")
plt.savefig(fname,dpi=dpiQ)
plt.close('all')
lfmv.trimFig(fname)

#---------------
#Polar plot
figSize = (8,8)
fname = "polarprecip.png"
da = 15.0
vNorm = mpl.colors.Normalize(vmin=0.,vmax=2.5e-3)

fig = plt.figure(figsize=figSize)
lon0 = -90
lat0 = 0.0
latM = 45
Np = 120
Nl = Np/2
pType = 'npstere'
doScl = True
#pType = 'ortho'
m = Basemap(projection=pType,boundinglat=latM,lon_0=lon0,resolution='l')

#Draw lines
LW = 0.5
m.drawparallels(np.arange(0,90,da)  ,color='k',linewidth=LW,labels=[False,False,False,False])
m.drawmeridians(np.arange(-180,181,da),color='k',linewidth=LW,labels=[True,False,False,True],fmt=lon2mlt)

#m.drawmapboundary(fill_color='aqua')

lons = np.linspace(-180,180,Np+1)
lats = np.linspace(0,90,Nl+1)

#Get histogram
H,xe,ye = np.histogram2d(phi[I],lam[I],bins=(lons,lats),normed=True)
lon2D,lat2D = np.meshgrid(lons,lats)

#Scale by surface area, ie cos(lat)
if (doScl):
	for i in range(Nl):
		lat = 0.5*(lats[i]+lats[i+1])*np.pi/180.0
		H[:,i] = H[:,i]/np.cos(lat)

H1 = np.random.rand(Nl,Np)
#m.drawcoastlines(linewidth=0.25,color='silver')
m.pcolormesh(lon2D,lat2D,H.T,latlon=True,norm=vNorm)
m.set_axes_limits()
cb = m.colorbar()

#Label latitudes
Ax = plt.gca()
for ml in np.arange(30,90,da):
	mlStr = r"$%d\degree$"%(ml)
	xy = m(-60,ml)
	Ax.annotate(mlStr,xy=xy,xycoords='data',color='silver')
cb.set_label("Probability Density")
plt.savefig(fname,dpi=dpiQ)
plt.close('all')
lfmv.trimFig(fname)

