# *-* coding:utf8 *-*
from driverUtils import executeOnCaeStartup
from caeModules import *
from abaqus import *
from abaqusConstants import *
file_path = 'D:/ping shi zi/d5v4-1 - d5v4-5-2x/s-d5v4-1.odb'
saving_path = 'D:/ping shi zi/d5v4-1 - d5v4-5-2x/sc/d5v4-1'
# odb导入
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
o1 = session.openOdb(name=file_path,
                     readOnly=False)
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
# 修改视图符合要求
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].view.rotate(xAngle=0, yAngle=0, zAngle=90,
                                             mode=MODEL)
session.viewports['Viewport: 1'].view.rotate(xAngle=0, yAngle=90, zAngle=0,
                                             mode=MODEL)
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    numIntervals=10, maxAutoCompute=OFF, maxValue=4.6e8, minAutoCompute=OFF,
    minValue=1e5)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendFont='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendDecimalPlaces=2)
session.graphicsOptions.setValues(backgroundStyle=SOLID,
                                  backgroundColor='#FFFFFF')
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendBox=OFF)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    visibleEdges=FEATURE)
leaf = dgo.LeafFromElementSets(elementSets=("PANEL-1.SET-10", ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
# 打印
session.printOptions.setValues(vpBackground=ON, compass=ON)
session.printToFile(fileName=saving_path, format=PNG,
                    canvasObjects=(session.viewports['Viewport: 1'], ))
session.odbs[file_path].close()
