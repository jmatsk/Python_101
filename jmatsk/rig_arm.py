import maya.cmds as cmds

# wip test

cmds.joint(p=(-4.026908, 0, 0.0498688), n='shoulder')
# print cmds.joint ('shoulder', p=True, q=True)
# cmds.joint ('shoulder', p=[0,0,0], e=True)
cmds.joint(p=(2.954728, 0, -0.199475), n='elbow')
# cmds.joint (e=True, zso=True, oj='xyz', sao=True, yup=True, joint1 )
cmds.joint(p=(8.340561, 0, 0.0748032), n='wrist')
# cmds.joint (e=True, zso=True, oj='xyz', sao=True, yup=True, joint2 )
