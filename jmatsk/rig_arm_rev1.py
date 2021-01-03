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
    for each in chain:
        cmds.joint(n=each[0], p=each[1])
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
cmds.parentConstraint('fk_shoulder_jnt', 'ik_shoulder_jnt', 'bn_shoulder_jnt')
cmds.parentConstraint('fk_elbow_jnt', 'ik_elbow_jnt', 'bn_elbow_jnt')
cmds.parentConstraint('fk_wrist_jnt', 'ik_wrist_jnt', 'bn_wrist_jnt')

### FK/IK switch ###
# create circle for switch control that follows bind skeleton wrist and is always visible
cmds.select(cl=True)
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
cmds.parentConstraint('bn_wrist_jnt', 'fkik_switch_ctrl_grp')

# lock and hide switch ctrl attrs
attrCount = 0
fkikAttrList = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'visibility']
for each in fkikAttrList:
    fkikAttr = 'fkik_switch_ctrl.' + fkikAttrList[attrCount]
    cmds.setAttr(fkikAttr, lock=True, keyable=False)
    print fkikAttr
    attrCount += 1
print 'Loop end'

# add a float attr to fkik switch for keyable switch blend
cmds.addAttr('fkik_switch_ctrl', longName='FK_IK_Switch', defaultValue=0.00, minValue=0.00, maxValue=10.00,
             keyable=True)
# cmds.deleteAttr('fkik_switch_ctrl.FK_IK')

# create SDKs for FKIK switch; set Attrs then create SDK ###
fkikSwN = 'fkik_switch_ctrl.FK_IK_Switch'

fkikAttrList = ['bn_shoulder_jnt_parentConstraint1.fk_shoulder_jntW0',
                'bn_shoulder_jnt_parentConstraint1.ik_shoulder_jntW1',
                'bn_elbow_jnt_parentConstraint1.fk_elbow_jntW0',
                'bn_elbow_jnt_parentConstraint1.ik_elbow_jntW1',
                'bn_wrist_jnt_parentConstraint1.fk_wrist_jntW0',
                'bn_wrist_jnt_parentConstraint1.ik_wrist_jntW1', ]

fkikSwVal = [0, 1, 10]

cmds.setAttr(fkikSwN, fkikSwVal[0])
fkOn = cmds.getAttr(fkikSwN)
print fkOn

printCount = 0
for each in fkikAttrList:
    # print each
    cmds.setAttr(each, fkikSwVal[0])
    # if FKIK switch is 0 (FK), set FK constraints to 1 (on)
    if fkOn == 0:
        cmds.setAttr(fkikAttrList[0], 1)
        cmds.setAttr(fkikAttrList[2], 1)
        cmds.setAttr(fkikAttrList[4], 1)

for each in fkikAttrList:
    cmds.setDrivenKeyframe(each, currentDriver=fkikSwN)
    printCount += 1
    print printCount

    if printCount == 6:
        print 'FK SDK done, set IK SDK'
        printCount = 0
        cmds.setAttr(fkikSwN, fkikSwVal[2])
        fkOn = cmds.getAttr(fkikSwN)
        print fkOn

        for each in fkikAttrList:
            cmds.setAttr(each, fkikSwVal[0])
            # if FKIK switch is 10 (IK), set IK constraints to 1 (on)
            if fkOn == 10:
                cmds.setAttr(fkikAttrList[1], 1)
                cmds.setAttr(fkikAttrList[3], 1)
                cmds.setAttr(fkikAttrList[5], 1)

for each in fkikAttrList:
    cmds.setDrivenKeyframe(each, currentDriver=fkikSwN)
    printCount += 1
    print printCount

    if printCount == 6:
        print 'IK SDK done'
        printCount = 0
        # set switch to 0, or fk, by default
        cmds.setAttr(fkikSwN, fkikSwVal[0])
        fkOn = cmds.getAttr(fkikSwN)
        print fkOn
