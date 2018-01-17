#Poloidal pressure
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec
import lfmViz as lfmv
import h5py

gB0 = 4.58

def GetSlice(fIn,nStp,vID="P"):
	with h5py.File(fIn,"r") as f:
		gId = "Step#%d"%(nStp)
		X = f["X"][:].T
		Y = f["Y"][:].T
		Z = f["Z"][:].T
		vStr = gId+"/" + vID
		Q = f[vStr][:].T
		bZ = f[gId+"/Bz"][:].T
		print("Bz at Sunward boundary = %f nT"%(bZ[-1,0,0]*gB0))
	Nk = X.shape[2]
	xx = X[:,:,0]
	yy = Y[:,:,0]
	#Poloidal slices
	kU = Nk/4
	kD = Nk/4 + Nk/2
	vU = Q[:,:,kU].squeeze()
	vD = Q[:,:,kD].squeeze()

	return xx,yy,vU,vD

#Ns = [240,492]
#Ns = [16,37]



fIn1 = "/glade/u/home/skareem/Work/xTreme/fstQ/msphere.h5"
fIn2 = "/glade/u/home/skareem/Work/xTreme/try/newQuad/msphere.h5"

fIns = [fIn2,fIn1,fIn1]
#Ns = [30,240,492]
Ns = [30,240,495]

N = len(Ns)

#fIn = "/Users/soratka1/Work/xtremeionosphere/Data/Quad/msphere.h5"

vID = "P"
vMin = 0
vMLog = 1.0e-1
vMax = 200
vN = mpl.colors.Normalize(vmin=vMin,vmax=vMax)
vN = LogNorm(vmin=vMLog,vmax=vMax)
xM = 20
yM = 20

cMap = "viridis"

figSize = (12,6)

fOut = "xP.png"
figQ = 300


fig = plt.figure(figsize=figSize)
wR = 20*np.ones(N+1)
wR[-1] = 1
gs = gridspec.GridSpec(1,N+1,width_ratios=wR)
for n in range(N):
	Ax = fig.add_subplot(gs[0,n])
	xx,yy,vU,vD = GetSlice(fIns[n],Ns[n])
	Ax.pcolormesh(xx, yy,vU,norm=vN,cmap=cMap)
	Ax.pcolormesh(xx,-yy,vD,norm=vN,cmap=cMap)
	plt.axis('scaled')
	Ax.set_xlim([-xM,xM])
	Ax.set_ylim([-yM,yM])

AxC = fig.add_subplot(gs[0,-1])

cb = mpl.colorbar.ColorbarBase(AxC,cmap=cMap,norm=vN,orientation='vertical')

plt.savefig(fOut,dpi=figQ)

print(Ns)
