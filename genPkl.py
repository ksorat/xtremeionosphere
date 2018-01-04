#Read from trap.pkl (all lost trapped particles) and create new pickle file

#Identify all interesting particles, map them to R=1 along dipole lines

import numpy as np
import cPickle as pickle


fPkl = "Trap.pkl"
fOut = "Precip.pkl"

#T0 value (roughly time of impact)
T0 = 45000.0

#Critical values
rIn = 1.5
rCrit = 2.15

kMin = 1.0e-8
kMax = 100

tMin = 35000.0 #Don't count immediately lost particles
tLossMax = 300 #Within 5 hours of CME

#tLossMax = 3000

#Load trapped data from PKL
with open(fPkl,"rb") as f:
	X   = pickle.load(f)
	Y   = pickle.load(f)
	Z   = pickle.load(f)
	Xeq = pickle.load(f)
	Yeq = pickle.load(f)
	Teq = pickle.load(f)
	pID = pickle.load(f)
	K   = pickle.load(f)

Ntot = X.size
Nbad = np.isnan(X).sum()

Ib = ~np.isnan(X) & (K>=kMin) & (K<=kMax) & (Teq>=tMin)
R = np.sqrt(X**2.0 + Y**2.0 + Z**2.0)
Req = np.sqrt(Xeq**2.0 + Yeq**2.0)
TLoss = (Teq-T0)/60.0

IAtm = (R<=rCrit) & (Req>=rIn) & (TLoss<=tLossMax) & (R>=1.0)

#Cut down to remaining values
I = Ib & IAtm
X = X[I]
Y = Y[I]
Z = Z[I]
K = K[I]
TLoss = TLoss[I]

#Now map to ionosphere
r = np.sqrt(X**2.0 + Y**2.0 + Z**2.0)
lamb = np.arcsin(Z/r)
phi = np.arctan2(Y,X)
L = r/(np.cos(lamb)**2.0)
LamE = np.arccos(1/np.sqrt(L))

#Now write pickle
r2d = 180.0/np.pi

print("Saving data for %d particles ..."%(phi.size))
with open(fOut,"wb") as f:
	pickle.dump(r2d*phi,f)
	pickle.dump(r2d*LamE,f)
	pickle.dump(TLoss,f)
	pickle.dump(K,f)



