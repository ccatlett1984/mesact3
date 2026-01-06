import os

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QComboBox, QLabel, QLineEdit, QSpinBox
from PyQt6.QtWidgets import QDoubleSpinBox, QCheckBox, QRadioButton
from PyQt6.QtWidgets import QPushButton, QGroupBox

from libmesact import dialogs
from libmesact import utilities

def load_ini(parent, ini_file=None):
	if not ini_file:
		home_dir = os.path.expanduser("~")
		config_dir = os.path.join(home_dir, 'linuxcnc/configs')
		if not os.path.isdir(config_dir):
			config_dir = home_dir
		ini_file, _ = QFileDialog.getOpenFileName(parent, "Select INI File",
			config_dir, '*.ini')

	if not ini_file:
		return

	with open(ini_file, 'r') as file:
		ini_list = file.readlines() # create a list of strings

	# get start and stop indexes of each section
	# starting at the end and working back to the start
	file_length = len(ini_list)-1
	sections = {}
	start = 0
	end = len(ini_list)-1
	for index, line in enumerate(reversed(ini_list)):
		if line.startswith('['):
			sections[line.strip()] = [file_length - index, end]
			end = (file_length - index) - 1

	# reverse backwards built dictionary
	sections = dict(reversed(sections.items()))

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
		mesa['CARD_1'] = 'daughter_cb_1'
		mesa['CARD_2'] = 'daughter_cb_2'

		start = sections['[MESA]'][0]
		end = sections['[MESA]'][1]
		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in mesa and value not in ['Select', 'None']:
					update(parent, mesa[key], value)

	if '[EMC]' in sections:
		start = sections['[EMC]'][0]
		end = sections['[EMC]'][1]

		emc = {}
		emc['MACHINE'] = 'machine_name_le'
		emc['DEBUG'] = 'debug_cb'

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
		start = sections['[HM2]'][0]
		end = sections['[HM2]'][1]

		hm2 = {}
		hm2['ADDRESS'] = 'address_cb'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in hm2 and value not in ['Select', 'None']:
					update(parent, hm2[key], value)

	if '[DISPLAY]' in sections:
		start = sections['[DISPLAY]'][0]
		end = sections['[DISPLAY]'][1]

		display = {}
		display['DISPLAY'] = 'gui_cb'
		display['GUI'] = 'flex_gui_le'
		display['EDITOR'] = 'editor_cb'
		display['POSITION_OFFSET'] = 'position_offset_cb'
		display['POSITION_FEEDBACK'] = 'position_feedback_cb'
		display['MAX_FEED_OVERRIDE'] = 'max_feed_override_dsb'
		display['MIN_VELOCITY'] = 'min_lin_jog_vel_dsb'
		display['DEFAULT_LINEAR_VELOCITY'] = 'default_lin_jog_vel_dsb'
		display['MAX_LINEAR_VELOCITY'] = 'max_lin_jog_vel_dsb'
		display['MIN_ANGULAR_VELOCITY'] = 'min_ang_jog_vel_dsb'
		display['DEFAULT_ANGULAR_VELOCITY'] = 'default_ang_jog_vel_dsb'
		display['MAX_ANGULAR_VELOCITY'] = 'max_ang_jog_vel_dsb'
		display['INCREMENTS'] = 'jog_increments'
		display['LATHE'] = 'front_tool_lathe_rb'
		display['BACK_TOOL_LATHE'] = 'backtool_lathe_rb'
		display['FOAM'] = 'foam_rb'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in display and value not in ['Select', 'None']:
					update(parent, display[key], value)

	# FILTER

	# RS274NGC

	# EMCMOT
	if '[EMCMOT]' in sections:
		start = sections['[EMCMOT]'][0]
		end = sections['[EMCMOT]'][1]

		emcot = {}
		emcot['SERVO_PERIOD'] = 'servo_period_sb'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in emcot and value not in ['Select', 'None']:
					update(parent, emcot[key], value)

	# TASK

	# HAL
	if '[HAL]' in sections:
		start = sections['[HAL]'][0]
		end = sections['[HAL]'][1]

		hal_files = {}
		#hal_files['HALFILE'] = 'custom_hal_cb'
		hal_files['POSTGUI_HALFILE'] = 'postgui_hal_cb'
		hal_files['SHUTDOWN'] = 'shutdown_hal_cb'
		hal_files['HALUI'] = 'halui_cb'

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
						utilities.add_mdi_row(parent)
					getattr(parent, f'mdi_le_{row}').setText(value)
					row += 1

	# APPLICATIONS

	# TRAJ # FIXME there are more options for traj
	if '[TRAJ]' in sections:
		start = sections['[TRAJ]'][0]
		end = sections['[TRAJ]'][1]

		traj_dict = {}
		traj_dict['LINEAR_UNITS'] = 'linear_units_cb'
		traj_dict['MAX_LINEAR_VELOCITY'] = 'traj_max_lin_vel_dsb'
		traj_dict['NO_FORCE_HOMING'] = 'no_force_homing_cb'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in traj_dict and value not in ['Select', 'None']:
					update(parent, traj_dict[key], value)

	# KINS

	# AXIS_

	# JOINT_
	for section in sections:
		if section.startswith('[JOINT_'):
			joint = section[-2].strip()

			start = sections[f'[JOINT_{joint}]'][0]
			end = sections[f'[JOINT_{joint}]'][1]

			for item in ini_list[start + 1:end + 1]:
				# CARD is the Board Tab
				# TAB is the Drive
				if item.startswith('BOARD'):
					key, value = [part.strip() for part in item.split('=', 1)]
					board = value
				elif item.startswith('DRIVE'):
					key, value = [part.strip() for part in item.split('=', 1)]
					joint = value

			joint_dict = {}
			joint_dict['AXIS'] = f'c{board}_axis_{joint}'
			joint_dict['SCALE'] = f'c{board}_scale_{joint}'
			joint_dict['MIN_LIMIT'] = f'c{board}_min_limit_{joint}'
			joint_dict['MAX_LIMIT'] = f'c{board}_max_limit_{joint}'
			joint_dict['MAX_VELOCITY'] = f'c{board}_max_vel_{joint}'
			joint_dict['MAX_ACCELERATION'] = f'c{board}_max_accel_{joint}'
			joint_dict['P'] = f'c{board}_p_{joint}'
			joint_dict['I'] = f'c{board}_i_{joint}'
			joint_dict['D'] = f'c{board}_d_{joint}'
			joint_dict['FF0'] = f'c{board}_ff0_{joint}'
			joint_dict['FF1'] = f'c{board}_ff1_{joint}'
			joint_dict['FF2'] = f'c{board}_ff2_{joint}'
			joint_dict['DEADBAND'] = f'c{board}_deadband_{joint}'
			joint_dict['BIAS'] = f'c{board}_bias_{joint}'
			joint_dict['MAX_OUTPUT'] = f'c{board}_max_output_{joint}'
			joint_dict['MAX_ERROR'] = f'c{board}_max_error_{joint}'
			joint_dict['MIN_FERROR'] = f'c{board}_min_ferror_{joint}'
			joint_dict['MAX_FERROR'] = f'c{board}_max_ferror_{joint}'

			joint_dict['HOME'] = f'c{board}_home_{joint}'
			joint_dict['HOME_OFFSET'] = f'c{board}_home_offset_{joint}'
			joint_dict['HOME_SEARCH_VEL'] = f'c{board}_home_search_vel_{joint}'
			joint_dict['HOME_LATCH_VEL'] = f'c{board}_home_latch_vel_{joint}'
			joint_dict['HOME_FINAL_VEL'] = f'c{board}_home_final_vel_{joint}'
			joint_dict['HOME_SEQUENCE'] = f'c{board}_home_sequence_{joint}'
			joint_dict['HOME_USE_INDEX'] = f'c{board}_home_use_index_{joint}'
			joint_dict['HOME_IS_SHARED'] = f'c{board}_home_switch_shared_{joint}'
			joint_dict['HOME_IGNORE_LIMITS'] = f'c{board}_home_ignore_limits_{joint}'

			joint_dict['STEP_DRIVE'] = f'c{board}_drive_{joint}'
			joint_dict['STEP_LEN'] = f'c{board}_step_time_{joint}'
			joint_dict['STEP_SPACE'] = f'c{board}_step_space_{joint}'
			joint_dict['DIR_SETUP'] = f'c{board}_dir_setup_{joint}'
			joint_dict['DIR_HOLD'] = f'c{board}_dir_hold_{joint}'
			joint_dict['STEP_INVERT'] = f'c{board}_step_invert_{joint}'
			joint_dict['DIR_INVERT'] = f'c{board}_dir_invert_{joint}'

			joint_dict['ANALOG_MIN_LIMIT'] = f'c{board}_analog_min_limit_{joint}'
			joint_dict['ANALOG_MAX_LIMIT'] = f'c{board}_analog_max_limit_{joint}'
			joint_dict['ANALOG_SCALE_MAX'] = f'c{board}_analog_scale_max_{joint}'
			joint_dict['ENCODER_SCALE'] = f'c{board}_encoder_scale_{joint}'

			for item in ini_list[start + 1:end + 1]:
				if '=' in item:
					key, value = [part.strip() for part in item.split('=', 1)]
					if key in joint_dict and value not in ['Select', 'None']:
						update(parent, joint_dict[key], value)

	# SPINDLE_
	if '[SPINDLE_0]' in sections:
		start = sections['[SPINDLE_0]'][0]
		end = sections['[SPINDLE_0]'][1]

		spindle_dict = {}
		spindle_dict['P'] = 'p_s'
		spindle_dict['I'] = 'i_s'
		spindle_dict['D'] = 'd_s'
		spindle_dict['FF0'] = 'ff0_s'
		spindle_dict['FF1'] = 'ff1_s'
		spindle_dict['FF2'] = 'ff2_s'
		spindle_dict['BIAS'] = 'bias_s'
		spindle_dict['DEADBAND'] = 'deadband_s'
		spindle_dict['MAX_OUTPUT'] = 'spindle_rpm_le'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in spindle_dict and value not in ['Select', 'None']:
					update(parent, spindle_dict[key], value)

		for item in ini_list[start + 1:end + 1]:
			if item.startswith('OUTPUT_SCALE'):
				update(parent, 'spindle_dir_cb', 'True')


	# EMCIO

	# INPUTS
	if '[INPUTS]' in sections:
		start = sections[f'[INPUTS]'][0]
		end = sections[f'[INPUTS]'][1]

		input_dict = {}
		for i in range(3):
			for j in range(32):
				input_dict[f'INPUT_{i}_{j}'] = f'c{i}_input_{j}'
				input_dict[f'INPUT_INVERT_{i}_{j}'] = f'c{i}_input_invert_{j}'
				input_dict[f'INPUT_SLOW_{i}_{j}'] = f'c{i}_input_debounce_{j}'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				#print(input_dict[key], value)
				if key in input_dict and value not in ['Select', 'None']:
					update(parent, input_dict[key], value)

	# OUTPUTS
	if '[OUTPUTS]' in sections:
		start = sections[f'[OUTPUTS]'][0]
		end = sections[f'[OUTPUTS]'][1]

		output_dict = {}
		for i in range(3):
			for j in range(16):
				output_dict[f'OUTPUT_{i}_{j}'] = f'c{i}_output_{j}'
				output_dict[f'OUTPUT_INVERT_{i}_{j}'] = f'c{i}_output_invert_{j}'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				#print(input_dict[key], value)
				if key in output_dict and value not in ['Select', 'None']:
					update(parent, output_dict[key], value)

			sink = ''
			source = ''
			for item in ini_list[start + 1:end + 1]:
				if item.strip().startswith('OUTPUT_SINK') and '=' in item:
					sink = item.split('=')[1].strip()
				if item.strip().startswith('OUTPUT_SOURCE') and '=' in item:
					source = item.split('=')[1].strip()
			if len(sink) == 16 and len(source) == 16:
				for i in range(16):
					if sink[i] == '1' and source[i] == '0': # sink
						getattr(parent, f'c0_output_type_{i}').setCurrentIndex(1)
					elif sink[i] == '1' and source[i] == '1': # push pull
						getattr(parent, f'c0_output_type_{i}').setCurrentIndex(2)

	# OPTIONS
	if '[OPTIONS]' in sections:
		start = sections[f'[OPTIONS]'][0]
		end = sections[f'[OPTIONS]'][1]

		options_dict = {}
		options_dict['LOAD_CONFIG'] = 'load_config_cb'
		options_dict['INTRO_GRAPHIC'] = 'intro_graphic_le'
		options_dict['INTRO_GRAPHIC_TIME'] = 'splash_screen_sb'
		options_dict['MANUAL_TOOL_CHANGE'] = 'manual_tool_change_cb'
		options_dict['PYVCP'] = 'pyvcp_cb'
		options_dict['LADDER'] = 'ladder_gb'
		options_dict['BACKUP'] = 'backup_cb'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				#print(input_dict[key], value)
				if key in options_dict and value not in ['Select', 'None']:
					update(parent, options_dict[key], value)

	# PLC
	if '[PLC]' in sections:
		start = sections[f'[PLC]'][0]
		end = sections[f'[PLC]'][1]

		update(parent, 'ladder_gb', 'True')
		plc_dict = {}
		plc_dict['LADDER_RUNGS'] = 'ladder_rungs_sb'
		plc_dict['LADDER_BITS'] = 'ladder_bits_sb'
		plc_dict['LADDER_WORDS'] = 'ladder_words_sb'
		plc_dict['LADDER_TIMERS'] = 'ladder_timers_sb'
		plc_dict['LADDER_IEC_TIMERS'] = 'ladder_iec_timer_sb'
		plc_dict['LADDER_MONOSTABLES'] = 'ladder_monostables_sb'
		plc_dict['LADDER_COUNTERS'] = 'ladder_counters_sb'
		plc_dict['LADDER_HAL_INPUTS'] = 'ladder_inputs_sb'
		plc_dict['LADDER_HAL_OUTPUTS'] = 'ladder_outputs_sb'
		plc_dict['LADDER_FLOAT_INPUTS'] = 'ladder_float_inputs_sb'
		plc_dict['LADDER_FLOAT_OUTPUTS'] = 'ladder_float_outputs_sb'
		plc_dict['LADDER_S32_INPUTS'] = 'ladder_s32_inputs_sb'
		plc_dict['LADDER_S32_OUTPUTS'] = 'ladder_s32_ouputs_sb'
		plc_dict['LADDER_SECTIONS'] = 'ladder_sections_sb'
		plc_dict['LADDER_SYMBOLS'] = 'ladder_symbols_sb'
		plc_dict['LADDER_EXPRESSIONS'] = 'ladder_expresions_sb'

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key in plc_dict and value not in ['Select', 'None']:
					update(parent, plc_dict[key], value)

	# SSERIAL
	if '[SSERIAL]' in sections:
		start = sections[f'[SSERIAL]'][0]
		end = sections[f'[SSERIAL]'][1]

		for item in ini_list[start + 1:end + 1]:
			if '=' in item:
				key, value = [part.strip() for part in item.split('=', 1)]
				if key == 'SS_CARD':
					update(parent, 'ss_card_cb', value)
				elif key.startswith('ss'):
					update(parent, key, value)

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
	elif isinstance(getattr(parent, obj), QPushButton):
		getattr(parent, obj).setText(value)
	elif isinstance(getattr(parent, obj), QGroupBox):
		getattr(parent, obj).setChecked(booleanDict[value.lower()])
	else:
		print(f'Unknown object {obj}')




