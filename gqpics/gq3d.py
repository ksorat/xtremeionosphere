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
gdata = "~/Work/xtremeionosphere/Data/Quad/msphere.xmf"
gdata = "~/Work/xTreme/fstQ/msphere.xmf"


Nt0 = 17
Nt0 = 18

n = Nt0

#Nt0 = 169

#Main scaling info
#--------------------
gX0 = 6.38e+6 #m
gV0 = 100.0e+3 #m/s
gB0 = 4.581 #nT

#Image config options
#--------------------
doQuiet = False

Rin = 2.51

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

DefineScalarExpression("inRad","if( le(RadAll, 25), 1.0, 0.0)")
DefineScalarExpression("outRad","if( ge(RadAll, 3.5), 1.0, 0.0)")
DefineScalarExpression("inPhi","if( ge(abs(phi), 1.5), 1.0, 0.0)")
DefineScalarExpression("inY","if( le(abs(yRe), 8.0), 1.0, 0.0)")

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
DefineScalarExpression("vCut","inPhi*inRad*outRad*inY")
DefineScalarExpression("vScl","zonal_constant(gMesh,100.0)")
DefineScalarExpression("Ve","vScl*(Vx*cos(phi)+Vy*sin(phi))")
DefineVectorExpression("Vxy","vCut*vScl*{Vx,Vy,0.0}")
DefineVectorExpression("V"  ,"vCut*vScl*{Vx,Vy,Vz}")

#Open database
OpenDatabase(gdata)
md0 = GetMetaData(gdata)

#Create plots
pCent = 1
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
pyv.lfmPCol(gdata,"dBz",vBds=[-25,25],Inv=True,Light=False,Legend=True,cMap="RdGy")
pOp = GetPlotOptions()
pOp.centering = pCent
SetPlotOptions(pOp)

AddOperator("Slice",0)
ops = GetOperatorOptions(0)
ops.project2d = 0
ops.axisType = 2
SetOperatorOptions(ops)

#Pressure poloidal
pyv.lfmPCol(gdata,"P",vBds=[1.0e-1,100],Light=False,Log=True,Legend=True,cMap="viridis")
pOp = GetPlotOptions()
pOp.centering = pCent
SetPlotOptions(pOp)

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

#Velocity contours

vMag = 150
NumVC = 15
yCut = 15
#Use fake pcolor to get right toolbar
pyv.lfmPCol(gdata,"Ve",vBds=[-vMag,vMag],Legend=True,cMap="PiYG")
pOp = GetPlotOptions()
pOp.opacity = 0
SetPlotOptions(pOp)

AddPlot("Contour","Ve")
pOp = GetPlotOptions()
pOp.colorType = 2
pOp.colorTableName = "PiYG"
pOp.lineWidth = 1
pOp.minFlag = 1
pOp.maxFlag = 1
pOp.min = -vMag
pOp.max = vMag
pOp.contourNLevels = NumVC
pOp.legendFlag = 0
SetPlotOptions(pOp)

AddOperator("Slice",0)
ops = GetOperatorOptions(0)
ops.project2d = 0
ops.axisType = 2
SetOperatorOptions(ops)

AddOperator("Threshold",0)
ops = GetOperatorOptions(1)
ops.listedVarNames = ("yRe","absphi","RadAll")
DefineScalarExpression("absphi","abs(phi)")
ops.lowerBounds = (-yCut,1.2*np.pi/2,5.0)
ops.upperBounds = (+yCut,np.pi,50)

SetOperatorOptions(ops)

# #Add velocity arrows
# AddPlot("Vector","Vxy")
# pOp = GetPlotOptions()
# pOp.minFlag = 1
# pOp.maxFlag = 1
# pOp.min = 0.0
# pOp.max = 200.0
# pOp.colorTableName = "Purples"
# pOp.autoScale = 0
# pOp.scaleByMagnitude = 0
# pOp.lineStem = 0
# pOp.nVectors = 2600
# #pOp.scale = 0.025
# pOp.scale = 1
# pOp.geometryQuality = 1
# SetPlotOptions(pOp)

# AddOperator("Slice",0)
# ops = GetOperatorOptions(0)
# ops.project2d = 0
# ops.axisType = 2
# SetOperatorOptions(ops)

# AddOperator("Threshold",0)
# ops = GetOperatorOptions(1)
# ops.listedVarNames = ("Vx")
# ops.lowerBounds = (-1.5)
# SetOperatorOptions(ops)


#Set visual range
# v3d = GetView3D()
# v3d.viewNormal = (-0.128, 0.922099, -0.365171)
# v3d.focus = (-122.94, 0, 0)
# v3d.viewUp = (-0.0144839, -0.369899, -0.928959)
# v3d.viewAngle = 30
# v3d.parallelScale = 225.223
# v3d.nearPlane = -450.447
# v3d.farPlane = 450.447
# v3d.imagePan = (-0.24736, -0.00364242)
# v3d.imageZoom = 14.421
# v3d.perspective = 1
# v3d.eyeAngle = 2
# v3d.centerOfRotationSet = 0
# v3d.centerOfRotation = (-122.94, 0, 0)
# v3d.axis3DScaleFlag = 0
# v3d.axis3DScales = (1, 1, 1)
# v3d.shear = (0, 0, 1)
# v3d.windowValid = 1
# SetView3D(v3d)

#pyv.ShiftWin3D(dx=0.25,dy=0.25)
ResetView()
pyv.ShiftWin3D(dx=-0.225)
#pyv.SetWin3D(Zoom=4)
pyv.SetWin3D(Ax=0,Ang=-60,Zoom=14)
#pyv.ShiftWin3D(dx=-0.2)
#pyv.SetWin3D(Zoom=14)
#
#pyv.SetWin3D(Ax=0,Ang=-60,Zoom=12)


#Move legends
fH = 0.025
dx = 0.01
dy = 0.01
xScl = 0.65
yScl = 0.45
#dBz
x1 = 0.05
y1 = 0.15
P1 = GetAnnotationObject("Plot0001")
P1.drawMinMax = 0
P1.managePosition = 0
P1.position = (x1,y1)
P1.drawTitle = 0
P1.orientation = 2
P1.yScale = yScl
P1.fontHeight = fH
pyv.genTit("Residual Field [nT]",Pos=(x1,y1+dy),height=fH)

#Pressure
P2 = GetAnnotationObject("Plot0002")
x2 = 0.9
y2 = 0.9
P2.drawMinMax = 0
P2.managePosition = 0
P2.position = (x2,y2)
P2.drawTitle = 0
P2.orientation = 1
P2.xScale = xScl
P2.yScale = 1.0
P2.fontHeight = fH
pyv.genTit("Pressure",Pos=(x2-3*dx,y2+2*dy),height=fH)

#Speed
P4 = GetAnnotationObject("Plot0004")
x4 = 0.45
y4 = y1

P4.drawMinMax = 0
P4.managePosition = 0
P4.position = (x4,y4)
P4.drawTitle = 0
P4.orientation = 2
P4.yScale = yScl
P4.fontHeight = fH
pyv.genTit("Velocity [km/s]",Pos=(x4,y4+dy),height=fH)

#GetAnnotationObject('Plot0000').drawMinMax = 0
#GetAnnotationObject('Plot0000').managePosition = 0

#plXs = [0.25,0.5]
#plYs = [0.25,0.5]
#plTits = ["Blah1","Blah2"]
#pyv.cleanLegends(plXs,plYs,plTits)

#Set time and draw
SetTimeSliderState(n)
DrawPlots()
#Save
swa = GetSaveWindowAttributes()
swa.fileName = "img.%04d"%(n)
SetSaveWindowAttributes(swa)
SaveWindow()
