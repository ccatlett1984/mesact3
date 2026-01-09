import os, traceback
from datetime import datetime

def build(parent):
	# if Axis is the GUI add the shutup file
	if parent.gui_cb.currentData() == 'axis':
		if parent.axis_nag_cb.isChecked():
			shutup_file = os.path.expanduser('~/.axisrc')
			if not os.path.isfile(shutup_file):
				with open(shutup_file, 'w') as f:
					f.writelines(['root_window.tk.call("wm","protocol",".","WM_DELETE_WINDOW","destroy .")'])
					parent.info_pte.appendPlainText(f'Building {shutup_file}')

	if parent.custom_hal_cb.isChecked():
		custom_file = os.path.join(parent.config_path, 'custom.hal')
		if not os.path.isfile(custom_file):
			contents = ['# This file was created with the Mesa Configuration Tool on ']
			contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
			contents.append('# Add HAL commands to this file that need to be executed BEFORE the GUI loads\n')
			contents.append('# This file will not be modified by the Configuration tool if it exists\n')
			with open(custom_file, 'w') as f:
				f.writelines(contents)
				parent.info_pte.appendPlainText(f'Building {custom_file}')

	if parent.postgui_hal_cb.isChecked():
		# create the postgui.hal file if not there
		postgui_file = os.path.join(parent.config_path, 'postgui.hal')
		if not os.path.isfile(postgui_file):
			contents = ['# This file was created with the Mesa Configuration Tool on ']
			contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
			contents.append('# Add HAL commands to this file that need to be executed AFTER the GUI loads\n')
			contents.append('# This file will not be modified by the Configuration tool if it exists\n')
			with open(postgui_file, 'w') as f:
				f.writelines(contents)
				parent.info_pte.appendPlainText(f'Building {postgui_file}')

	if parent.shutdown_hal_cb.isChecked():
		# create the shutdown.hal file if not there
		shutdown_file = os.path.join(parent.config_path, 'shutdown.hal')
		if not os.path.isfile(shutdown_file):
			contents = ['# This file was created with the Mesa Configuration Tool on ']
			contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
			contents.append('# Add HAL commands to this file that need to be executed AFTER the GUI shuts down\n')
			contents.append('# This file will not be modified by the Configuration tool if it exists\n')
			with open(shutdown_file, 'w') as f:
				f.writelines(contents)
				parent.info_pte.appendPlainText(f'Building {shutdown_file}')

	# create the readme file if text in readme_pte
	if parent.readme_pte.toPlainText():
		readme_file = os.path.join(parent.config_path, 'README')
		with open(readme_file, 'w') as f:
			f.writelines(parent.readme_pte.toPlainText())

	# create the linuxcnc/subroutines directory if requested and not there
	if parent.subroutine_cb.isChecked():
		sub_path = os.path.expanduser('~/linuxcnc/subroutines')
		if not os.path.isdir(sub_path):
			os.mkdir(os.path.expanduser('~/linuxcnc/subroutines'))
			parent.info_pte.appendPlainText(f'The directory {sub_path} was created')

	# create the var file if not there
	var_file = os.path.join(parent.config_path, 'parameters.var')
	if not os.path.isfile(var_file):
		open(var_file, 'a').close()
		parent.info_pte.appendPlainText(f'The parameters file {var_file} was created')

	# create the tool file if not there
	tool_file = os.path.join(parent.config_path, 'tool.tbl')
	if not os.path.isfile(tool_file):
		with open(tool_file, 'w') as f:
			f.write(';\n')
			f.write('T1  P1  ;sample tool')
		parent.info_pte.appendPlainText(f'The tool table file {tool_file} was created')

	# create the pyvcp panel if checked and not there
	if parent.pyvcp_cb.isChecked():
		pyvcp_file = os.path.join(parent.config_path, 'pyvcp.xml')
			if not os.path.isfile(pyvcp_file):
				contents = ["<?xml version='1.0' encoding='UTF-8'?>\n"]
				contents.append('<pyvcp>\n')
				contents.append('<!--\n')
				contents.append('Build your PyVCP panel between the <pyvcp></pyvcp> tags.\n')
				contents.append('Make sure your outside the comment tags.\n')
				contents.append('The contents of this file will not be overwritten\n')
				contents.append('when you run the configuration tool again.\n')
				contents.append('	<label>\n')
				contents.append('		<text>"This is a Sample Label:"</text>\n')
				contents.append('		<font>("Helvetica",10)</font>\n')
				contents.append('	</label>\n')
				contents.append('</pyvcp>\n')
				with open(pyvcp_file, 'w') as f:
					f.writelines(contents)
					parent.info_pte.appendPlainText(f'Building {pyvcp_file}')

	if parent.ladder_gb.isChecked():
		ladder_file = os.path.join(parent.config_path, 'ladder.clp')
			if not os.path.isfile(ladder_file):
				contents = """_FILES_CLASSICLADDER
_FILE-symbols.csv
#VER=1.0
_/FILE-symbols.csv
_FILE-modbusioconf.csv
#VER=1.0
_/FILE-modbusioconf.csv
_FILE-com_params.txt
MODBUS_MASTER_SERIAL_PORT=
MODBUS_MASTER_SERIAL_SPEED=9600
MODBUS_ELEMENT_OFFSET=0
MODBUS_MASTER_SERIAL_USE_RTS_TO_SEND=0
MODBUS_MASTER_TIME_INTER_FRAME=100
MODBUS_MASTER_TIME_OUT_RECEIPT=500
MODBUS_MASTER_TIME_AFTER_TRANSMIT=0
MODBUS_DEBUG_LEVEL=0
MODBUS_MAP_COIL_READ=0
MODBUS_MAP_COIL_WRITE=0
MODBUS_MAP_INPUT=0
MODBUS_MAP_HOLDING=0
MODBUS_MAP_REGISTER_READ=0
MODBUS_MAP_REGISTER_WRITE=0
_/FILE-com_params.txt
_FILE-timers_iec.csv
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
_/FILE-timers_iec.csv
_FILE-timers.csv
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
_/FILE-timers.csv
_FILE-counters.csv
0
0
0
0
0
0
0
0
0
0
_/FILE-counters.csv
_FILE-sections.csv
#VER=1.0
#NAME000=Prog1
000,0,-1,0,0,0
_/FILE-sections.csv
_FILE-arithmetic_expressions.csv
#VER=2.0
_/FILE-arithmetic_expressions.csv
_FILE-rung_0.csv
#VER=2.0
#LABEL=
#COMMENT=
#PREVRUNG=0
#NEXTRUNG=0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
_/FILE-rung_0.csv
_FILE-ioconf.csv
#VER=1.0
_/FILE-ioconf.csv
_FILE-monostables.csv
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
_/FILE-monostables.csv
_FILE-sequential.csv
#VER=1.0
_/FILE-sequential.csv
_FILE-general.txt
PERIODIC_REFRESH=50
SIZE_NBR_RUNGS=100
SIZE_NBR_BITS=500
SIZE_NBR_WORDS=100
SIZE_NBR_TIMERS=10
SIZE_NBR_MONOSTABLES=10
SIZE_NBR_COUNTERS=10
SIZE_NBR_TIMERS_IEC=10
SIZE_NBR_PHYS_INPUTS=15
SIZE_NBR_PHYS_OUTPUTS=15
SIZE_NBR_ARITHM_EXPR=100
SIZE_NBR_SECTIONS=10
SIZE_NBR_SYMBOLS=100
_/FILE-general.txt
_/FILES_CLASSICLADDER
"""

				with open(ladder_file, 'w') as f:
					f.writelines(contents)
					parent.info_pte.appendPlainText(f'Building {ladder_file}')







