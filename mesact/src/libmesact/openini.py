import os

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QComboBox, QLabel, QLineEdit, QSpinBox
from PyQt6.QtWidgets import QDoubleSpinBox, QCheckBox, QRadioButton

from libmesact import dialogs

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
		mesa['BOARD_NAME'] = 'boardCB'
		mesa['FIRMWARE'] = 'firmwareCB'
		mesa['CARD_0'] = 'daughterCB_0'
		mesa['CARD_1'] = 'daughterCB_1'

		start = sections['[MESA]'][0]
		end = sections['[MESA]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in mesa and value not in ['Select', 'None']:
					update(parent, mesa[key], value)

	if '[EMC]' in sections:
		emc = {}
		emc['MACHINE'] = 'configNameLE'
		emc['DEBUG'] = 'debugCB'

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
		display['DISPLAY'] = 'guiCB'
		display['EDITOR'] = 'editorCB'
		display['POSITION_OFFSET'] = 'positionOffsetCB'
		display['POSITION_FEEDBACK'] = 'positionFeedbackCB'
		display['MAX_FEED_OVERRIDE'] = 'maxFeedOverrideSB'
		display['MIN_VELOCITY'] = 'minLinJogVelDSB'
		display['DEFAULT_LINEAR_VELOCITY'] = 'defLinJogVelDSB'
		display['MAX_LINEAR_VELOCITY'] = 'maxLinJogVelDSB'
		display['MIN_ANGULAR_VELOCITY'] = 'minAngJogVelDSB'
		display['DEFAULT_ANGULAR_VELOCITY'] = 'defAngJogVelDSB'
		display['MAX_ANGULAR_VELOCITY'] = 'maxAngJogVelDSB'
		display['INCREMENTS'] = 'jog_increments'
		display['LATHE'] = 'frontToolLatheRB'
		display['BACK_TOOL_LATHE'] = 'backToolLatheRB'
		display['FOAM'] = 'foamRB'

		start = sections['[DISPLAY]'][0]
		end = sections['[DISPLAY]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in display and value not in ['Select', 'None']:
					update(parent, display[key], value)



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




