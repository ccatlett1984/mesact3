import traceback

from datetime import datetime

from PyQt6.QtWidgets import QSpinBox, QPushButton

def build(parent):
	parent.info_pte.appendPlainText(f'Building {parent.ini_path}')

	contents = ['# This file was created with the Mesa Configuration Tool on ']
	contents.append(f'{datetime.now().strftime("%b %d %Y %H:%M:%S")}\n')
	contents.append('# Changes to most things are ok and will be read by the Configuration Tool\n')

	# build the [MESA] section
	contents.append('\n[MESA]\n')
	contents.append(f'VERSION = {parent.version}\n')
	contents.append(f'BOARD_NAME = {parent.board_cb.currentText()}\n')
	if parent.firmware_cb.currentData():
		contents.append(f'FIRMWARE = {parent.firmware_cb.currentData()}\n')
	if parent.daughter_cb_1.currentData():
		contents.append(f'DAUGHTER_1 = {parent.daughter_cb_1.currentText()}\n')
	if parent.daughter_cb_2.currentData():
		contents.append(f'DAUGHTER_2 = {parent.daughter_cb_2.currentText()}\n')

	# build the [EMC] section
	contents.append('\n[EMC]\n')
	contents.append('# VERSION is used by the LinuxCNC startup script\n')
	contents.append(f'VERSION = 1.1\n')
	contents.append(f'EMC_VERSION = {parent.emc_version}\n')
	contents.append(f'MACHINE = {parent.machine_name_le.text()}\n')
	contents.append(f'DEBUG = {parent.debug_cb.currentData()}\n')

	# build the [HM2] section
	contents.append('\n[HM2]\n')
	if parent.board_interface == 'eth':
		contents.append('DRIVER = hm2_eth\n')
		contents.append(f'ADDRESS = {parent.address_cb.currentText()}\n')
	elif parent.board_interface == 'pci':
		contents.append('DRIVER = hm2_pci\n')
	elif parent.board_interface == 'spi':
		contents.append('DRIVER = hm2_spix\n')
		contents.append(f'ADDRESS = {parent.address_cb.currentText()}\n')

	# build the [DISPLAY] section
	contents.append('\n[DISPLAY]\n')
	if not parent.gui_cb.currentData(): # use the user gui
		contents.append(f'DISPLAY = {parent.gui_cb.currentText()}\n')
	else:
		contents.append(f'DISPLAY = {parent.gui_cb.currentData()}\n')
	# Flex GUI
	if parent.gui_cb.currentData() == 'flexgui':
		contents.append(f'GUI = {parent.flex_gui_le.text()}\n')

	contents.append(f'PROGRAM_PREFIX = ~/linuxcnc/nc_files\n')

	if parent.gui_cb.currentData() == 'axis':
		contents.append(f'INTRO_GRAPHIC = {parent.intro_graphic_le.text()}\n')
		contents.append(f'INTRO_TIME = {parent.splash_screen_sb.value()}\n')
		contents.append(f'OPEN_FILE = "{parent.startup_file_le.text()}"\n')

	if parent.max_feed_override_dsb.value() > 0:
		contents.append(f'MAX_FEED_OVERRIDE = {parent.max_feed_override_dsb.value():.1f}\n')
	if parent.min_lin_jog_vel_dsb.value() > 0:
		contents.append(f'MIN_LINEAR_VELOCITY = {parent.min_lin_jog_vel_dsb.value():.1f}\n')
	if parent.gui_cb.currentData() == 'axis':
		contents.append(f'DEFAULT_LINEAR_VELOCITY = {parent.default_lin_jog_vel_dsb.value():.1f}\n')
	if parent.max_lin_jog_vel_dsb.value() > 0:
		contents.append(f'MAX_LINEAR_VELOCITY = {parent.max_lin_jog_vel_dsb.value():.1f}\n')
	if parent.min_ang_jog_vel_dsb.value() > 0:
		contents.append(f'MIN_ANGULAR_VELOCITY = {parent.min_ang_jog_vel_dsb.value():.1f}\n')
	if parent.default_ang_jog_vel_dsb.value() > 0:
		contents.append(f'DEFAULT_ANGULAR_VELOCITY = {parent.default_ang_jog_vel_dsb.value():.1f}\n')
	if parent.max_ang_jog_vel_dsb.value() > 0:
		contents.append(f'MAX_ANGULAR_VELOCITY = {parent.max_ang_jog_vel_dsb.value():.1f}\n')
	if parent.jog_increments.text():
		contents.append(f'INCREMENTS = {parent.jog_increments.text()}\n')

	# required by Axis
	# INTRO_GRAPHIC = linuxcnc.gif
	# INTRO_TIME = 5
	# DEFAULT_LINEAR_VELOCITY = 0.250000
	# MAX_LINEAR_VELOCITY = 1.000000



	# FIXME these are in [FLEXGUI]
	if parent.keyboard_qss_cb.isChecked():
		contents.append(f'INPUT = keyboard\n')
	elif parent.touch_qss_cb.isChecked():
		contents.append(f'INPUT = touch\n')
	elif len(parent.custom_qss_le.text()) > 0:
		contents.append(f'QSS = {parent.custom_qss_le.text()}\n')
	if parent.flex_size_cb.currentData():
		contents.append(f'SIZE = {parent.flex_size_cb.currentData()}\n')

	if parent.editor_cb.currentData():
		contents.append(f'EDITOR = {parent.editor_cb.currentData()}\n')

	if parent.position_offset_cb.currentData():
		contents.append(f'POSITION_OFFSET = {parent.position_offset_cb.currentData()}\n')
	if parent.position_feedback_cb.currentData():
		contents.append(f'POSITION_FEEDBACK = {parent.position_feedback_cb.currentData()}\n')

	if parent.front_tool_lathe_rb.isChecked():
		contents.append('LATHE = 1\n')
	if parent.backtool_lathe_rb.isChecked():
		contents.append('BACK_TOOL_LATHE = 1\n')
	if parent.foam_rb.isChecked(): # FIXME this needs to be checked for correct coordinates
		contents.append(f'Geometry = {parent.coordinates_lb.text()[0:2]};{parent.coordinates_lb.text()[2:4]}\n')
		contents.append('FOAM = 1\n')

	# build the [FILTER] Section
	# build the [RS274NGC] Section
	contents.append('\n[RS274NGC]\n')
	contents.append(f'PARAMETER_FILE = parameters.var\n')
	if parent.subroutine_cb.isChecked():
		contents.append(f'SUBROUTINE_PATH = ~/linuxcnc/subroutines\n')

	# build the [EMCMOT] Section
	contents.append('\n[EMCMOT]\n')
	contents.append('EMCMOT = motmod\n')
	contents.append('COMM_TIMEOUT = 1.0\n')
	contents.append(f'SERVO_PERIOD = {parent.servo_period_sb.value()}\n')

	# build the [TASK] Section
	contents.append('\n[TASK]\n')
	contents.append('TASK = milltask\n')
	contents.append('CYCLE_TIME = 0.010\n')

	# build the [HAL] section
	contents.append('\n[HAL]\n')
	contents.append(f'HALFILE = main.hal\n')
	io = False
	for i in range(3):
		inputs = getattr(parent, f'c{i}_inputs_tw').findChildren(QPushButton)
		for item in inputs:
			if item.text() != 'Select':
				io = True
				break
	#c0_inputs_tw
	#c0_outputs_w
	if io:
		contents.append('HALFILE = io.hal\n')
	if parent.ss_card_cb.currentData():
		contents.append('HALFILE = sserial.hal\n')
	if parent.custom_hal_cb.isChecked():
		contents.append('HALFILE = custom.hal\n')
	if parent.postgui_hal_cb.isChecked():
		contents.append('POSTGUI_HALFILE = postgui.hal\n')
	if parent.shutdown_hal_cb.isChecked():
		contents.append('SHUTDOWN = shutdown.hal\n')
	if parent.halui_cb.isChecked():
		contents.append('HALUI = halui\n')

	# build the [HALUI] section
	if parent.halui_cb.isChecked():
		contents.append('\n[HALUI]\n')

		rows = parent.mdi_grid_layout.rowCount()
		for i in range(parent.mdi_grid_layout.rowCount()):
			item = parent.mdi_grid_layout.itemAtPosition(i, 1)
			cmd = item.widget().text()
			if cmd:
				contents.append(f'MDI_COMMAND = {cmd}\n')
			else:
				print('empty mdi command')

	# build the [APPLICATIONS] Section
	# build the [TRAJ] Section
	# required COORDINATES LINEAR_UNITS ANGULAR_UNITS MAX_LINEAR_VELOCITY
	contents.append('\n[TRAJ]\n')
	contents.append(f'COORDINATES = {parent.coordinates_lb.text()}\n')
	contents.append(f'LINEAR_UNITS = {parent.linear_units_cb.currentData()}\n')
	contents.append('ANGULAR_UNITS = degree\n')
	contents.append(f'MAX_LINEAR_VELOCITY = {parent.traj_max_lin_vel_dsb.value():.1f}\n')
	if parent.no_force_homing_cb.isChecked():
		contents.append(f'NO_FORCE_HOMING = 1\n')

	# build the [KINS] Section
	contents.append('\n[KINS]\n')
	if len(set(parent.coordinates_lb.text())) == len(parent.coordinates_lb.text()): # 1 joint for each axis
		contents.append(f'KINEMATICS = trivkins coordinates={parent.coordinates_lb.text()}\n')
	else: # more than one joint per axis
		contents.append(f'KINEMATICS = trivkins coordinates={parent.coordinates_lb.text()} kinstype=BOTH\n')
	contents.append(f'JOINTS = {len(parent.coordinates_lb.text())}\n')

	axes = []
	joint = 0
	for i in range(3):
		if getattr(parent, f'board_{i}_type') not in ['stepper', 'servo']:
			continue

		for j in range(6):
			if getattr(parent, f'c{i}_axis_{j}').currentData():
				axis = getattr(parent, f'c{i}_axis_{j}').currentText() # text is upper case
				if axis and axis not in axes: # new axis only add one of each axis
					axes.append(axis)
					# build the [AXIS_<letter>] Section
					contents.append(f'\n[AXIS_{axis}]\n')
					contents.append(f'MIN_LIMIT = {getattr(parent, f"c{i}_min_limit_{j}").text()}\n')
					contents.append(f'MAX_LIMIT = {getattr(parent, f"c{i}_max_limit_{j}").text()}\n')
					contents.append(f'MAX_VELOCITY = {getattr(parent, f"c{i}_max_vel_{j}").text()}\n')
					contents.append(f'MAX_ACCELERATION = {getattr(parent, f"c{i}_max_accel_{j}").text()}\n')

				# build the [JOINT_<num>] Section
				contents.append(f'\n[JOINT_{joint}]\n')
				contents.append(f'BOARD = {i}\n')
				contents.append(f'DRIVE = {j}\n')
				contents.append(f'AXIS = {getattr(parent, f"c{i}_axis_{j}").currentText()}\n')
				contents.append(f'SCALE = {getattr(parent, f"c{i}_scale_{j}").text()}\n')
				contents.append(f'MIN_LIMIT = {getattr(parent, f"c{i}_min_limit_{j}").text()}\n')
				contents.append(f'MAX_LIMIT = {getattr(parent, f"c{i}_max_limit_{j}").text()}\n')
				contents.append(f'MAX_VELOCITY = {getattr(parent, f"c{i}_max_vel_{j}").text()}\n')
				contents.append(f'MAX_ACCELERATION = {getattr(parent, f"c{i}_max_accel_{j}").text()}\n')
				contents.append(f'TYPE = {getattr(parent, f"c{i}_axis_type_{j}").text()}\n')

				# PID
				contents.append(f'\n# PID Settings\n')
				contents.append(f'P = {getattr(parent, f"c{i}_p_{j}").text()}\n')
				contents.append(f'I = {getattr(parent, f"c{i}_i_{j}").text()}\n')
				contents.append(f'D = {getattr(parent, f"c{i}_d_{j}").text()}\n')
				contents.append(f'FF0 = {getattr(parent, f"c{i}_ff0_{j}").text()}\n')
				contents.append(f'FF1 = {getattr(parent, f"c{i}_ff1_{j}").text()}\n')
				contents.append(f'FF2 = {getattr(parent, f"c{i}_ff2_{j}").text()}\n')
				contents.append(f'DEADBAND = {getattr(parent, f"c{i}_deadband_{j}").text()}\n')
				contents.append(f'BIAS = {getattr(parent, f"c{i}_bias_{j}").text()}\n')
				contents.append(f'MAX_OUTPUT = {getattr(parent, f"c{i}_max_output_{j}").text()}\n')
				contents.append(f'MAX_ERROR = {getattr(parent, f"c{i}_max_error_{j}").text()}\n')

				# Following Error 
				contents.append(f'\n# Following Error Settings\n')
				contents.append(f'FERROR = {getattr(parent, f"c{i}_max_ferror_{j}").text()}\n')
				contents.append(f'MIN_FERROR = {getattr(parent, f"c{i}_min_ferror_{j}").text()}\n')

				# Homing
				home_le = [
				['_home_', 'HOME'],
				['_home_offset_', 'HOME_OFFSET'],
				['_home_search_vel_', 'HOME_SEARCH_VEL'],
				['_home_latch_vel_', 'HOME_LATCH_VEL'],
				['_home_final_vel_', 'HOME_FINAL_VEL'],
				['_home_sequence_', 'HOME_SEQUENCE'],
				]

				for item in home_le:
					if getattr(parent, f'c{i}{item[0]}{j}').text():
						contents.append('\n# Homing Settings\n')
						break

				for item in home_le:
					text = getattr(parent, f'c{i}{item[0]}{j}').text()
					if text:
						contents.append(f'{item[1]} = {text}\n')

				home_cb = [
				['_home_ignore_limits_', 'HOME_IGNORE_LIMITS'],
				['_home_use_index_', 'HOME_USE_INDEX'],
				['_home_switch_shared_', 'HOME_IS_SHARED']
				]

				for item in home_cb:
					if getattr(parent, f'c{i}{item[0]}{j}').isChecked():
						contents.append(f'{item[1]} = True\n')

				# Stepper Drive
				if getattr(parent, f'board_{i}_type') == 'stepper':
					contents.append(f'\n# Stepper Drive Settings\n')
					contents.append(f'STEP_DRIVE = {getattr(parent, f"c{i}_drive_{j}").currentText()}\n')
					contents.append(f'STEP_LEN = {getattr(parent, f"c{i}_step_time_{j}").text()}\n')
					contents.append(f'STEP_SPACE = {getattr(parent, f"c{i}_step_space_{j}").text()}\n')
					contents.append(f'STEP_INVERT = {getattr(parent, f"c{i}_step_invert_{j}").isChecked()}\n')
					contents.append(f'DIR_SETUP = {getattr(parent, f"c{i}_dir_setup_{j}").text()}\n')
					contents.append(f'DIR_HOLD = {getattr(parent, f"c{i}_dir_hold_{j}").text()}\n')
					contents.append(f'DIR_INVERT = {getattr(parent, f"c{i}_dir_invert_{j}").isChecked()}\n')
					contents.append(f'STEPGEN_MAX_VEL = {float(getattr(parent, f"c{i}_max_vel_{j}").text()) * 1.2:.2f}\n')
					contents.append(f'STEPGEN_MAX_ACC = {float(getattr(parent, f"c{i}_max_accel_{j}").text()) * 1.2:.2f}\n')


				# Analog Drive
				if getattr(parent, f'board_{i}_type') == 'servo':
					contents.append(f'\n# Servo Drive Settings\n')
					contents.append(f'ANALOG_MIN_LIMIT = {getattr(parent, f"c{i}_analog_min_limit_{j}").text()}\n')
					contents.append(f'ANALOG_MAX_LIMIT = {getattr(parent, f"c{i}_analog_max_limit_{j}").text()}\n')
					contents.append(f'ANALOG_SCALE_MAX = {getattr(parent, f"c{i}_analog_scale_max_{j}").text()}\n')

				if getattr(parent, f'c{i}_encoder_scale_{j}').text(): # Encoder Scale
					contents.append(f'ENCODER_SCALE = {getattr(parent, f"c{i}_encoder_scale_{j}").text()}\n')

				joint += 1

	# build the [SPINDLE_<num>] Section(s)
	if parent.spindle_rpm_le.text():
		contents.append('\n[SPINDLE_0]\n')
		contents.append(f'P = {parent.p_s.cleanText()}\n')
		contents.append(f'I = {parent.i_s.cleanText()}\n')
		contents.append(f'D = {parent.d_s.cleanText()}\n')
		contents.append(f'FF0 = {parent.ff0_s.cleanText()}\n')
		contents.append(f'FF1 = {parent.ff1_s.cleanText()}\n')
		contents.append(f'FF2 = {parent.ff2_s.cleanText()}\n')
		contents.append(f'BIAS = {parent.bias_s.cleanText()}\n')
		contents.append(f'DEADBAND = {parent.deadband_s.cleanText()}\n')
		contents.append(f'MAX_OUTPUT = {int(parent.spindle_rpm_le.text())}\n')

		if parent.spindle_dir_cb.isChecked():
			contents.append(f'OUTPUT_SCALE = {int(parent.spindle_rpm_le.text())}\n')
			contents.append(f'OUTPUT_MIN_LIMIT = -{int(parent.spindle_rpm_le.text())}\n')
			contents.append(f'OUTPUT_MAX_LIMIT = {int(parent.spindle_rpm_le.text())}\n')


	# build the [EMCIO] Section
	contents.append('\n[EMCIO]\n')
	contents.append('EMCIO = iov2\n')
	contents.append('CYCLE_TIME = 0.100\n')
	contents.append('TOOL_TABLE = tool.tbl\n')

	# build the [INPUTS] section
	contents.append('\n[INPUTS]\n')
	contents.append('# DO NOT change the inputs they are used by the configuration tool\n')
	for i in range(3):
		if parent.main_tw.isTabVisible(i + 3): # if the board tab is visible
			if getattr(parent, f'c{i}_board_tw').isTabVisible(1):
				for j in range(32):
					if getattr(parent, f"c{i}_input_{j}").text() != 'Select': # only add inputs that are used
						contents.append(f'INPUT_{i}_{j} = {getattr(parent, f"c{i}_input_{j}").text()}\n')
						contents.append(f'INPUT_INVERT_{i}_{j} = {getattr(parent, f"c{i}_input_invert_{j}").isChecked()}\n')
						contents.append(f'INPUT_SLOW_{i}_{j} = {getattr(parent, f"c{i}_input_debounce_{j}").isChecked()}\n')

	# build the [OUTPUTS] section 
	contents.append('\n[OUTPUTS]\n')
	contents.append('# DO NOT change the outputs they are used by the configuration tool\n')

	for i in range(3):
		for j in range(16):
			if getattr(parent, f"c{i}_output_{j}").text() != 'Select': # only add outputs that are used
				contents.append(f'OUTPUT_{i}_{j} = {getattr(parent, f"c{i}_output_{j}").text()}\n')
				contents.append(f'OUTPUT_INVERT_{i}_{j} = {getattr(parent, f"c{i}_output_invert_{j}").isChecked()}\n')

	# boards with sink, source outputs
	sink_source_boards = ['7i76EU']
	if parent.board_cb.currentText() in sink_source_boards:
		sink = ''
		source = ''
		for i in range(16):
			sink += getattr(parent, f'c0_output_type_{i}').currentData()[0]
			source += getattr(parent, f'c0_output_type_{i}').currentData()[1]
		contents.append(f'OUTPUT_SINK = {sink}\n')
		contents.append(f'OUTPUT_SOURCE = {source}\n')

	# build the [OPTIONS] section
	contents.append('\n[OPTIONS]\n')
	contents.append('# DO NOT change the options they are used by the configuration tool\n')
	contents.append(f'LOAD_CONFIG = {parent.load_config_cb.isChecked()}\n')
	contents.append(f'MANUAL_TOOL_CHANGE = {parent.manual_tool_change_cb.isChecked()}\n')
	contents.append(f'CUSTOM_HAL = {parent.custom_hal_cb.isChecked()}\n')
	contents.append(f'POST_GUI_HAL = {parent.postgui_hal_cb.isChecked()}\n')
	contents.append(f'SHUTDOWN_HAL = {parent.shutdown_hal_cb.isChecked()}\n')
	contents.append(f'HALUI = {parent.halui_cb.isChecked()}\n')
	contents.append(f'PYVCP = {parent.pyvcp_cb.isChecked()}\n')
	contents.append(f'BACKUP = {parent.backup_cb.isChecked()}\n')

	# build the [PLC] section
	if parent.ladder_gb.isChecked(): # check for any options
		contents.append('\n[PLC]\n')
		contents.append('# DO NOT change the plc options they are used by the configuration tool\n')
		children = parent.ladder_gb.findChildren(QSpinBox)
		for child in children:
			if child.value() > 0:
				contents.append(f'{child.property("item")} = {child.value()}\n')

	# build the [SSERIAL] section
	if parent.ss_card_cb.currentData():
		contents.append('\n[SSERIAL]\n')
		contents.append('# DO NOT change the sserial they are used by the configuration tool\n')
		contents.append(f'HOST_BOARD = {parent.sserial_host_cb.currentText()}\n')
		contents.append(f'SSERIAL_BOARD = {parent.ss_card_cb.currentText()}\n')

	if parent.ss_card_cb.currentData() == '7i64':
		# 24 ss7i64in_
		# 24 ss7i64out_
		for i in range(24):
			if getattr(parent, f'ss7i64in_{i}').text() != 'Select':
				contents.append(f'ss7i64in_{i} = {getattr(parent, "ss7i64in_" + str(i)).text()}\n')
		for i in range(24):
			if getattr(parent, f'ss7i64out_{i}').text() != 'Select':
				contents.append(f'ss7i64out_{i} = {getattr(parent, "ss7i64out_" + str(i)).text()}\n')

	elif parent.ss_card_cb.currentData() == '7i69':
		# 24 ss7i69in_
		# 24 ss7i69out_
		for i in range(24):
			if getattr(parent, f'ss7i69in_{i}').text() != 'Select':
				contents.append(f'ss7i69in_{i} = {getattr(parent, "ss7i69in_" + str(i)).text()}\n')
		for i in range(24):
			if getattr(parent, f'ss7i69out_{i}').text() != 'Select':
				contents.append(f'ss7i69out_{i} = {getattr(parent, "ss7i69out_" + str(i)).text()}\n')

	elif parent.ss_card_cb.currentData() == '7i70':
		# 48 ss7i70in_
		for i in range(48):
			if getattr(parent, f'ss7i70in_{i}').text() != 'Select':
				contents.append(f'ss7i70in_{i} = {getattr(parent, "ss7i70in_" + str(i)).text()}\n')

	elif parent.ss_card_cb.currentData() == '7i71':
		# 48 ss7i71out_
		for i in range(48):
			if getattr(parent, f'ss7i71out_{i}').text() != 'Select':
				contents.append(f'ss7i71out_{i} = {getattr(parent, "ss7i71out_" + str(i)).text()}\n')

	elif parent.ss_card_cb.currentData() == '7i72':
		# 48 ss7i72out_
		for i in range(48):
			if getattr(parent, f'ss7i72out_{i}').text() != 'Select':
				contents.append(f'ss7i72out_{i} = {getattr(parent, "ss7i72out_" + str(i)).text()}\n')

	elif parent.ss_card_cb.currentData() == '7i73':
		# 16 ss7i73key_
		# 12 ss7i73lcd_
		# 16 ss7i73in_
		# 2 ss7i73out_
		for i in range(16):
			if getattr(parent, f'ss7i73key_{i}').text() != 'Select':
				contents.append(f'ss7i73key_{i} = {getattr(parent, "ss7i73key_" + str(i)).text()}\n')
		for i in range(12):
			if getattr(parent, f'ss7i73lcd_{i}').text() != 'Select':
				contents.append(f'ss7i73lcd_{i} = {getattr(parent, "ss7i73lcd_" + str(i)).text()}\n')
		for i in range(16):
			if getattr(parent, f'ss7i73in_{i}').text() != 'Select':
				contents.append(f'ss7i73in_{i} = {getattr(parent, "ss7i73in_" + str(i)).text()}\n')
		for i in range(2):
			if getattr(parent, f'ss7i73out_{i}').text() != 'Select':
				contents.append(f'ss7i73out_{i} = {getattr(parent, "ss7i73out_" + str(i)).text()}\n')

	elif parent.ss_card_cb.currentData() == '7i84u':
		# 32 ss7i84in_
		# 16 ss7i84out_
		for i in range(32):
			if getattr(parent, f'ss7i84uin_{i}').text() != 'Select':
				contents.append(f'ss7i84uin_{i} = {getattr(parent, "ss7i84uin_" + str(i)).text()}\n')
		for i in range(16):
			if getattr(parent, f'ss7i84uout_{i}').text() != 'Select':
				contents.append(f'ss7i84uout_{i} = {getattr(parent, "ss7i84uout_" + str(i)).text()}\n')

	elif parent.ss_card_cb.currentData() == '7i87':
		# 8 ss7i87in_
		for i in range(8):
			if getattr(parent, f'ss7i87in_{i}').text() != 'Select':
				contents.append(f'ss7i87in_{i} = {getattr(parent, "ss7i87in_" + str(i)).text()}\n')


	try:
		with open(parent.ini_path, 'w') as f:
			f.writelines(contents)
			parent.info_pte.appendPlainText(f'Finished Building the {parent.ini_path} file')
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')
