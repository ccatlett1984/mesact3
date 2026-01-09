import os

from libmesact import check
from libmesact import utilities
from libmesact import updateini
from libmesact import buildini
from libmesact import buildhal
from libmesact import buildio
from libmesact import buildmisc

def build(parent):
	if not check.check_config(parent):
		return

	if parent.backup_cb.isChecked():
		utilities.backup_files(parent)

	# create linuxcnc directory if not there
	emc_path = os.path.expanduser('~/linuxcnc')
	if not os.path.isdir(emc_path):
		os.mkdir(emc_path)
		parent.info_pte.appendPlainText(f'The directory {emc_path} was created')

	# create the linuxcnc/configs directory if not there
	configs_path = os.path.expanduser('~/linuxcnc/configs')
	if not os.path.isdir(configs_path):
		os.mkdir(configs_path)
		parent.info_pte.appendPlainText(f'The directory {configs_path} was created')

	# create the linuxcnc/nc_files directory if not there
	nc_path = os.path.expanduser('~/linuxcnc/nc_files')
	if not os.path.isdir(nc_path):
		os.mkdir(nc_path)
		parent.info_pte.appendPlainText(f'The directory {nc_path} was created')

	# create the linuxcnc/configs/configuration directory if not there
	if not os.path.isdir(parent.config_path):
		os.mkdir(parent.config_path)
		parent.info_pte.appendPlainText(f'The directory {parent.config_path} was created')

	# for testing this is not used
	'''
	if os.path.exists(parent.ini_path):
		updateini.update(parent)
	else:
		buildini.build(parent)
	'''
	buildini.build(parent) # FIXME remove after update ini is started
	buildhal.build(parent)
	buildio.build_io(parent)
	#buildio.build_ss(parent)
	buildmisc.build(parent)
	#parent.mainTW.setCurrentIndex(11)
	#parent.status_lb.setText('Saved')
	#parent.actionBuild.setText('Build Config')



