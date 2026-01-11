import os, traceback
from datetime import datetime

from libmesact import io

def build(parent):
	file_path = os.path.join(parent.config_path, 'sserial.hal')
	parent.info_pte.appendPlainText(f'Building {file_path}')
	ss_board = parent.ss_card_cb.currentData()
	host_board = parent.sserial_host_cb.currentData()
	if ss_board:
		contents = []
		contents = ['# This file was created with the Mesa Configuration Tool on ']
		contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
		contents.append('# If you make changes to this file DO NOT use the Configuration Tool\n')

		'''
		'7i64':'24 Inputs, 24 Outputs',
		'7i70':'48 Inputs',
		'7i71':'48 Sourcing Outputs',
		'7i72':'48 Sinking Outputs',
		'7i73':'Pendant Card',
		'7i83':'6 Channel Analog Outputs'
		'7i84u':'32 Inputs 16 Outputs',
		'7i87':'8 Channel Analog Inputs',
		'7iAO':'48 Inputs 24, Outputs'
		'''


		match ss_board:
			case '7i70':
				contents.append('\n# 7i70 Inputs\n')
				contents.extend(build_inputs(parent, host_board, ss_board, 48))
			case '7i71':
				contents.append('\n# 7i71 Outputs\n')
				contents.extend(build_outputs(parent, host_board, ss_board, 48))
			case '7i72':
				contents.append('\n# 7i72 Outputs\n')
				contents.extend(build_outputs(parent, host_board, ss_board, 48))


		create_file(parent, file_path, contents)

def build_inputs(parent, host_board, ss_board, count):
	inputs = []
	for i in range(count):
		if getattr(parent, f'ss{ss_board}in_' + str(i)).text() != 'Select':
			key = getattr(parent, f'ss{ss_board}in_' + str(i)).text()
			inputs.append(f'{io.inputs[key]} hm2_{host_board}.0.{ss_board}.0.0.input-{i:02}\n')
	return inputs

def build_outputs(parent, host_board, ss_board, count):
	outputs = []
	for i in range(count):
		if getattr(parent, f'ss{ss_board}out_{i}').text() != 'Select':
			key = getattr(parent, f'ss{ss_board}out_{i}').text()
			outputs.append(f'{io.outputs[key]} hm2_{host_board}.0.{ss_board}.0.0.output-{i:02}\n')
	return outputs


def create_file(parent, file_path, contents):
	try:
		with open(file_path, 'w') as f:
			f.writelines(contents)
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

