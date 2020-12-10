import maya.cmds as cmds
cmds.select(cl=True)
cmds.select(all=True)
cmds.delete()

cmds.joint (n = 'shoulder_jnt', p = [0, 0, 0] )
# print cmds.joint ('shoulder', p=True, q=True)
# cmds.joint ('shoulder', p=[0,0,0], e=True)
cmds.joint (n = 'elbow_jnt', p = [7, 0, -0.3] )
# cmds.joint (e=True, zso=True, oj='xyz', sao='yup' )
cmds.joint (n='wrist_jnt', p = [14, 0, 0] )
# cmds.joint (e=True, zso=True, oj='xyz', sao='yup' )

# move shoulder joint to origin 000
# cmds.joint ('shoulder_jnt', p=[0,0,0], e=True)

cmds.select(cl=True)
# create ik arm joints
cmds.joint (n = 'ik_shoulder_jnt', p = [0, 0, 0] )
cmds.joint (n = 'ik_elbow_jnt', p = [7, 0, -0.3] )
cmds.joint (n='ik_wrist_jnt', p = [14, 0, 0] )

# create ik handle on ik arm joints
cmds.ikHandle (n='ikSolver_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver')

cmds.select(cl=True)
# create fk arm joints
cmds.joint (p = (0, 0, 0), n = 'fk_shoulder_jnt')
cmds.joint (p = (7, 0, -0.3), n = 'fk_elbow_jnt' )
cmds.joint (p = (14, 0, 0), n='fk_wrist_jnt')

cmds.select(cl=True)

### IK controls ###

# create ik control grouper
cmds.group(em=True, name='wrist_ik_ctrl_grp')

# create nurbs circle for IK wrist ctrl
cmds.circle(n='wrist_ik_ctrl', r=2, nr=[1,0,0])

cmds.select(cl=True)
# parent ik wrist ctrl to ik wrist grp
cmds.parent('wrist_ik_ctrl','wrist_ik_ctrl_grp')

# get wrist joint pos
pos = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)
# print pos

# move wrist ik ctrl group to joint and freeze transforms
cmds.xform('wrist_ik_ctrl_grp', t=pos)
cmds.makeIdentity(apply=True)

cmds.select(cl=True)
# point constrain ik handle to ik wrist ctrl
cmds.pointConstraint('wrist_ik_ctrl','ikSolver_arm')

# orient constrain ik wrist joint to ik wrist control
cmds.orientConstraint('wrist_ik_ctrl','ik_wrist_jnt')


### FK controls ###

# create nurbs circle for FK joints
cmds.circle(n='shoulder_fk_ctrl', r=2, nr=[1,0,0])
cmds.circle(n='elbow_fk_ctrl', r=2, nr=[1,0,0])
cmds.circle(n='wrist_fk_ctrl', r=2, nr=[1,0,0])

# create fk control grouper
cmds.group(em=True, name='shoulder_fk_ctrl_grp')
cmds.group(em=True, name='elbow_fk_ctrl_grp')
cmds.group(em=True, name='wrist_fk_ctrl_grp')

cmds.select(cl=True)
# parent fk ctrls to respective fk ctrl groups
cmds.parent('shoulder_fk_ctrl','shoulder_fk_ctrl_grp')
cmds.parent('elbow_fk_ctrl','elbow_fk_ctrl_grp')
cmds.parent('wrist_fk_ctrl','wrist_fk_ctrl_grp')

# get fk joint pos and move fk ctrl groups to fk joints and freeze transforms
posFK1 = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)
# print posFK1
cmds.xform('shoulder_fk_ctrl_grp', t = posFK1)
cmds.makeIdentity(apply=True)

posFK2 = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
# print posFK2
cmds.xform('elbow_fk_ctrl_grp', t = posFK2)
cmds.makeIdentity(apply=True)

posFK3 = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
# print posFK3
cmds.xform('wrist_fk_ctrl_grp', t = posFK3)
cmds.makeIdentity(apply=True)

cmds.select(cl=True)
# parent constrain fk joints to fk ctrls
cmds.parentConstraint('shoulder_fk_ctrl','fk_shoulder_jnt')
cmds.parentConstraint('elbow_fk_ctrl','fk_elbow_jnt')
cmds.parentConstraint('wrist_fk_ctrl','fk_wrist_jnt')

# parent fk ctrl groups into hierarchy
cmds.parent('elbow_fk_ctrl_grp','shoulder_fk_ctrl')
cmds.parent('wrist_fk_ctrl_grp','elbow_fk_ctrl')

cmds.select(cl=True)
