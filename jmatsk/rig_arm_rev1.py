import maya.cmds as cmds

cmds.select(cl=True)
cmds.select(all=True)
cmds.delete()

# list containing 3 joint chains
jntList = [[['bn_shoulder_jnt', [0, 0, 0]],['bn_elbow_jnt', [7, 0, -0.3]],['bn_wrist_jnt', [14, 0, 0]]],
        [['ik_shoulder_jnt', [0, 0, 0]], ['ik_elbow_jnt', [7, 0, -0.3]], ['ik_wrist_jnt', [14, 0, 0]]],
        [['fk_shoulder_jnt', [0, 0, 0]],['fk_elbow_jnt', [7, 0, -0.3]],['fk_wrist_jnt', [14, 0, 0]]]]

# loop to create joints; checks for finished chain and clears selection before new chain
printCount = 0
for chain in jntList:
    for joint in chain:
        cmds.joint(n=joint[0], p=joint[1])
        printCount += 1

        if printCount == 3:
            print('chain done')
            cmds.select(cl=True)
            printCount = 0
print 'Loop end'

# create ik handle on ik arm joints
cmds.ikHandle(n='ikSolver_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver')

### IK controls ###
cmds.select(cl=True)
# create ik control grouper
cmds.group(em=True, name='wrist_ik_ctrl_grp')

# create nurbs circle for IK wrist ctrl
cmds.circle(n='wrist_ik_ctrl', r=2.5, nr=[1, 0, 0])

cmds.select(cl=True)
# parent ik wrist ctrl to ik wrist grp
cmds.parent('wrist_ik_ctrl', 'wrist_ik_ctrl_grp')

# get wrist joint pos
pos = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)
# print pos

# move wrist ik ctrl group to joint and freeze transforms
cmds.xform('wrist_ik_ctrl_grp', t=pos)
cmds.makeIdentity(apply=True)

cmds.select(cl=True)
# point constrain ik handle to ik wrist ctrl
cmds.pointConstraint('wrist_ik_ctrl', 'ikSolver_arm')
# orient constrain ik wrist joint to ik wrist control
cmds.orientConstraint('wrist_ik_ctrl', 'ik_wrist_jnt')

### IK pole vector ###
cmds.select(cl=True)

# create locator for elbow PV
cmds.spaceLocator(n='loc_elbow_pv')

# get pos of ik elbow joint
posElbow = cmds.xform('ik_elbow_jnt', q=True, t=True, ws=True)

# move pv loc to elbow joint pos
cmds.xform('loc_elbow_pv', t=posElbow)

# posLocElbTZ = cmds.getAttr('loc_elbow_pv.translateZ')
# pvMove = posLocElbTZ - 2
# print pvMove
cmds.select('loc_elbow_pv')
cmds.move(-10.2, z=1, relative=True)
cmds.select(cl=True)

# create pole vector constraint between IK handle and new elbow locator
cmds.poleVectorConstraint('loc_elbow_pv', 'ikSolver_arm')

# create nurbs circle, snap to PV locator, point constrain PV loc to nurbs circle

### FK controls ###
cmds.select(cl=True)
# create nurbs circle for FK joints
cmds.circle(n='shoulder_fk_ctrl', r=2, nr=[1, 0, 0])
cmds.circle(n='elbow_fk_ctrl', r=2, nr=[1, 0, 0])
cmds.circle(n='wrist_fk_ctrl', r=2, nr=[1, 0, 0])

# create fk control grouper
cmds.group(em=True, name='shoulder_fk_ctrl_grp')
cmds.group(em=True, name='elbow_fk_ctrl_grp')
cmds.group(em=True, name='wrist_fk_ctrl_grp')

cmds.select(cl=True)
# parent fk ctrls to respective fk ctrl groups
cmds.parent('shoulder_fk_ctrl', 'shoulder_fk_ctrl_grp')
cmds.parent('elbow_fk_ctrl', 'elbow_fk_ctrl_grp')
cmds.parent('wrist_fk_ctrl', 'wrist_fk_ctrl_grp')

# get fk joint pos and move fk ctrl groups to fk joints and freeze transforms
posFK1 = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)
# print posFK1
cmds.xform('shoulder_fk_ctrl_grp', t=posFK1)
cmds.makeIdentity(apply=True)

posFK2 = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
# print posFK2
cmds.xform('elbow_fk_ctrl_grp', t=posFK2)
cmds.makeIdentity(apply=True)

posFK3 = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
# print posFK3
cmds.xform('wrist_fk_ctrl_grp', t=posFK3)
cmds.makeIdentity(apply=True)

cmds.select(cl=True)
# parent constrain fk joints to fk ctrls
cmds.parentConstraint('shoulder_fk_ctrl', 'fk_shoulder_jnt')
cmds.parentConstraint('elbow_fk_ctrl', 'fk_elbow_jnt')
cmds.parentConstraint('wrist_fk_ctrl', 'fk_wrist_jnt')

# parent fk ctrl groups into hierarchy
cmds.parent('elbow_fk_ctrl_grp', 'shoulder_fk_ctrl')
cmds.parent('wrist_fk_ctrl_grp', 'elbow_fk_ctrl')

cmds.select(cl=True)

### constrain rig joints to fk and ik chains
cmds.parentConstraint('fk_shoulder_jnt', 'ik_shoulder_jnt', 'shoulder_jnt')
cmds.parentConstraint('fk_elbow_jnt', 'ik_elbow_jnt', 'elbow_jnt')
cmds.parentConstraint('fk_wrist_jnt', 'ik_wrist_jnt', 'wrist_jnt')

### FK/IK switch ###
# create circle for switch control that follows bind skeleton wrist and is always visible
cmds.select(cl=True)
# create nurbs circle for fkik switch
cmds.circle(n='fkik_switch_ctrl', r=1, nr=[1, 0, 0])

# create switch control grouper
cmds.group(em=True, name='fkik_switch_ctrl_grp')

cmds.select(cl=True)
# parent fkik switch ctrl to ctrl group
cmds.parent('fkik_switch_ctrl', 'fkik_switch_ctrl_grp')

# use fk wrist joint pos Variable and move switch ctrl group to wrist, then freeze transforms
cmds.xform('fkik_switch_ctrl_grp', t=posFK3)
cmds.makeIdentity(apply=True)

# offset switch ctrl from wrist joint and freeze xforms; switch ctrl group pivot stays at wrist
cmds.select(cl=True)
cmds.select('fkik_switch_ctrl')
cmds.move(7.5, x=1, relative=True)
cmds.makeIdentity(apply=True)
cmds.select(cl=True)

# constrain switch ctrl group to bind skeleton wris
cmds.parentConstraint('wrist_jnt', 'fkik_switch_ctrl_grp')

# lock and hide switch ctrl attrs
cmds.setAttr('fkik_switch_ctrl.tx', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.ty', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.tz', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.rx', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.ry', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.rz', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.sx', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.sy', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.sz', lock=True, keyable=False)
cmds.setAttr('fkik_switch_ctrl.visibility', lock=True, keyable=False)

# add a float attr to fkik switch for keyable switch blend
cmds.addAttr('fkik_switch_ctrl', longName='FK_IK_Switch', defaultValue=0.00, minValue=0.00, maxValue=10.00,
             keyable=True)
# cmds.deleteAttr('fkik_switch_ctrl.FK_IK')

# create SDKs for FKIK switch; set Attrs then create SDK ###
# shoulder sdk
cmds.setAttr("fkik_switch_ctrl.FK_IK_Switch", 0)
cmds.setAttr("shoulder_jnt_parentConstraint1.fk_shoulder_jntW0", 1)
cmds.setAttr("shoulder_jnt_parentConstraint1.ik_shoulder_jntW1", 0)
cmds.setDrivenKeyframe('shoulder_jnt_parentConstraint1.fk_shoulder_jntW0',
                       currentDriver='fkik_switch_ctrl.FK_IK_Switch')
cmds.setDrivenKeyframe('shoulder_jnt_parentConstraint1.ik_shoulder_jntW1',
                       currentDriver='fkik_switch_ctrl.FK_IK_Switch')

cmds.setAttr("fkik_switch_ctrl.FK_IK_Switch", 10)
cmds.setAttr("shoulder_jnt_parentConstraint1.fk_shoulder_jntW0", 0)
cmds.setAttr("shoulder_jnt_parentConstraint1.ik_shoulder_jntW1", 1)
cmds.setDrivenKeyframe('shoulder_jnt_parentConstraint1.fk_shoulder_jntW0',
                       currentDriver='fkik_switch_ctrl.FK_IK_Switch')
cmds.setDrivenKeyframe('shoulder_jnt_parentConstraint1.ik_shoulder_jntW1',
                       currentDriver='fkik_switch_ctrl.FK_IK_Switch')

# elbow sdk
cmds.setAttr("fkik_switch_ctrl.FK_IK_Switch", 0)
cmds.setAttr("elbow_jnt_parentConstraint1.fk_elbow_jntW0", 1)
cmds.setAttr("elbow_jnt_parentConstraint1.ik_elbow_jntW1", 0)
cmds.setDrivenKeyframe('elbow_jnt_parentConstraint1.fk_elbow_jntW0', currentDriver='fkik_switch_ctrl.FK_IK_Switch')
cmds.setDrivenKeyframe('elbow_jnt_parentConstraint1.ik_elbow_jntW1', currentDriver='fkik_switch_ctrl.FK_IK_Switch')

cmds.setAttr("fkik_switch_ctrl.FK_IK_Switch", 10)
cmds.setAttr("elbow_jnt_parentConstraint1.fk_elbow_jntW0", 0)
cmds.setAttr("elbow_jnt_parentConstraint1.ik_elbow_jntW1", 1)
cmds.setDrivenKeyframe('elbow_jnt_parentConstraint1.fk_elbow_jntW0', currentDriver='fkik_switch_ctrl.FK_IK_Switch')
cmds.setDrivenKeyframe('elbow_jnt_parentConstraint1.ik_elbow_jntW1', currentDriver='fkik_switch_ctrl.FK_IK_Switch')

# wrist sdk
cmds.setAttr("fkik_switch_ctrl.FK_IK_Switch", 0)
cmds.setAttr("wrist_jnt_parentConstraint1.fk_wrist_jntW0", 1)
cmds.setAttr("wrist_jnt_parentConstraint1.ik_wrist_jntW1", 0)
cmds.setDrivenKeyframe('wrist_jnt_parentConstraint1.fk_wrist_jntW0', currentDriver='fkik_switch_ctrl.FK_IK_Switch')
cmds.setDrivenKeyframe('wrist_jnt_parentConstraint1.ik_wrist_jntW1', currentDriver='fkik_switch_ctrl.FK_IK_Switch')

cmds.setAttr("fkik_switch_ctrl.FK_IK_Switch", 10)
cmds.setAttr("wrist_jnt_parentConstraint1.fk_wrist_jntW0", 0)
cmds.setAttr("wrist_jnt_parentConstraint1.ik_wrist_jntW1", 1)
cmds.setDrivenKeyframe('wrist_jnt_parentConstraint1.fk_wrist_jntW0', currentDriver='fkik_switch_ctrl.FK_IK_Switch')
cmds.setDrivenKeyframe('wrist_jnt_parentConstraint1.ik_wrist_jntW1', currentDriver='fkik_switch_ctrl.FK_IK_Switch')

# set switch to 0, or fk, by default
cmds.setAttr("fkik_switch_ctrl.FK_IK_Switch", 0)