import shutil

def build_combos(parent):
	# Machine Tab Board Name, HAL Name
	boards = [
	['Select', False],
	['5i25', '5i25'],
	['5i25T', '5i25t'],
	['6i25', '5i25'],
	['7c80', '7c80'],
	['7c81', '7c81'],
	['7i76E', '7i76e'],
	['7i76EU', '7i76eu'],
	['7i92', '7i92'],
	['7i92T', '7i92t'],
	['7i95', '7i95'],
	['7i95T', '7i95t'],
	['7i96', '7i96'],
	['7i96S', '7i96s'],
	['7i97', '7i97'],
	['7i97T', '7i97t'],
	['7i98', '7i98'],
	]

	for item in boards:
		parent.board_cb.addItem(item[0], item[1])

	# Settings Tab
	gui = [
		['Select', False],
		['Axis', 'axis'],
		['Gmoccapy', 'gmoccapy'],
		['Tklinuxcnc', 'tklinuxcnc'],
		['Touchy', 'touchy']
		]

	for item in gui:
		parent.gui_cb.addItem(item[0], item[1])
	parent.gui_cb.setEditable(True)
	if parent.flex_gui:
		parent.gui_cb.addItem('Flex GUI', 'flexgui')

	linearUnits = [
		['Select', False],
		['Inch', 'inch'],
		['Millimeter', 'mm']
		]

	for item in linearUnits:
		parent.linear_units_cb.addItem(item[0], item[1])

	positionOffset = [
		['Select', False],
		['Relative', 'RELATIVE'],
		['Machine', 'MACHINE']
		]

	for item in positionOffset:
		parent.position_offset_cb.addItem(item[0], item[1])

	positionFeedback = [
		['Select', False],
		['Commanded', 'COMMANDED'],
		['Actual', 'ACTUAL']
		]

	for item in positionFeedback:
		parent.position_feedback_cb.addItem(item[0], item[1])

	editor_dict = {'Gedit':'gedit', 'Geany':'geany', 'Pyroom':'pyroom',
		'Pluma':'pluma', 'Scite':'scite', 'Kwrite':'kwrite',
		'Kate':'kate', 'Mousepad':'mousepad', 'Jedit':'jedit',
		'XED':'xed'}

	editor_list = []
	for key, value in editor_dict.items(): # get a list of installed editors
		if shutil.which(value) is not None:
			editor_list.append([key, value])

	if editor_list:
		parent.editor_cb.addItem('None', False)
		for item in editor_list:
			parent.editor_cb.addItem(item[0], item[1])
	else:
		parent.editor_cb.addItem('No Editors Found', False)

	screen_size = [
	['Select', False],
	['Minimized', 'minimized'],
	['Normal', 'normal'],
	['Maximized', 'maximized'],
	['Full', 'full']
	]

	for item in screen_size:
		parent.flex_size_cb.addItem(item[0], item[1])

	# Joint Tabs
	axes = [
		['Select', False],
		['X', 'X'],
		['Y', 'Y'],
		['Z', 'Z'],
		['A', 'A'],
		['B', 'B'],
		['C', 'C'],
		['U', 'U'],
		['V', 'V'],
		['W', 'W']
		]

	for i in range(3):
		for j in range(6):
			for item in axes:
				getattr(parent, f'c{i}_axis_{j}').addItem(item[0], item[1])

	drives = [
		['Custom', False],
		['Gecko 201', ['500', '4000', '20000', '1000']],
		['Gecko 202', ['500', '4500', '20000', '1000']],
		['Gecko 203v', ['1000', '2000', '200', '200']],
		['Gecko 210', ['500', '4000', '20000', '1000']],
		['Gecko 212', ['500', '4000', '20000', '1000']],
		['Gecko 320', ['3500', '500', '200', '200']],
		['Gecko 540', ['1000', '2000', '200', '200']],
		['TB6600', ['5000', '5000', '20000', '20000']],
		['L297', ['500', '4000', '4000', '1000']],
		['PMDX 150', ['1000', '2000', '1000', '1000']],
		['Sherline', ['22000', '22000', '100000', '100000']],
		['Xylotex BS-3', ['2000', '1000', '200', '200']],
		['Parker 750', ['1000', '1000', '1000', '200000']],
		['JVL SMD41/42', ['500', '500', '2500', '2500']],
		['Hobbycnc', ['2000', '2000', '2000', '2000']],
		['Keling 4030', ['5000', '5000', '20000', '20000']]
		]

	for i in range(3):
		for j in range(6):
			for item in drives:
				getattr(parent, f'c{i}_drive_{j}').addItem(item[0], item[1])

	# Multi Function Outputs C0
	# description, [sink, source]
	output_types = [
		['Sourcing', ['0', '1']],
		['Sinking', ['1', '0']],
		['Push Pull', ['1', '1']],
		]

	for i in range(16):
		for item in output_types:
			getattr(parent, f'c0_output_type_{i}').addItem(item[0], item[1])

	# SS Card Tab
	ssCards = [
		['Select', False],
		['7i64', '7i64'],
		['7i69', '7i69'],
		['7i70', '7i70'],
		['7i71', '7i71'],
		['7i72', '7i72'],
		['7i73', '7i73'],
		['7i84', '7i84'],
		['7i87', '7i87']
		]

	for item in ssCards:
		parent.ss_card_cb.addItem(item[0], item[1])

	# 7i73 Combo Boxes
	parent.ss7i73_keypad_cb.addItem('None', ['w5d', 'w6d'])
	parent.ss7i73_keypad_cb.addItem('4x8', ['w5d', 'w6u'])
	parent.ss7i73_keypad_cb.addItem('8x8', ['w5u', 'w6d'])

	parent.ss7i73lcd_cb.addItem('Disabled', 'w7d')
	parent.ss7i73lcd_cb.addItem('Enabled', 'w7u')

	cpuSpeed = [
		['MHz', 1000000],
		['GHz', 1000000000]
		]

	for item in cpuSpeed:
		parent.nt_cpu_units_cb.addItem(item[0], item[1])
	for item in cpuSpeed:
		parent.st_cpu_units_cb.addItem(item[0], item[1])

	# Options Tab
	debug = [
		['Debug Off', '0x00000000'],
		['Debug Configuration', '0x00000002'],
		['Debug Task Issues', '0x00000008'],
		['Debug NML', '0x00000010'],
		['Debug Motion Time', '0x00000040'],
		['Debug Interpreter', '0x00000080'],
		['Debug RCS', '0x00000100'],
		['Debug Interperter List', '0x00000800'],
		['Debug IO Control', '0x00001000'],
		['Debug O Word', '0x00002000'],
		['Debug Remap', '0x00004000'],
		['Debug Python', '0x00008000'],
		['Debug Named Parameters', '0x00010000'],
		['Debug Gdbon Signal', '0x00020000'],
		['Debug Python Task', '0x00040000'],
		['Debug User 1', '0x10000000'],
		['Debug User 2', '0x20000000'],
		['Debug Unconditional', '0x40000000'],
		['Debug All', '0x7FFFFFFF']
		]

	for item in debug:
		parent.debug_cb.addItem(item[0], item[1])

