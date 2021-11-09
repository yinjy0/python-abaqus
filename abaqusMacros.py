# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
from caeModules import *
Mdb()

len, wid, hei, seed = getInputs((('Enter the length of the rectangle', '50'),
                                 ('Enter the width of the rectangle', '50'),
                                 ('Enter the height of the rectangle', '50'),
                                 ('Enter the global size', '5')))
print '**The length of the rectangle is '+len
print '**The width of the rectangle is '+wid
print '**The height of the rectangle is '+hei
print '**The global size is '+seed
len = float(len)
wid = float(wid)
hei = float(hei)
seed = float(seed)

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                            sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0.0, 0.0), point2=(len, hei))
session.viewports['Viewport: 1'].view.setValues(nearPlane=157.288,
                                                farPlane=219.836, width=371.577, height=179.626, cameraPosition=(
                                                    -8.54027, 27.1384, 188.562), cameraTarget=(-8.54027, 27.1384, 0))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,
                               type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s, depth=wid)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=seed, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()
