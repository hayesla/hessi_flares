import pandas as pd 
import numpy as np

column_names = ['flare_id', 'date', 'start', 'peak', 'end',
				'dur', 'peak_cts', 'total_counts', 'energy_range',
				'X', 'Y', 'radial', 'AR', 'flag1']

columns_to_use = np.arange(len(column_names))
dtypes = dtype=(int, str, str, str, str, float, float, float,
				str, float, float, float, float, str)

dtype_dict = dict()
for i in range(len(column_names)):
	dtype_dict[column_names[i]] = dtypes[i]

data = pd.read_csv('hessi_flare_list.txt', delim_whitespace=True, 
					skiprows=7, nrows=121180, usecols=columns_to_use, names=column_names,
					dtype=dtype_dict) 


tstart = parse_time('12-Feb-2002')
tend = parse_time('12-Mar-2008')
#tend = parse_time('3-Mar-2018')
dates = [tstart.strftime('%d-%b-%Y')]
while tend>tstart:
	tstart = tstart + datetime.timedelta(days=1)
	dates.append(tstart.strftime('%d-%b-%Y'))

def test_times():
	t1 = time.time()
	for i in range(10):
		date = dates[i]
		plot_date(i, date)
	print(time.time() - t1)


	t1 = time.time()
	for i in range(10):
		date = dates[i]
		plot_date2(i, date)
	print(time.time() - t1)

i = 0 

t1 = time.time()
date_plot, lat_plot = [], []
for i in range(0, len(data), 10):
	print(i)
	date = parse_time(data.iloc[i]['date']).datetime

	coord1 = SkyCoord(data.iloc[i]['X']*u.arcsec, data.iloc[i]['Y']*u.arcsec,
					  frame=frames.Helioprojective(observer='Earth', obstime=date)).transform_to(frames.HeliographicCarrington)

	date_plot.append(date)
	lat_plot.append(coord1.lat.value)
print(time.time() - t1)



savedir = '/Users/lahayes/space_weather_stuff/hessi_flares/plots/'
def plot_date(i, date):
	print(i)
	data_plot = data[data['date'].isin([date])]


	data_arr = np.zeros((2000, 2000))

	coord = SkyCoord(0*u.arcsec, 0*u.arcsec, frame=frames.Helioprojective(observer='Earth', obstime=date))
	header = sunpy.map.make_fitswcs_header(data_arr, coord, scale=[1.5, 1.5]*u.arcsec/u.pix)
	mapy = sunpy.map.Map(data_arr, header)

	coord1 = SkyCoord(data_plot['X']*u.arcsec, data_plot['Y']*u.arcsec,
					  frame=frames.Helioprojective(observer='Earth', obstime=date))

	fig = plt.figure()
	ax = fig.add_subplot(projection=mapy)
	mapy.plot(alpha=0, title=date)
	mapy.draw_limb(color='k')
	mapy.draw_grid(lw=0.5, color='grey')
	ax.plot_coord(coord1, marker='o', color='r', ls='')

	plt.savefig(savedir + 'test_{:d}.png'.format(i), dpi=200)
	plt.close()

def plot_date2(i, date):

	circle1 = plt.Circle((0, 0), 959.63, color='k', fill=False)
	data_plot = data[data['date'].isin([date])]

	xx = data_plot['X']
	yy = data_plot['Y']
	size = data_plot['total_counts']
	fig, ax = plt.subplots()

	ax.add_artist(circle1)
	ax.set_xlim(-1500, 1500)
	ax.set_ylim(-1500, 1500)
	ax.set_aspect('equal', adjustable='box')

	ax.scatter(xx, yy, marker='o', s=10*np.log10(size), c=np.log10(size))

	plt.savefig(savedir + 'test2_{:d}.png'.format(i), dpi=200)
	plt.close()
