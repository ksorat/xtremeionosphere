#Poloidal pressure
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
import lfmViz as lfmv
import h5py

def GetSlice(fIn,nStp,vID="P"):
	with h5py.File(fIn,"r") as f:
		gId = "Step#%d"%(nStp)
		X = f["X"][:].T
		Y = f["Y"][:].T
		Z = f["Z"][:].T
		vStr = gId+"/" + vID
		Q = f[vStr][:].T

	Nk = X.shape[2]
	xx = X[:,:,0]
	yy = Y[:,:,0]
	#Poloidal slices
	kU = Nk/4
	kD = Nk/4 + Nk/2
	vU = Q[:,:,kU].squeeze()
	vD = Q[:,:,kD].squeeze()

	return xx,yy,vU,vD
n1 = 150


fIn = "/glade/u/home/skareem/Work/xTreme/fstQ/msphere.h5"
#fIn = "/Users/soratka1/Work/xtremeionosphere/Data/Quad/msphere.h5"

vID = "P"
vMin = 0
vMax = 100
cMap = "viridis"

figSize = (8,8)

fOut = "xP.png"
figQ = 300


fig = plt.figure(figsize=figSize)
gs = gridspec.GridSpec(1,2,width_ratios=[10,1])
Ax = fig.add_subplot(gs[0,0])
xx,yy,vU,vD = GetSlice(fIn,n1)
Ax.pcolormesh(xx, yy,vU,vmin=vMin,vmax=vMax,cmap=cMap)
Ax.pcolormesh(xx,-yy,vD,vmin=vMin,vmax=vMax,cmap=cMap)
plt.axis('scaled')
Ax.set_xlim([-25,25])
Ax.set_ylim([-40,40])

AxC = fig.add_subplot(gs[0,-1])
vN = mpl.colors.Normalize(vmin=vMin,vmax=vMax)
cb = mpl.colorbar.ColorbarBase(AxC,cmap=cMap,norm=vN,orientation='vertical')

plt.savefig(fOut,dpi=figQ)


