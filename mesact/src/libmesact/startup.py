import os

from libmesact import openini

def setup_vars(parent):
	parent.config_path = ''

def hide_tabs(parent):
	# set main tab visibility
	parent.main_tw.setTabVisible(3, False)
	parent.main_tw.setTabVisible(4, False)
	parent.main_tw.setTabVisible(5, False)
	parent.main_tw.setTabVisible(6, False)

def disable_controls(parent):
	parent.mdi_commands_gb.setEnabled(False)

def load_ini(parent):
	if parent.settings.contains('STARTUP/config'):
		if parent.settings.value('STARTUP/config', False, type=bool):
			config_file = parent.settings.value('STARTUP/config')
			if os.path.isfile(config_file):
				openini.load_ini(parent, config_file)


def test(parent):
	parent.machine_name_le.setText('Mesa CT 3')
	parent.board_cb.setCurrentIndex(6)
	parent.address_cb.setCurrentIndex(1)
	parent.gui_cb.setCurrentIndex(1)
	parent.linear_units_cb.setCurrentIndex(1)
	parent.position_offset_cb.setCurrentIndex(1)
	parent.position_feedback_cb.setCurrentIndex(1)
	parent.def_lin_jog_vel_dsb.setValue(0.1)
	set_joints(parent, 0, ['X', 'Y', 'Z'])

def set_joints(parent, card, axes):
	# value = <value_if_true> if <expression> else <value_if_false>
	#mb = parent.boardCB.currentText()
	#p1 = parent.daughterCB_0.currentData()
	#p2 = parent.daughterCB_1.currentData()
	#mb = mb if mb else ''
	#p1 = f' P1-{p1}' if p1 else ''
	#p2 = f' P2-{p2}' if p2 else ''
	#name = mb if mb else ''
	for joint, axis in enumerate(axes):
		getattr(parent, f'c{card}_scale_{joint}').setText('1000')
		getattr(parent, f'c{card}_axis_{joint}').setCurrentIndex(getattr(parent, f'c0_axis_{joint}').findData(axis))
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
		getattr(parent, f'c{card}_drive_{joint}').setCurrentIndex(getattr(parent, f'c{card}_drive_{joint}').findText('Gecko 203v'))
	#parent.configNameLE.setText(f'{mb}{p1}{p2} {parent.coordinatesLB.text()}')



