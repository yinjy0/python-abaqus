#!/user/bin/python
# -* - coding:UTF-8 -*-
# 该脚本的功能是搜索当前视口中输出数据库文件中的最大Mises应力。
# 要求：视口中必须打开某个输出数据库文件，否则，将抛出异常。
from abaqus import *
from abaqusConstants import *
import visualization
import displayGroupOdbToolset as dgo

# 对当前视口中的输出数据库进行操作
vp = session.viewports[session.currentViewportName]
odb = vp.displayedObject
if type(odb) != visualization.OdbType: 
    raise 'The ODB file must be displayed in the current viewport.'

# 搜索最大Mises应力
maxValue = None
stressOutputExists = FALSE
for step in odb.steps.values():
    print 'The processing step is:', step.name
    for frame in step.frames:
        try: 
            stress = frame.fieldOutputs['S']
            stressOutputExists = TRUE
        except KeyError: # 跳过不包含应力输出的帧
            continue
        for stressValue in stress.values:
            if (not maxValue or
                    stressValue.mises > maxValue.mises):
                    maxValue = stressValue
                    maxStep, maxFrame = step, frame  
               
# 如果odb文件中没有输出应力结果，则抛出异常。
if not stressOutputExists:
    raise 'The ODB file does not contain the output of stress results. '

# 输出最大Mises应力的详细信息
print 'The maximum Mises stress %E found is at:' % maxValue.mises
print 'Step:              ', maxStep.name 
print 'Frame:             ', maxFrame.frameId    
print 'Part instance:     ', maxValue.instance.name
print 'Element label:     ', maxValue.elementLabel 
print 'Section points:    ', maxValue.sectionPoint
print 'Integration points:', maxValue.integrationPoint

# 对最大Mises应力所在单元设置红色进行高亮显示
leaf = dgo.Leaf(ALL_SURFACES)
vp.odbDisplay.displayGroup.remove(leaf)
leaf = dgo.LeafFromElementLabels(partInstanceName=maxValue.instance.name, 
    elementLabels=(maxValue.elementLabel,) )
vp.setColor(leaf=leaf, fillColor='Red')
vp.odbDisplay.commonOptions.setValues(renderStyle=FILLED,
    elementShrink=ON, elementShrinkFactor=0.15)
vp.odbDisplay.display.setValues(plotState=(UNDEFORMED,))