from astropy.io import fits
from sunpy.time import parse_time
from astropy.table import Table, vstack
from dateutil.relativedelta import relativedelta 
import urllib 
import os
from pathlib import Path


def make_one_fits():
	"""
	Function to concatenate the monthly flare fits 
	files for RHESSI into one fits file that contains
	them all.
	"""
	base_path = Path("/Users/lahayes/ssw/hessi/dbase/")
	tstart = parse_time("2002-02-01").datetime
	tend = parse_time("2018-03-01").datetime
	month_list = [tstart.strftime("hessi_flare_list_%Y%m.fits")]
	while tend>tstart:
		tstart = tstart + relativedelta(months=1)
		month_list.append(tstart.strftime("hessi_flare_list_%Y%m.fits"))
	 
	file_paths = [base_path.joinpath(m) for m in month_list] 

	table1 = Table(fits.open(file_paths[0])[3].data)
	for f in file_paths[1:]:
		if f.exists():
			table2 = Table(fits.open(f)[3].data)
			table1 = vstack([table1, table2])
		else:
			print("{:s} doesnt exist".format(str(f)))

	table1.write('full_hessi_flares.fits')
