
from sunpy.time import parse_time
from dateutil.relativedelta import relativedelta 
import urllib 
import os


base_path = Path("/Users/lahayes/ssw/hessi/dbase/")
tstart = parse_time('2002-02-01').datetime
tend = parse_time('2018-03-01').datetime
month_list = [tstart.strftime('hessi_flare_list_%Y%m.fits')]
while tend>tstart:
	tstart = tstart + relativedelta(months=1)
	month_list.append(tstart.strftime('hessi_flare_list_%Y%m.fits'))

def online_fits():
	base_url = "https://hesperia.gsfc.nasa.gov/hessidata/dbase"
	url_paths = [os.path.join(base_url, m) for m in month_list]
	for url in url_paths:

		try:
			aa = urllib.request.urlretrieve(url, url.split('/')[-1])

		except urllib.error.HTTPError as e:
			print(e.reason)
			print(url)