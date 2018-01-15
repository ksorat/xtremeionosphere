#3D gamera quad run pics
#Using python+visit setup

import sys
import numpy as np
import datetime
from visit import *
from visit_utils import *
from visit_utils.common import lsearch #lsearch(dir(),"blah")
import pyVisit as pyv

#Data info
gdata = "~/Work/xtremeionosphere/Data/Dbl/msphere.xmf"
gdata = "~/Work/xtremeionosphere/Data/Quad/msphere.xmf"

#Main scaling info
#--------------------
gX0 = 6.38e+6 #m
gV0 = 100.0e+3 #m/s
gB0 = 4.581 #nT

#Image config options
#--------------------
doQuiet = False


#Launch viewer
if (doQuiet):
	LaunchNowin()
else:
	Launch()

#Expressions
MagM = -0.311*1.0e+5 #Mag moment, Gauss->nT
eBxStr = "3*xRe*zRe*(%e)*rm5"%(MagM)
eByStr = "3*yRe*zRe*(%e)*rm5"%(MagM)
eBzStr = "(3.0*zRe*zRe - Radius*Radius)*(%e)*rm5"%(MagM)

#Define expressions (Geometry)
DefineScalarExpression("RadAll","polar_radius(gMesh)")
DefineScalarExpression("Radius","if( ge(RadAll, 2.1), RadAll, 2.1)") #Respect cutout
DefineScalarExpression("xRe","coord(gMesh)[0]")
DefineScalarExpression("yRe","coord(gMesh)[1]")
DefineScalarExpression("zRe","coord(gMesh)[2]")
DefineScalarExpression("rm5","Radius^(-5.0)")
DefineScalarExpression("bScl","zonal_constant(gMesh,%e)"%(gB0))
#Earth field
DefineScalarExpression("eBx",eBxStr)
DefineScalarExpression("eBy",eByStr)
DefineScalarExpression("eBz",eBzStr)

#Residual field
DefineScalarExpression("dBx","bScl*Bx-eBx")
DefineScalarExpression("dBy","bScl*By-eBy")
DefineScalarExpression("dBz","bScl*Bz-eBz")


#Open database
OpenDatabase(gdata)
md0 = GetMetaData(gdata)

#Create plot
pyv.lfmPCol(gdata,"eBz",vBds=[-25,25])


DrawPlots()

