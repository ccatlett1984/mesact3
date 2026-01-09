import os, traceback
from datetime import datetime

from libmesact import io

def build_io(parent):
	file_path = os.path.join(parent.config_path, 'io.hal')
	parent.info_pte.appendPlainText(f'Building {file_path}')
	contents = []
	contents = ['# This file was created with the Mesa Configuration Tool on ']
	contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
	contents.append('# If you make changes to this file DO NOT use the Configuration Tool\n')

	# key is hal name, value is hm2
	main_board_hm2 = {
	'5i25': 'hm2_5i25.0.',
	'7c80': 'hm2_7c80.0.',
	'7c81': 'FIXME',
	'7i76e': 'hm2_7i76e.0.7i76.0.0.',
	'7i92': 'hm2_7i92.0.',
	'7i95': 'hm2_7i95.0.',
	'7i96': 'hm2_7i96.0.',
	'7i96s': 'hm2_7i96s.0.',
	'7i97': 'hm2_7i97.0.'
	}

	daughter_ports = {'7i76': ['2', '0'], '7i77': ['3', '0']}

	input_names = {
	'7c80': 'inmux.00.input-',
	'7i76': 'input-',
	'7i76e': 'input-',
	'7i77': 'input-',
	'7i95': 'inmux.00.input-',
	'7i96': 'gpio.0',
	'7i96s': 'inm.00.input-',
	'7i97': 'inmux.00.input-'}

	output_names = {
	'7c80': ['ssr.00.out-', 'ssr.00.invert-'],
	'7i76': 'output-',
	'7i76e': 'output-',
	'7i77': 'output-',
	'7i95': ['ssr.00.out-', 'ssr.00.invert-'],
	'7i96': ['ssr.00.out-', 'ssr.00.invert-'],
	'7i96s': ['ssr.00.out-', 'outm.00.out'],
	'7i97': ['ssr.00.out-', 'ssr.00.invert-'],}

	mb = parent.board_0_hal_name
	hm2 = main_board_hm2[mb]
	for i in range(3): # determine if the main_tw board tab is visible
		if getattr(parent, f'main_tw').isTabVisible(i + 3): # board tab
			board_name = getattr(parent, f'board_{i}_hal_name')
			#print(f'board_name {board_name}')
			if i == 0:
				address = hm2
			elif i > 0: # it's a daughter board create hm2
				daughter = f'{getattr(parent, f"board_{i}_hal_name")}'
				port = daughter_ports[daughter][i-1]
				address = f'hm2_{mb}.0.{daughter}.0.{port}.'
			#print(f'address {address}')

			if getattr(parent, f'c{i}_board_tw').isTabVisible(7): # inputs tab
				contents.append(f'\n# Inputs for {parent.mesaflash_name}\n')
				for j in range(32):
					input_pb = getattr(parent, f'c{i}_input_{j}')
					if input_pb.isEnabled() and input_pb.text() != 'Select':
						key = getattr(parent, f'c{i}_input_{j}').text()

						if i == 0:
							input_pin = f'{hm2}{input_names[mb]}{j:02d}'
						elif i > 0:
							input_pin = f'{address}{input_names[daughter]}{j:02d}'

						if getattr(parent, f'c{i}_input_invert_{j}').isChecked():
							input_pin += '_not' if mb == '7i96' else '-not'
						elif getattr(parent, f'c{i}_input_debounce_{j}').isChecked():
							input_pin += '-slow'
						#print(f'input pin name {pin_name}')

						if io.inputs.get(key, False): # return False if key is not in dictionary
							contents.append(f'{io.inputs[key]} {input_pin}\n')
							#print(f'{io.inputs[key]} {pin_name}')
						else: # handle special cases
							if key == 'Home All':
								contents.append('\n# Home All Joints\n')
								contents.append('net home-all ' + f'{pin_name}\n')
								for i in range(6):
									if getattr(parent, 'axisCB_' + str(i)).currentData():
										contents.append('net home-all ' + f'joint.{j}.home-sw-in\n')
							elif key[0:6] == 'E Stop':
								eStops.append(hm2)
							elif '+ Joint' in key: # Jog axis and joint enable
								axis = key.split()[1].lower()
								if axis in ja_dict:
									joint = ja_dict[axis]
									contents.append(f'net jog-{axis}-enable axis.{axis}.jog-enable <= {pin_name}\n')
									contents.append(f'net jog-{axis}-enable joint.{joint}.jog-enable\n')

			if getattr(parent, f'c{i}_board_tw').isTabVisible(8): # outputs tab
				contents.append(f'\n# Outputs for {parent.mesaflash_name}\n')
				#print(f'outputs board_name {board_name}')

				if parent.mesaflash_name in ['7i76eu']: # set output types
					sink = ''
					source = ''
					for i in reversed(range(16)):
						sink += getattr(parent, f'c0_output_type_{i}').currentData()[0]
						source += getattr(parent, f'c0_output_type_{i}').currentData()[1]
					contents.append(f'\n# Output Types for {parent.mesaflash_name}\n')
					contents.append(f'setp hm2_7i76e.0.7i76.0.0.output_sink {f"0x{int(sink, 2):0>4X}"}\n')
					contents.append(f'setp hm2_7i76e.0.7i76.0.0.output_source {f"0x{int(source, 2):0>4X}"}\n\n')

				for k in range(16):
					output_parameter = ''
					output_pb = getattr(parent, f'c{i}_output_{k}')
					if output_pb.isEnabled() and output_pb.text() != 'Select':
						output_key = output_pb.text()
						if board_name in ['7i76', '7i77', '7i76e']:
							output_pin = f'{address}output-{k:02d}'
							if getattr(parent, f'c{i}_output_invert_{k}').isChecked():
								output_parameter = f'setp {address}output-{k:02d}-invert True\n'
						elif board_name in ['7c80', '7i95', '7i96', '7i97']:
							invert = 'invert-' if getattr(parent, f'c{i}_output_invert_{k}').isChecked() else 'out-'
							output_pin = f'{address}ssr.00.{invert}{k:02d}'
						elif board_name in ['7i96s']:
							if k <= 3:
								invert = 'invert-' if getattr(parent, f'c{i}_output_invert_{k}').isChecked() else 'out-'
								output_pin = f'{address}ssr.00.{invert}{k:02d}'
							else:
								invert = 'invert-' if getattr(parent, f'c{i}_output_invert_{k}').isChecked() else 'out-'
								output_pin = f'{address}outm.00.{invert}{k:02d}'
						else:
							print('board not found')

						if output_parameter:
							contents.append(output_parameter)
						if io.outputs.get(output_key, False): # return False if key is not in dictionary
							contents.append(f'{io.outputs[output_key]} {output_pin}\n')


	# c0_output_invert_0
	# c0_output_type_0

	try:
		with open(file_path, 'w') as f:
			f.writelines(contents)
	except OSError:
		parent.info_pte.appendPlainText(f'OS error\n {traceback.print_exc()}')

