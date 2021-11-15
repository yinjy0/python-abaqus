#!/user/bin/python
# -* - coding:UTF-8 -*-
# �ýű��Ĺ�����������ǰ�ӿ���������ݿ��ļ��е����MisesӦ����
# Ҫ���ӿ��б����ĳ��������ݿ��ļ������򣬽��׳��쳣��
from abaqus import *
from abaqusConstants import *
import visualization
import displayGroupOdbToolset as dgo

# �Ե�ǰ�ӿ��е�������ݿ���в���
vp = session.viewports[session.currentViewportName]
odb = vp.displayedObject
if type(odb) != visualization.OdbType: 
    raise 'The ODB file must be displayed in the current viewport.'

# �������MisesӦ��
maxValue = None
stressOutputExists = FALSE
for step in odb.steps.values():
    print 'The processing step is:', step.name
    for frame in step.frames:
        try: 
            stress = frame.fieldOutputs['S']
            stressOutputExists = TRUE
        except KeyError: # ����������Ӧ�������֡
            continue
        for stressValue in stress.values:
            if (not maxValue or
                    stressValue.mises > maxValue.mises):
                    maxValue = stressValue
                    maxStep, maxFrame = step, frame  
               
# ���odb�ļ���û�����Ӧ����������׳��쳣��
if not stressOutputExists:
    raise 'The ODB file does not contain the output of stress results. '

# ������MisesӦ������ϸ��Ϣ
print 'The maximum Mises stress %E found is at:' % maxValue.mises
print 'Step:              ', maxStep.name 
print 'Frame:             ', maxFrame.frameId    
print 'Part instance:     ', maxValue.instance.name
print 'Element label:     ', maxValue.elementLabel 
print 'Section points:    ', maxValue.sectionPoint
print 'Integration points:', maxValue.integrationPoint

# �����MisesӦ�����ڵ�Ԫ���ú�ɫ���и�����ʾ
leaf = dgo.Leaf(ALL_SURFACES)
vp.odbDisplay.displayGroup.remove(leaf)
leaf = dgo.LeafFromElementLabels(partInstanceName=maxValue.instance.name, 
    elementLabels=(maxValue.elementLabel,) )
vp.setColor(leaf=leaf, fillColor='Red')
vp.odbDisplay.commonOptions.setValues(renderStyle=FILLED,
    elementShrink=ON, elementShrinkFactor=0.15)
vp.odbDisplay.display.setValues(plotState=(UNDEFORMED,))