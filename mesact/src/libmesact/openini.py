import os

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QComboBox, QLabel, QLineEdit, QSpinBox
from PyQt6.QtWidgets import QDoubleSpinBox, QCheckBox, QRadioButton

from libmesact import dialogs
from libmesact import utilities

def open_ini(parent):
	home_dir = os.path.expanduser("~")
	config_dir = os.path.join(home_dir, 'linuxcnc/configs')
	if not os.path.isdir(config_dir):
		config_dir = home_dir
	ini_file, _ = QFileDialog.getOpenFileName(parent, "Select INI File",
		config_dir, '*.ini')

	with open(ini_file, 'r') as file:
		ini_list = file.readlines() # create a list of strings

	# get start and stop indexes of each section
	file_length = len(ini_list)-1
	sections = {}
	start = 0
	end = len(ini_list)-1
	for index, line in enumerate(reversed(ini_list)):
		if line.startswith('['):
			sections[line.strip()] = [file_length - index, end]
			end = (file_length - index) - 1

	if 'Mesa' not in ini_list[0] or '[MESA]' not in sections:
		msg = (f'The INI file {os.path.basename(ini_file)}\n'
		'Does not appear to be built with the\n'
		'Mesa Configuration Tool.')
		dialogs.msg_error_ok(parent, msg, 'File not Valid')
		return

	if '[MESA]' in sections:
		mesa = {}
		mesa['BOARD_NAME'] = 'board_cb'
		mesa['FIRMWARE'] = 'firmware_cb'
		mesa['CARD_1'] = 'daughter_1_cb'
		mesa['CARD_2'] = 'daughter_2_cb'

		start = sections['[MESA]'][0]
		end = sections['[MESA]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in mesa and value not in ['Select', 'None']:
					update(parent, mesa[key], value)

	if '[EMC]' in sections:
		emc = {}
		emc['MACHINE'] = 'machine_name_le'
		emc['DEBUG'] = 'debug_cb'

		start = sections['[EMC]'][0]
		end = sections['[EMC]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in emc and value not in ['Select', 'None']:
					update(parent, emc[key], value)

	'''
	hm2 = [
	['[HM2]', 'ADDRESS', 'address_cb'],
	['[HM2]', 'STEPGENS', 'stepgens_cb'],
	['[HM2]', 'PWMGENS', 'pwmgens_cb'],
	['[HM2]', 'ENCODERS', 'encoders_cb']
	]
	'''

	if '[HM2]' in sections:
		hm2 = {}
		hm2['ADDRESS'] = 'address_cb'

		start = sections['[HM2]'][0]
		end = sections['[HM2]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in hm2 and value not in ['Select', 'None']:
					update(parent, hm2[key], value)

	if '[DISPLAY]' in sections:
		display = {}
		display['DISPLAY'] = 'gui_cb'
		display['EDITOR'] = 'editor_cb'
		display['POSITION_OFFSET'] = 'position_offset_cb'
		display['POSITION_FEEDBACK'] = 'position_feedback_cb'
		display['MAX_FEED_OVERRIDE'] = 'max_feed_override_sb'
		display['MIN_VELOCITY'] = 'min_lin_jog_vel_dsb'
		display['DEFAULT_LINEAR_VELOCITY'] = 'def_lin_jog_vel_dsb'
		display['MAX_LINEAR_VELOCITY'] = 'max_lin_jog_vel_dsb'
		display['MIN_ANGULAR_VELOCITY'] = 'min_ang_jog_vel_dsb'
		display['DEFAULT_ANGULAR_VELOCITY'] = 'def_ang_jog_vel_dsb'
		display['MAX_ANGULAR_VELOCITY'] = 'def_ang_jog_vel_dsb'
		display['INCREMENTS'] = 'jog_increments'
		display['LATHE'] = 'front_tool_lathe_rb'
		display['BACK_TOOL_LATHE'] = 'backtool_lathe_rb'
		display['FOAM'] = 'foam_rb'

		start = sections['[DISPLAY]'][0]
		end = sections['[DISPLAY]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in display and value not in ['Select', 'None']:
					update(parent, display[key], value)

	# FILTER

	# RS274NGC

	# EMCMOT
	if '[EMCMOT]' in sections:
		emcot = {}
		emcot['SERVO_PERIOD'] = 'servo_period_sb'
		start = sections['[EMCMOT]'][0]
		end = sections['[EMCMOT]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in emcot and value not in ['Select', 'None']:
					update(parent, emcot[key], value)


	# TASK

	# HAL
	if '[HAL]' in sections:
		hal_files = {}
		#hal_files['HALFILE'] = 'custom_hal_cb'
		hal_files['POSTGUI_HALFILE'] = 'postgui_hal_cb'
		hal_files['SHUTDOWN'] = 'shutdown_hal_cb'
		hal_files['HALUI'] = 'halui_cb'
		start = sections['[HAL]'][0]
		end = sections['[HAL]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in hal_files and value not in ['Select', 'None']:
					update(parent, hal_files[key], 'True')
				elif key == 'HALFILE' and value == 'custom.hal':
					update(parent, 'custom_hal_cb' , 'True')

	# HALUI
	if '[HALUI]' in sections:
		start = sections['[HALUI]'][0]
		end = sections['[HALUI]'][1]
		row = 0
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key == 'MDI_COMMAND' and value not in ['Select', 'None']:
					if not parent.findChildren(QLineEdit, f'mdi_le_{row}'):
						print('adding row')
						utilities.add_mdi_row(parent)
					else:
						print(f'QLineEdit mdi_le_{row} found')
					getattr(parent, f'mdi_le_{row}').setText(value)
					row += 1



	# APPLICATIONS

	# TRAJ

	# KINS

	# AXIS_

	# JOINT_

	# SPINDLE_

	# EMCIO

def update(parent, obj, value):
	booleanDict = {'true': True, 'yes': True, '1': True,
		'false': False, 'no': False, '0': False,}
	if isinstance(getattr(parent, obj), QComboBox):
		index = 0
		if getattr(parent, obj).findData(value) >= 0:
			index = getattr(parent, obj).findData(value)
		elif getattr(parent, obj).findText(value) >= 0:
			index = getattr(parent, obj).findText(value)
		if index >= 0:
			getattr(parent, obj).setCurrentIndex(index)
	elif isinstance(getattr(parent, obj), QLabel):
		getattr(parent, obj).setText(value)
	elif isinstance(getattr(parent, obj), QLineEdit):
		getattr(parent, obj).setText(value)
	elif isinstance(getattr(parent, obj), QSpinBox):
		getattr(parent, obj).setValue(int(value))
	elif isinstance(getattr(parent, obj), QDoubleSpinBox):
		getattr(parent, obj).setValue(float(value))
	elif isinstance(getattr(parent, obj), QCheckBox):
		getattr(parent, obj).setChecked(booleanDict[value.lower()])
	elif isinstance(getattr(parent, obj), QRadioButton):
		getattr(parent, obj).setChecked(booleanDict[value.lower()])
	else:
		print('Unknown object')




