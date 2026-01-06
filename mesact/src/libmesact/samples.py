
from libmesact import utilities

def default_imperial(parent):
	utilities.new_config(parent)
	parent.linear_units_cb.setCurrentIndex(parent.linear_units_cb.findData('inch'))
	parent.default_lin_jog_vel_dsb.setValue(0.5)
	parent.max_lin_jog_vel_dsb.setValue(1.0)
	default(parent)

def default_metric(parent):
	utilities.new_config(parent)
	parent.linear_units_cb.setCurrentIndex(parent.linear_units_cb.findData('mm'))
	parent.default_lin_jog_vel_dsb.setValue(1.5)
	parent.max_lin_jog_vel_dsb.setValue(25.0)
	default(parent)

def default(parent):
	parent.gui_cb.setCurrentIndex(parent.gui_cb.findData('axis'))
	parent.position_offset_cb.setCurrentIndex(parent.position_offset_cb.findData('RELATIVE'))
	parent.position_feedback_cb.setCurrentIndex(parent.position_feedback_cb.findData('COMMANDED'))
	parent.max_feed_override_dsb.setValue(1.2)
	parent.sample_5i25_7i76_pb.setEnabled(True)
	parent.sample_5i25_7i77_pb.setEnabled(True)
	parent.sample_7i76eu_pb.setEnabled(True)
	parent.sample_7i92t_7i76_pb.setEnabled(True)
	parent.sample_7i92t_7i77_pb.setEnabled(True)
	parent.sample_7i95t_pb.setEnabled(True)
	parent.sample_7i96s_pb.setEnabled(True)
	parent.sample_7i97t_pb.setEnabled(True)

def sample_5i25_7i76(parent):
	parent.board_cb.setCurrentIndex(parent.board_cb.findText('5i25T'))
	parent.daughter_cb_2.setCurrentIndex(parent.daughter_cb_2.findText('7i76'))
	set_joints(parent, 2, ['X', 'Y', 'Z'], 'stepper')
	parent.c2_home_sequence_0.setText('2')
	parent.c2_home_sequence_1.setText('1')
	parent.c2_home_sequence_2.setText('0')

def sample_5i25_7i77(parent):
	parent.board_cb.setCurrentIndex(parent.board_cb.findText('5i25T'))
	parent.daughter_cb_2.setCurrentIndex(parent.daughter_cb_2.findText('7i77'))
	set_joints(parent, 2, ['X', 'Y', 'Z'], 'servo')
	parent.c2_home_sequence_0.setText('2')
	parent.c2_home_sequence_1.setText('1')
	parent.c2_home_sequence_2.setText('0')

def sample_7i76eu(parent):
	parent.board_cb.setCurrentIndex(parent.board_cb.findText('7i76EU'))
	parent.address_cb.setCurrentIndex(parent.address_cb.findData('10.10.10.10'))
	set_joints(parent, 0, ['X', 'Y', 'Z'], 'stepper')
	parent.c0_home_sequence_0.setText('2')
	parent.c0_home_sequence_1.setText('1')
	parent.c0_home_sequence_2.setText('0')

def sample_7i92t_7i76(parent):
	parent.board_cb.setCurrentIndex(parent.board_cb.findText('7i92T'))
	parent.address_cb.setCurrentIndex(parent.address_cb.findData('10.10.10.10'))
	parent.daughter_cb_2.setCurrentIndex(parent.daughter_cb_2.findText('7I76'))
	set_joints(parent, 2, ['X', 'Y', 'Z'], 'stepper')
	parent.c2_home_sequence_0.setText('2')
	parent.c2_home_sequence_1.setText('1')
	parent.c2_home_sequence_2.setText('0')

def sample_7i92t_7i77(parent):
	parent.board_cb.setCurrentIndex(parent.board_cb.findText('7i92T'))
	parent.address_cb.setCurrentIndex(parent.address_cb.findData('10.10.10.10'))
	parent.daughter_cb_2.setCurrentIndex(parent.daughter_cb_2.findText('7I77'))
	set_joints(parent, 2, ['X', 'Y', 'Z'], 'servo')
	parent.c2_home_sequence_0.setText('2')
	parent.c2_home_sequence_1.setText('1')
	parent.c2_home_sequence_2.setText('0')

def sample_7i95t(parent):
	parent.board_cb.setCurrentIndex(parent.board_cb.findText('7i95T'))
	parent.address_cb.setCurrentIndex(parent.address_cb.findData('10.10.10.10'))
	set_joints(parent, 0, ['X', 'Y', 'Z'], 'stepper')
	parent.c0_home_sequence_0.setText('2')
	parent.c0_home_sequence_1.setText('1')
	parent.c0_home_sequence_2.setText('0')

def sample_7i96s(parent):
	parent.board_cb.setCurrentIndex(parent.board_cb.findText('7i96S'))
	parent.address_cb.setCurrentIndex(parent.address_cb.findData('10.10.10.10'))
	set_joints(parent, 0, ['X', 'Y', 'Z'], 'stepper')
	parent.c0_home_sequence_0.setText('2')
	parent.c0_home_sequence_1.setText('1')
	parent.c0_home_sequence_2.setText('0')

def sample_7i97t(parent):
	parent.board_cb.setCurrentIndex(parent.board_cb.findText('7i97T'))
	parent.address_cb.setCurrentIndex(parent.address_cb.findData('10.10.10.10'))
	set_joints(parent, 0, ['X', 'Y', 'Z'], 'servo')
	parent.c0_home_sequence_0.setText('2')
	parent.c0_home_sequence_1.setText('1')
	parent.c0_home_sequence_2.setText('0')


def set_joints(parent, card, axes, drive_type):
	# value = <value_if_true> if <expression> else <value_if_false>
	mb = parent.board_cb.currentText()
	p1 = parent.daughter_cb_1.currentData()
	p2 = parent.daughter_cb_2.currentData()
	mb = mb if mb else ''
	p1 = f' P1-{p1}' if p1 else ''
	p2 = f' P2-{p2}' if p2 else ''
	name = mb if mb else ''
	for joint, axis in enumerate(axes):
		getattr(parent, f'c{card}_scale_{joint}').setText('1000')
		getattr(parent, f'c{card}_axis_{joint}').setCurrentIndex(getattr(parent, f'c0_axis_{joint}').findText(axis))
		if axis == 'Z':
			getattr(parent, f'c{card}_min_limit_{joint}').setText('-5')
			getattr(parent, f'c{card}_max_limit_{joint}').setText('0')
		else:
			getattr(parent, f'c{card}_min_limit_{joint}').setText('0')
			getattr(parent, f'c{card}_max_limit_{joint}').setText('10')
		getattr(parent, f'c{card}_max_vel_{joint}').setText('1')
		getattr(parent, f'c{card}_max_accel_{joint}').setText('4')
		getattr(parent, f'c{card}_pid_default_{joint}').click()
		getattr(parent, f'c{card}_ferror_default_{joint}').click()
		# FIXME this is only for stepper drive neeed different for analog boards
		if drive_type == 'stepper':
			index = getattr(parent, f'c{card}_drive_{joint}').findText('Gecko 203v')
			getattr(parent, f'c{card}_drive_{joint}').setCurrentIndex(index)
		elif drive_type == 'servo':
			getattr(parent, f'c{card}_analog_default_{joint}').click()
			getattr(parent, f'c{card}_encoder_scale_{joint}').setText('2500')
	parent.machine_name_le.setText(f'{mb}{p1}{p2}')



