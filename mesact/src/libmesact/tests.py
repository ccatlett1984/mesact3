
from functools import partial

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QComboBox, QWidget

from libmesact import dialogs
from libmesact import download



def connect(parent):
	parent.msg_open_abort_cancel_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_open_cancel_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_cancel_ok_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_error_ok_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_question_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_yes_no_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_yes_no_check_pb.clicked.connect(partial(test_dialogs, parent))
	parent.msg_ok_pb.clicked.connect(partial(test_dialogs, parent))

	parent.amd64_deb_pb.clicked.connect(partial(download.download_deb, 'amd64', parent))
	parent.armhf_deb_pb.clicked.connect(partial(download.download_deb, 'armhf', parent))
	parent.arm64_deb_pb.clicked.connect(partial(download.download_deb, 'arm64', parent))
	parent.bad_url_pb.clicked.connect(partial(download.download_deb, parent))
	parent.download_firmware_pb.clicked.connect(partial(download.download_firmware, parent))

	parent.test_axis_names_pb.clicked.connect(partial(test_axis_names, parent))
	parent.test_pid_names_pb.clicked.connect(partial(test_pid_names, parent))
	parent.test_homing_names_pb.clicked.connect(partial(test_homing_names, parent))
	parent.test_stepgen_names_pb.clicked.connect(partial(test_stepgen_names, parent))
	parent.test_analog_names_pb.clicked.connect(partial(test_analog_names, parent))
	parent.test_input_names_pb.clicked.connect(partial(test_input_names, parent))
	parent.test_output_names_pb.clicked.connect(partial(test_output_names, parent))



def test_dialogs(parent):
	name = parent.sender().objectName()
	match name:
		case 'msg_open_abort_cancel_pb':
			result = dialogs.msg_open_abort_cancel(parent, 'Test', 'Title')
			print(result)
		case 'msg_open_cancel_pb':
			result = dialogs.msg_open_cancel(parent, 'Test', 'Title')
			print(result)
		case 'msg_cancel_ok_pb':
			result = dialogs.msg_cancel_ok(parent, 'Test', 'Title')
			print(result)
		case 'msg_error_ok_pb':
			result = dialogs.msg_error_ok(parent, 'Test', 'Title')
			print(result)
		case 'msg_question_pb':
			result = dialogs.msg_question(parent, 'Test', 'Title')
			print(result)
		case 'msg_yes_no_pb':
			result = dialogs.msg_yes_no(parent, 'Test', 'Title')
			print(result)
		case 'msg_yes_no_check_pb':
			result = dialogs.msg_yes_no_check(parent, 'Test', 'Title', 'Text')
			print(result)
		case 'msg_ok_pb':
			result = dialogs.msg_ok(parent, 'Test', 'Title')
			print(result)

def test_axis_names(parent):
	print('test_axis_names')
	'''
	c0_axis_0 c0_axis_type_0 c0_scale_0 c0_min_limit_0 c0_max_limit_0 c0_max_vel_0
	c0_max_vel_suffix_0 c0_max_accel_0 c0_max_vel_min_0 c0_max_vel_min_suffix_0
	'''
	axis_list = ['axis', 'axis_type', 'scale', 'min_limit', 'max_limit',
	'max_vel', 'max_vel_suffix', 'max_accel', 'max_vel_min', 'max_vel_min_suffix']
	for item in axis_list:
		for i in range(3):
			for j in range (6):
				if not parent.findChildren(QObject, f'c{i}_{item}_{j}'):
					print(f'******* c{i}_{item}_{j} Not Found *******')
		print(f'All of the {item} names were tested')

def test_pid_names(parent):
	print('test_axis_names')
	'''
	c0_p_0 c0_i_0 c0_d_0 c0_ff0_0 c0_ff1_0 c0_ff2_0
	c0_deadband_0 c0_bias_0 c0_max_output_0 c0_max_error_0 c0_pid_default_0
	c0_min_ferror_0 c0_max_ferror_0 c0_ferror_default_0
	'''

	pid_list = ['p', 'i', 'd', 'ff0', 'ff1', 'ff2', 'deadband', 'bias',
	'max_output', 'max_error', 'pid_default', 'min_ferror', 'max_ferror', 'ferror_default']
	for item in pid_list:
		for i in range(3):
			for j in range (6):
				if not parent.findChildren(QObject, f'c{i}_{item}_{j}'):
					print(f'******* c{i}_{item}_{j} Not Found *******')
		print(f'All of the {item} names were tested')

def test_homing_names(parent):
	print('test_homing_names')
	'''
	c0_home_0 c0_home_offset_0 c0_home_search_vel_0 c0_home_latch_vel_0
	c0_home_final_vel_0 c0_home_sequence_0 c0_home_use_index_0
	c0_home_switch_shared_0 c0_home_ignore_limits_0
	'''

	home_list = ['home', 'home_offset', 'home_search_vel', 'home_latch_vel',
	'home_final_vel', 'home_sequence', 'home_use_index', 'home_switch_shared',
	'home_ignore_limits']
	for item in home_list:
		for i in range(3):
			for j in range (6):
				if not parent.findChildren(QObject, f'c{i}_{item}_{j}'):
					print(f'******* c{i}_{item}_{j} Not Found *******')
		print(f'All of the {item} names were tested')

def test_stepgen_names(parent):
	print('test_stepgen_names')
	'''
	c0_drive_0 c0_step_time_0 c0_step_invert_0 c0_step_space_0 c0_dir_setup_0
	c0_dir_invert_0 c0_dir_hold_0
	'''

	stepgen_list = ['drive', 'step_time', 'step_invert', 'step_space',
	'dir_setup', 'dir_invert', 'dir_hold']

	for item in stepgen_list:
		for i in range(3):
			for j in range (6):
				if not parent.findChildren(QObject, f'c{i}_{item}_{j}'):
					print(f'******* c{i}_{item}_{j} Not Found *******')
		print(f'All of the {item} names were tested')

def test_analog_names(parent):
	print('test_analog_names')
	'''
	c0_analog_min_limit_0 c0_analog_max_limit_0 c0_analog_scale_max_0
	c0_analog_default_0 c0_encoder_scale_0
	'''

	analog_list = ['analog_min_limit', 'analog_max_limit', 'analog_scale_max',
	'analog_default', 'encoder_scale']

	for item in analog_list:
		for i in range(3):
			for j in range (6):
				if not parent.findChildren(QObject, f'c{i}_{item}_{j}'):
					print(f'******* c{i}_{item}_{j} Not Found *******')
		print(f'All of the {item} names were tested')

def test_input_names(parent):
	print('test_input_names')
	'''
	c0_input_0 c0_input_invert_0 c0_input_debounce_0
	'''

	input_list = ['input', 'input_invert', 'input_debounce']

	for item in input_list:
		for i in range(3):
			for j in range (32):
				if not parent.findChildren(QObject, f'c{i}_{item}_{j}'):
					print(f'******* c{i}_{item}_{j} Not Found *******')
		print(f'All of the {item} names were tested')

def test_output_names(parent):
	'''
	c0_output_0 c0_output_invert_0 c0_output_type_0
	'''

	output_list = ['output', 'output_invert', 'output_type']
	for item in output_list:
		for i in range(3):
			for j in range (16):
				if not parent.findChildren(QObject, f'c{i}_{item}_{j}'):
					print(f'******* c{i}_{item}_{j} Not Found *******')
		print(f'All of the {item} names were tested')

def test_connection():
	print('test')


