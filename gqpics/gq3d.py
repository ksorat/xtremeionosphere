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
Nt0 = 17
Rin = 2.25

#Launch viewer
if (doQuiet):
	LaunchNowin()
else:
	Launch()

#Init
pyv.setAtts()

#Expressions
MagM = -0.311*1.0e+5 #Mag moment, Gauss->nT
eBxStr = "3*xRe*zRe*(%e)*rm5"%(MagM)
eByStr = "3*yRe*zRe*(%e)*rm5"%(MagM)
eBzStr = "(3.0*zRe*zRe - Radius*Radius)*(%e)*rm5"%(MagM)

#Define expressions (Geometry)
DefineScalarExpression("RadAll","polar_radius(gMesh)")
DefineScalarExpression("Radius","if( ge(RadAll, 2.1), RadAll, 2.1)") #Respect cutout
DefineScalarExpression("phi","cylindrical_theta(gMesh)")

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

#Current (Jy)
DefineScalarExpression("jScl","zonal_constant(gMesh,%e)"%(gB0/gX0))
DefineScalarExpression("Current","abs(jScl*Jy)")

#Earthward velocity
DefineScalarExpression("vScl","zonal_constant(gMesh,100.0)")
DefineScalarExpression("vScl*(Vx*cos(phi)+Vy*sin(phi))")
#Open database
OpenDatabase(gdata)
md0 = GetMetaData(gdata)

#Create plots
#--------------------

#Earth cutout
AddPlot("Contour","RadAll")
ops = GetPlotOptions()
ops.contourMethod = 1
ops.contourValue = (Rin)
ops.colorType = 0
ops.singleColor = (211,211,211,255)
ops.legendFlag = 0
SetPlotOptions(ops)

#pyv.plotContour(gdata,"RadAll",values=[Rin])

#Field perturbation
pyv.lfmPCol(gdata,"dBz",vBds=[-25,25],Light=False,Legend=True,cMap="RdYlBu")
AddOperator("Slice",0)
ops = GetOperatorOptions(0)
ops.project2d = 0
ops.axisType = 2
SetOperatorOptions(ops)

#Pressure poloidal
pyv.lfmPCol(gdata,"P",vBds=[1.0e-1,100],Light=False,Log=True,Legend=True,cMap="viridis")
AddOperator("Slice",0)
ops = GetOperatorOptions(0)
ops.project2d = 0
ops.axisType = 1
SetOperatorOptions(ops)

#Add field lines
Nfl = 40

AddPlot("Pseudocolor","operators/IntegralCurve/B")
pOp = GetPlotOptions()
pOp.colorTableName = "bluehot"
pOp.invertColorTable = 1
pOp.legendFlag = 0
pOp.lightingFlag = 1
SetPlotOptions(pOp)

sOp = GetOperatorOptions(0)
sOp.sourceType = 3
sOp.planeOrigin = (0, 0, 0)
sOp.planeNormal = (0, 1, 0)
sOp.planeUpAxis = (0, 0, 1)
sOp.radius = 10
sOp.sampleDensity0 = Nfl
sOp.termDistance = 15
sOp.terminateByDistance = 1
sOp.dataValue = 0
SetOperatorOptions(sOp)

AddOperator("Tube",0)
tOp = GetOperatorOptions(1)
tOp.radiusFractionBBox = 0.00025
SetOperatorOptions(tOp)

#Set visual range
v3d = GetView3D()
v3d.viewNormal = (-0.128, 0.922099, -0.365171)
v3d.focus = (-122.94, 0, 0)
v3d.viewUp = (-0.0144839, -0.369899, -0.928959)
v3d.viewAngle = 30
v3d.parallelScale = 225.223
v3d.nearPlane = -450.447
v3d.farPlane = 450.447
v3d.imagePan = (-0.24736, -0.00364242)
v3d.imageZoom = 14.421
v3d.perspective = 1
v3d.eyeAngle = 2
v3d.centerOfRotationSet = 0
v3d.centerOfRotation = (-122.94, 0, 0)
v3d.axis3DScaleFlag = 0
v3d.axis3DScales = (1, 1, 1)
v3d.shear = (0, 0, 1)
v3d.windowValid = 1
SetView3D(v3d)


#Move legends
#dBz
fH = 0.025
P1 = GetAnnotationObject("Plot0001")
P1.drawMinMax = 0
P1.managePosition = 0
P1.position = (0.05,0.1)
P1.drawTitle = 0
P1.orientation = 2
P1.yScale = 0.5
P1.fontHeight = fH
pyv.genTit("Residual Field [nT]",Pos=(0.05,0.105),height=fH)

#Pressure
P2 = GetAnnotationObject("Plot0002")
P2.drawMinMax = 0
P2.managePosition = 0
P2.position = (0.9,0.9)
P2.drawTitle = 0
P2.orientation = 1
P2.xScale = 0.75
P2.yScale = 1.0
P2.fontHeight = fH
pyv.genTit("Pressure",Pos=(0.875,0.925),height=fH)


#GetAnnotationObject('Plot0000').drawMinMax = 0
#GetAnnotationObject('Plot0000').managePosition = 0

#plXs = [0.25,0.5]
#plYs = [0.25,0.5]
#plTits = ["Blah1","Blah2"]
#pyv.cleanLegends(plXs,plYs,plTits)

#Set time and draw
SetTimeSliderState(Nt0)
DrawPlots()

