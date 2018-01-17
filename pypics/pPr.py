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

Ns = [240,492]
#Ns = [16,37]

N = len(Ns)

fIn = "/glade/u/home/skareem/Work/xTreme/fstQ/msphere.h5"
#fIn = "/glade/u/home/skareem/Work/xTreme/try/newQuad/msphere.h5"

#fIn = "/Users/soratka1/Work/xtremeionosphere/Data/Quad/msphere.h5"

vID = "P"
vMin = 0
vMax = 100
xM = 20
yM = 20

cMap = "viridis"

figSize = (8,8)

fOut = "xP.png"
figQ = 300


fig = plt.figure(figsize=figSize)
wR = 10*np.ones(N+1)
wR[-1] = 1
gs = gridspec.GridSpec(1,N+1,width_ratios=wR)
for n in range(N):
	Ax = fig.add_subplot(gs[0,n])
	xx,yy,vU,vD = GetSlice(fIn,Ns[n])
	Ax.pcolormesh(xx, yy,vU,vmin=vMin,vmax=vMax,cmap=cMap)
	Ax.pcolormesh(xx,-yy,vD,vmin=vMin,vmax=vMax,cmap=cMap)
	plt.axis('scaled')
	Ax.set_xlim([-xM,xM])
	Ax.set_ylim([-yM,yM])

AxC = fig.add_subplot(gs[0,-1])
vN = mpl.colors.Normalize(vmin=vMin,vmax=vMax)
cb = mpl.colorbar.ColorbarBase(AxC,cmap=cMap,norm=vN,orientation='vertical')

plt.savefig(fOut,dpi=figQ)

print(Ns)
