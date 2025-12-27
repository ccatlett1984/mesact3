
from libmesact import utilities

def axis_changed(parent):
	board = parent.sender().objectName()[:3]
	joint = parent.sender().objectName()[-1]
	#print(board, joint)
	all_axes = ['X', 'Y', 'Z', 'U', 'V', 'W', 'A', 'B', 'C']
	linear_axes = ['X', 'Y', 'Z', 'U', 'V', 'W']
	angular_axes = ['A', 'B', 'C']

	if parent.sender().currentData():
		axis = parent.sender().currentText()
		if axis in linear_axes:
			getattr(parent, f'{board}axis_type_{joint}').setText('LINEAR')
		elif axis in angular_axes:
			getattr(parent, f'{board}axis_type_{joint}').setText('ANGULAR')

	# update coordinates label
	coord_list = []
	for i in range(3):
		for j in range(6):
			axis_letter = getattr(parent, f'c{i}_axis_{j}').currentText()
			if axis_letter in all_axes:
				coord_list.append(axis_letter)
				parent.coordinates_lb.setText(''.join(coord_list))

	# set copy pb enables
	if coord_list:
		parent.copy_linear_scale_pb.setEnabled(True)
		parent.copy_angluar_scale_pb.setEnabled(True)
	else:
		parent.copy_linear_scale_pb.setEnabled(False)
		parent.copy_angluar_scale_pb.setEnabled(False)
		# clear scale copy cb's
		parent.lin_scale_joint_cb.clear()
		parent.angluar_scale_joint_cb.clear()
	return

	# setup scale axes and joints
	if set(linear_axes)&set(coord_list):
		parent.lin_scale_joint_cb.clear()
		parent.lin_scale_joint_cb.addItem('Select', False)
	else:
		parent.lin_scale_joint_cb.clear()
	if set(angular_axes)&set(coord_list):
		parent.angluar_scale_joint_cb.clear()
		parent.angluar_scale_joint_cb.addItem('Select', False)
	else:
		parent.angluar_scale_joint_cb.clear()

	for i in range(3):
		for j in range(6):
			board = getattr(parent, f'c{i}_JointTW').tabText(0)
			axis_letter = getattr(parent, f'c{i}_axis_{j}').currentText()
			if axis_letter in linear_axes:
				if board in ['7i77']:
					parent.lin_scale_joint_cb.addItem(f'{board}, {axis_letter} Axis, Drive {j}', f'c{i}_encoderScale_{j}')
				else:
					parent.lin_scale_joint_cb.addItem(f'{board}, {axis_letter} Axis, Drive {j}', f'c{i}_scale_{j}')
			if axis_letter in angular_axes:
				parent.angluar_scale_joint_cb.addItem(f'{board}, {axis_letter} Axis, Drive {j}', f'c{i}_scale_{j}')

def drive_changed(parent):
	timing = parent.sender().currentData()
	board = parent.sender().objectName()[:2]
	joint = f'{parent.sender().objectName()[-1]}'
	if parent.sender().objectName() == 'spindleDriveCB':
		connector = 'spindle'
		joint = ''
	if timing:
		parent.sender().setEditable(False)
		getattr(parent, f'{board}_step_time_{joint}').setText(timing[0])
		getattr(parent, f'{board}_step_space_{joint}').setText(timing[1])
		getattr(parent, f'{board}_dir_setup_{joint}').setText(timing[2])
		getattr(parent, f'{board}_dir_hold_{joint}').setText(timing[3])
		getattr(parent, f'{board}_step_time_{joint}').setEnabled(False)
		getattr(parent, f'{board}_step_space_{joint}').setEnabled(False)
		getattr(parent, f'{board}_dir_setup_{joint}').setEnabled(False)
		getattr(parent, f'{board}_dir_hold_{joint}').setEnabled(False)
	else:
		parent.sender().setEditable(True)
		getattr(parent, f'{board}_step_time_{joint}').setEnabled(True)
		getattr(parent, f'{board}_step_space_{joint}').setEnabled(True)
		getattr(parent, f'{board}_dir_setup_{joint}').setEnabled(True)
		getattr(parent, f'{board}_dir_hold_{joint}').setEnabled(True)

def update_axis_info(parent):
	card = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, f'{card}_scale_' + joint).text()
	if scale and utilities.is_number(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, f'{card}_max_vel_' + joint).text()
	if maxVelocity and utilities.is_number(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, f'{card}_max_accel_' + joint).text()
	if maxAccel and utilities.is_number(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if parent.linear_units_cb.currentData():
		accelTime = maxVelocity / maxAccel
		getattr(parent, f'{card}_timeJoint_' + joint).setText(f'{accelTime:.3f} seconds')
		accelDistance = accelTime * 0.5 * maxVelocity
		getattr(parent, f'{card}_distanceJoint_' + joint).setText(f'{accelDistance:.3f} {parent.linear_units_cb.currentData()}')
		stepRate = scale * maxVelocity
		getattr(parent, f'{card}_stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} Hz')

def set_default_pid(parent):
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if not parent.linear_units_cb.currentData():
		QMessageBox.warning(parent,'Warning', 'Settings Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	if joint == 's':
		getattr(parent, 'p_s').setValue(0)
		getattr(parent, 'i_s').setValue(0)
		getattr(parent, 'd_s').setValue(0)
		getattr(parent, 'ff0_s').setValue(1)
		getattr(parent, 'ff1_s').setValue(0)
		getattr(parent, 'ff2_s').setValue(0)
		getattr(parent, 'bias_s').setValue(0)
		getattr(parent, 'max_output_s').setValue(parent.spindleMaxRpm.value())
		getattr(parent, 'max_error_s').setValue(0)
		getattr(parent, 'deadband_s').setValue(0)
		return

	p = int(1000/(parent.servo_period_sb.value()/1000000))
	getattr(parent,  f'{connector}_p_{joint}').setText(f'{p}')
	getattr(parent, f'{connector}_i_{joint}').setText('0')
	getattr(parent, f'{connector}_d_{joint}').setText('0')
	getattr(parent, f'{connector}_ff0_{joint}').setText('0')
	getattr(parent, f'{connector}_ff1_{joint}').setText('1')
	getattr(parent, f'{connector}_ff2_{joint}').setText('0')
	getattr(parent, f'{connector}_bias_{joint}').setText('0')
	getattr(parent, f'{connector}_max_output_{joint}').setText('0')
	if parent.linear_units_cb.currentData() == 'inch':
		getattr(parent, f'{connector}_max_error_{joint}').setText('0.0005')
	else: # metric
		getattr(parent, f'{connector}_max_error_{joint}').setText('0.0127')
	getattr(parent, f'{connector}_max_error_{joint}').setText('0.0005')
	getattr(parent, f'{connector}_deadband_{joint}').setText('0')



def set_default_ferror(parent):
	if not parent.linear_units_cb.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if parent.linear_units_cb.currentData() == 'inch':
		getattr(parent, f'{connector}_max_ferror_{joint}').setText(' 0.002')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.001')
	else:
		getattr(parent, f'{connector}_max_ferror_{joint}').setText(' 0.005')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.0025')

def set_default_analog(parent):
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	getattr(parent, f'{connector}_analog_min_limit_{joint}').setText('-10')
	getattr(parent, f'{connector}_analog_max_limit_{joint}').setText('10')
	getattr(parent, f'{connector}_analog_scale_max_{joint}').setText('10')

