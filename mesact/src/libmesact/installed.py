import os, subprocess, sysconfig
from threading import Thread
from platform import python_version

from PyQt6.QtCore import qVersion

def versions(parent):
	try: # need to set this before building combos
		parent.flex_gui = False
		flex = subprocess.check_output(['apt-cache', 'policy', 'flexgui'], text=True)
		#print(f'flex {flex}')
		#print(f'len(flex) {len(flex)}')
		if len(flex) > 0:
			version = flex.split()[2]
			parent.flex_gui_lb.setText(f'{version}')
			parent.flex_gui = True
		else:
			parent.flex_gui_lb.setText('Not Installed')
	except:
		parent.flex_gui_lb.setText('Error')

	#print(f'parent.flex_gui {parent.flex_gui}')

	try:
		mf = subprocess.check_output('mesaflash', encoding='UTF-8')
		if len(mf) > 0:
			version = mf.split()[2]
			parent.mesaflash_version = tuple(int(i) for i in version.split('.'))
			parent.mesaflash_version_lb.setText(version)
			parent.mesaflash = True
			parent.flashed = False
	except FileNotFoundError as error:
		parent.firmware_gb.setEnabled(False)
		parent.verify_board_pb.setEnabled(False)
		parent.mesaflash_version_lb.setText('Not Installed')
		parent.mesaflash = False
		parent.mesaflash_version = ()

	# get emc version if installed
	parent.emcVersion_lb.clear()
	parent.emc_version = (0, 0, 0)
	try: # don't crash if your not running debian
		emc = subprocess.check_output(['apt-cache', 'policy', 'linuxcnc-uspace'], text=True)
	except:
		emc = False
		pass

	if emc:
		for line in emc.split('\n'):
			if 'installed' in line.lower():
				version = line.split() # remove leading space
				if len(version) == 2: # split out the version number
					version = version[1]
				if ':' in version: # strip the 1 from version
					version = version.split(':')[1]
					version = '.'.join(version.split('.', 3)[:3])
				if '~' in version:
					version = version.split('~')[0]
				# make damn sure version is valid
				if all(c in "0123456789." for c in version) and version.count('.') > 1:
					parent.emcVersion_lb.setText(version)
					parent.emc_version = tuple(int(i) for i in version.split('.'))
				else:
					parent.emcVersion_lb.setText('Version Error')
				break
	else:
		parent.emcVersion_lb.setText('Not Installed')

	try:
		os_name = subprocess.check_output(['lsb_release', '-is'], encoding='UTF-8').split()
		os_version = subprocess.check_output(['lsb_release', '-rs'], encoding='UTF-8').split()
		parent.os_name_lb.setText(f'{os_name[0]} {os_version[0]}')
		code_name = subprocess.check_output(['lsb_release', '-cs'], encoding='UTF-8').split()
		parent.os_code_name_lb.setText(f'{code_name[0].title()}')
	except:
		parent.os_name_lb.setText('OS Unknown')
		parent.os_code_name_lb.setText('No Codename')

	parent.platform_lb.setText(sysconfig.get_platform())
	parent.python_lb.setText(python_version())
	parent.pyqt_lb.setText(qVersion())

def get_versions(parent):
	versions_thread = Thread(target=versions, args=(parent,))
	versions_thread.start()
	versions_thread.join()





