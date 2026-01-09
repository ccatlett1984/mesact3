import os, traceback
from datetime import datetime

def build(parent):

	hal_path = os.path.join(parent.config_path, 'main' + '.hal')
	parent.info_pte.appendPlainText(f'Building {hal_path}')

	contents = []
	contents = ['# This file was created with the Mesa Configuration Tool on ']
	contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	contents.append('# If you make changes to this file DO NOT run the configuration tool again!\n')
	contents.append('# This file will be replaced with a new file if you do!\n')

	# build the standard header
	contents.append('\n# kinematics\n')
	contents.append('loadrt [KINS](KINEMATICS)\n')

	contents.append('\n# motion controller\n')
	contents.append('loadrt [EMCMOT](EMCMOT) ')
	contents.append('servo_period_nsec=[EMCMOT](SERVO_PERIOD) ')
	contents.append('num_joints=[KINS](JOINTS)\n')

	contents.append('\n# hostmot2 driver\n')
	contents.append('loadrt hostmot2\n')

	contents.append('loadrt ')
	if parent.board_interface == 'eth':
		contents.append('hm2_eth ')
	elif parent.board_interface == 'pci':
		contents.append('hm2_pci ')
	elif parent.board_interface == 'spi':
		contents.append('hm2_spix ')

	if parent.board_interface == 'eth':
		contents.append(f'board_ip="{parent.address_cb.currentText()}" config="sserial_port_0=00000000"\n')

	contents.append(f'\nsetp hm2_{parent.board_0_hal_name}.0.watchdog.timeout_ns {parent.servo_period_sb.value() * 5}\n')

	# PID FIXME for daughter boards
	pid_count = 0
	pid_string = ''
	for axis in parent.coordinates_lb.text():
		if parent.coordinates_lb.text().count(axis) == 1:
			pid_string += f'pid.{axis.lower()},'
		elif parent.coordinates_lb.text().count(axis) > 1:
			pid_string += f'pid.{axis.lower()}{pid_count},'
			pid_count += 1
	if parent.spindle_rpm_le.text():
		pid_string += f'pid.s,'
	contents.append(f'\nloadrt pid names={pid_string[:-1]}\n')

	if parent.board_0_type == 'stepper':
		contents.append('\n# Why Mesa Stepper Boards need a PID controller\n')
		contents.append('# Mesa hardware step generators at every servo thread invocation, the step\n')
		contents.append('# generator hardware is given a new velocity. Without feedback from the PID\n')
		contents.append('# controller the hardware position would slowly drift because of clock speed and\n')
		contents.append('# timing differences between LinuxCNC and the step generator hardware.\n')
		contents.append('# The PID controller gets feedback from the actual (fractional) step position and\n')
		contents.append('# corrects for these small differences.\n')

		contents.append('\n# DPLL TIMER\n')
		contents.append(f'setp hm2_{parent.board_0_hal_name}.0.dpll.01.timer-us -200\n')
		contents.append(f'setp hm2_{parent.board_0_hal_name}.0.stepgen.timer-number 1\n')

	contents.append('\n# THREADS\n')
	contents.append(f'addf hm2_{parent.board_0_hal_name}.0.read servo-thread\n')
	contents.append('addf motion-command-handler servo-thread\n')
	contents.append('addf motion-controller servo-thread\n')

	pid_list = pid_string[:-1].split(',')
	for pid in pid_list:
		contents.append(f'addf {pid}.do-pid-calcs servo-thread\n')
	contents.append(f'addf hm2_{parent.board_0_hal_name}.0.write servo-thread\n')

	contents.append('\n# amp enable\n')
	contents.append(f'net motion-enable <= motion.motion-enabled\n')

	# Joints
	# 7i96s has a pwmgen enable for something
	drive_enables = {'7i76': 'stepgen', '7i76e': 'stepgen', '7i77': 'pwmgen',
	'7i95': 'stepgen', '7i96': 'stepgen', '7i96s': 'stepgen', '7i97': 'pwmgen'}

	joint = 0
	for i in range(3):
		if getattr(parent, f'c{i}_board_tw').tabText(0):
			#board = getattr(parent, f'c{i}_board_tw').tabText(0)
			hal_name = getattr(parent, f'board_{i}_hal_name')
			for j in range(6):
				axis = getattr(parent, f'c{i}_axis_{j}').currentData()
				if axis:
					contents.append(f'\n# Axis: {axis} Joint: {joint} Output: {j}\n')
					contents.append(f'# PID Setup\n')
					contents.append(f'setp {pid_list[joint]}.Pgain [JOINT_{joint}](P)\n')
					contents.append(f'setp {pid_list[joint]}.Igain [JOINT_{joint}](I)\n')
					contents.append(f'setp {pid_list[joint]}.Dgain [JOINT_{joint}](D)\n')
					contents.append(f'setp {pid_list[joint]}.bias [JOINT_{joint}](BIAS)\n')
					contents.append(f'setp {pid_list[joint]}.FF0 [JOINT_{joint}](FF0)\n')
					contents.append(f'setp {pid_list[joint]}.FF1 [JOINT_{joint}](FF1)\n')
					contents.append(f'setp {pid_list[joint]}.FF2 [JOINT_{joint}](FF2)\n')
					contents.append(f'setp {pid_list[joint]}.deadband [JOINT_{joint}](DEADBAND)\n')
					contents.append(f'setp {pid_list[joint]}.maxoutput [JOINT_{joint}](MAX_OUTPUT)\n')
					contents.append(f'setp {pid_list[joint]}.error-previous-target True\n')

					# Index Enable
					contents.append(f'\n# joint-{joint} enable chain\n')
					contents.append(f'net joint-{joint}-index-enable <=> {pid_list[joint]}.index-enable\n')
					contents.append(f'net joint-{joint}-index-enable <=> joint.{joint}.index-enable\n')

					# Enables
					contents.append('\n# Joint Enables\n')
					contents.append(f'net {axis}-enable => pid.{axis}.enable\n')
					contents.append(f'net {axis}-enable <= joint.{joint}.amp-enable-out\n')
					contents.append(f'net {axis}-enable <= hm2_{hal_name}.0.{drive_enables[hal_name]}.0{joint}.enable\n')

					# Stepgen
					if getattr(parent, f'board_{i}_type') == 'stepper':
						contents.append(f'\n# Joint {joint} Step Generator Settings\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.steplen [JOINT_{joint}](STEP_LEN)\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.stepspace [JOINT_{joint}](STEP_SPACE)\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.dirsetup [JOINT_{joint}](DIR_SETUP)\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.dirhold [JOINT_{joint}](DIR_HOLD)\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.position-scale [JOINT_{joint}](SCALE)\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.maxvel [JOINT_{joint}](STEPGEN_MAX_VEL)\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.maxaccel [JOINT_{joint}](STEPGEN_MAX_ACC)\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.step_type 0\n')
						contents.append(f'setp hm2_{hal_name}.0.stepgen.0{joint}.control-type 1\n')

					# Servo FIXME

					# Position Command and Feedback
					contents.append('\n# position command and feedback\n')
					contents.append(f'net joint-{joint}-pos-cmd <= joint.{joint}.motor-pos-cmd\n')
					contents.append(f'net joint-{joint}-pos-cmd => {pid_list[joint]}.command\n')

					if getattr(parent, f'board_{i}_type') == 'stepper':
						contents.append(f'net joint-{joint}-pos-fb <= hm2_{hal_name}.0.stepgen.0{joint}.position-fb\n')
					elif getattr(parent, f'board_{i}_type') == 'servo':
						contents.append(f'net joint-{joint}-pos-fb <= hm2_{hal_name}.0.encoder.0{joint}.position\n')
					contents.append(f'net joint-{joint}-pos-fb => joint.{joint}.motor-pos-fb\n')
					contents.append(f'net joint-{joint}-pos-fb => {pid_list[joint]}.feedback\n')

					# PID Output
					contents.append('\n# PID Output\n')
					contents.append(f'net joint.{joint}.output <= {pid_list[joint]}.output\n')
					if getattr(parent, f'board_{i}_type') == 'stepper':
						contents.append(f'net joint.{joint}.output => hm2_{hal_name}.0.stepgen.0{joint}.velocity-cmd\n')
					# hm2_7i92.0.7i77.0.1.analogout0
					elif getattr(parent, f'board_{i}_type') == 'servo':
						contents.append(f'net joint.{joint}.output => hm2_{hal_name}.0.pwmgen.0{output}.value\n')

					joint += 1

	# E Stop
	external_estop = False
	for i in range(3): # test for an external e stop input
		for j in range(16):
			key = getattr(parent, f'c{i}_input_{j}').text()
			if key[0:6] == 'E Stop':
				external_estop = True
	if not external_estop:
		contents.append('\n# Standard I/O Block - EStop, Etc\n')
		contents.append('# create a signal for the estop loopback\n')
		contents.append('net estop-loopback iocontrol.0.emc-enable-in <= iocontrol.0.user-enable-out\n')

	# Manual Tool Change
	if parent.manual_tool_change_cb.isChecked():
		contents.append('\n# Manual Tool Change Dialog\n')
		contents.append('loadusr -W hal_manualtoolchange\n')
		contents.append('net tool-number hal_manualtoolchange.number <= iocontrol.0.tool-prep-number\n')
		contents.append('net tool-change-request hal_manualtoolchange.change <= iocontrol.0.tool-change\n')
		contents.append('net tool-change-confirmed iocontrol.0.tool-changed => hal_manualtoolchange.changed\n')

		contents.append('\n# tool prep loopback\n')
		contents.append('net tool-prep-loop iocontrol.0.tool-prepare => iocontrol.0.tool-prepared\n')

	# ClassicLadder
	if parent.ladder_gb.isChecked():
		ladder_options_list = ['ladder_rungs_sb', 'ladder_bits_sb', 'ladder_words_sb',
		'ladder_timers_sb', 'ladder_iec_timer_sb', 'ladder_monostables_sb',
		'ladder_counters_sb', 'ladder_inputs_sb', 'ladder_outputs_sb',
		'ladder_float_inputs_sb', 'ladder_float_outputs_sb', 'ladder_s32_inputs_sb',
		'ladder_s32_ouputs_sb', 'ladder_sections_sb', 'ladder_symbols_sb',
		'ladder_expresions_sb']

		contents.append('\n# # Load Classicladder without GUI\n')
		# this line needs to be built from the options if any are above 0
		ladder_options = []
		for option in ladder_options_list:
			if getattr(parent, option).value() > 0:
				ladder_options.append(getattr(parent, option).property('option') + '=' + str(getattr(parent, option).value()))
		if ladder_options:
				contents.append(f'loadrt classicladder_rt {" ".join(ladder_options)}\n')
		else:
			contents.append('loadrt classicladder_rt\n')
		contents.append('addf classicladder.0.refresh servo-thread 1\n')

	try:
		with open(hal_path, 'w') as f:
			f.writelines(contents)
			parent.info_pte.appendPlainText(f'Finished Building the {hal_path} file')

	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')
