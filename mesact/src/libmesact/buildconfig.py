import os


from libmesact import check
from libmesact import utilities
from libmesact import updateini
from libmesact import buildini

def build(parent):
	if not check.check_config(parent):
		return

	if parent.backup_cb.isChecked():
		utilities.backup_files(parent)

	# check for emc paths and build if needed
	emc_path = os.path.expanduser('~/linuxcnc')
	config_path = os.path.expanduser('~/linuxcnc/configs')
	nc_path = os.path.expanduser('~/linuxcnc/nc_files')
	sub_path = os.path.expanduser('~/linuxcnc/subroutines')

	if not os.path.isdir(emc_path):
		os.mkdir(emc_path)
		parent.info_pte.appendPlainText(f'The directory {emc_path} was created')

	if not os.path.isdir(config_path):
		os.mkdir(config_path)
		parent.info_pte.appendPlainText(f'The directory {config_path} was created')

	if not os.path.isdir(nc_path):
		os.mkdir(nc_path)
		parent.info_pte.appendPlainText(f'The directory {nc_path} was created')

	if parent.subroutine_cb.isChecked():
		if not os.path.isdir(sub_path):
			os.mkdir(sub_path)
			parent.info_pte.appendPlainText(f'The directory {sub_path} was created')

	if not os.path.isdir(parent.config_path):
		os.mkdir(parent.config_path)
		parent.info_pte.appendPlainText(f'The directory {parent.config_path} was created')

	if os.path.exists(parent.ini_path):
		updateini.update(parent)
	else:
		buildini.build(parent)

	#buildhal.build(parent)
	#buildio.build_io(parent)
	#buildio.build_ss(parent)
	#buildmisc.build(parent)
	#parent.mainTW.setCurrentIndex(11)
	#parent.status_lb.setText('Saved')
	#parent.actionBuild.setText('Build Config')



