
from datetime import datetime

def build(parent):
	parent.info_pte.appendPlainText(f'Building {parent.ini_path}')

	contents = ['# This file was created with the Mesa Configuration Tool on ']
	contents.append(f'{datetime.now().strftime("%b %d %Y %H:%M:%S")}\n')
	contents.append('# Changes to most things are ok and will be read by the Configuration Tool\n')

	# build the [MESA] section
	contents.append('\n[MESA]\n')
	contents.append(f'VERSION = {parent.version}\n')
	contents.append(f'BOARD_NAME = {parent.board_cb.currentText()}\n')
	contents.append(f'MESAFLASH_NAME = {parent.board_cb.currentData()}\n')
	if parent.firmware_cb.currentData():
		contents.append(f'FIRMWARE = {parent.firmware_cb.currentData()}\n')
	if parent.daughter_cb_1.currentData():
		contents.append(f'DAUGHTER_1 = {parent.daughter_cb_1.currentData()}\n')
	if parent.daughter_cb_2.currentData():
		contents.append(f'DAUGHTER_2 = {parent.daughter_cb_2.currentData()}\n')

	# build the [EMC] section
	contents.append('\n[EMC]\n')
	contents.append('# VERSION is used by the LinuxCNC startup script\n')
	contents.append(f'VERSION = 1.1\n')
	contents.append(f'EMC_VERSION = {parent.emc_version}\n')
	contents.append(f'MACHINE = {parent.machine_name_le.text()}\n')
	contents.append(f'DEBUG = {parent.debug_cb.currentData()}\n')

	# build the [HM2] section
	contents.append('\n[HM2]\n')
	if parent.board_type == 'eth':
		contents.append('DRIVER = hm2_eth\n')
		contents.append(f'ADDRESS = {parent.address_cb.currentText()}\n')
	elif parent.board_type == 'pci':
		contents.append('DRIVER = hm2_pci\n')
	elif parent.board_type == 'spi':
		contents.append('DRIVER = hm2_spix\n')

	# build the [DISPLAY] section
	contents.append('\n[DISPLAY]\n')
	if not parent.gui_cb.currentData(): # use the user gui
		contents.append(f'DISPLAY = {parent.gui_cb.currentText()}\n')
	else:
		contents.append(f'DISPLAY = {parent.gui_cb.currentData()}\n')
	contents.append(f'PROGRAM_PREFIX = ~/linuxcnc/nc_files\n')


	# Flex GUI
	if len(parent.flex_gui_le.text()) > 0:
		contents.append(f'GUI = {parent.flex_gui_le.text()}\n')
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

	if parent.max_feed_override_dsb.value() > 0:
		contents.append(f'MAX_FEED_OVERRIDE = {parent.max_feed_override_dsb.value():.1f}\n')
	if parent.min_lin_jog_vel_dsb.value() > 0:
		contents.append(f'MIN_LINEAR_VELOCITY = {parent.min_lin_jog_vel_dsb.value():.1f}\n')
	if parent.def_lin_jog_vel_dsb.value() > 0:
		contents.append(f'DEFAULT_LINEAR_VELOCITY = {parent.def_lin_jog_vel_dsb.value():.1f}\n')
	if parent.max_lin_jog_vel_dsb.value() > 0:
		contents.append(f'MAX_LINEAR_VELOCITY = {parent.max_lin_jog_vel_dsb.value():.1f}\n')
	if parent.min_ang_jog_vel_dsb.value() > 0:
		contents.append(f'MIN_ANGULAR_VELOCITY = {parent.min_ang_jog_vel_dsb.value():.1f}\n')
	if parent.def_ang_jog_vel_dsb.value() > 0:
		contents.append(f'DEFAULT_ANGULAR_VELOCITY = {parent.def_ang_jog_vel_dsb.value():.1f}\n')
	if parent.max_ang_jog_vel_dsb.value() > 0:
		contents.append(f'MAX_ANGULAR_VELOCITY = {parent.max_ang_jog_vel_dsb.value():.1f}\n')
	if parent.jog_increments.text():
		contents.append(f'INCREMENTS = {parent.jog_increments.text()}\n')
	if parent.splash_screen_gb.isChecked():
		contents.append(f'INTRO_GRAPHIC = {parent.intro_graphic_le.text()}\n')
		contents.append(f'INTRO_TIME = {parent.splash_screen_sb.value()}\n')
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

	# build the [KINS] Section
	# build the [AXIS_<letter>] Section
	# build the [JOINT_<num>] Sections
	# build the [SPINDLE_<num>] Section(s)
	# build the [EMCIO] Section


	'''
	contents.
	contents.
	'''

	try:
		with open(parent.ini_path, 'w') as f:
			f.writelines(contents)
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')
