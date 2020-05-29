from astropy.table import Table, unique
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u 
from sunpy.coordinates import frames
from sunpy.time import parse_time
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 

def save_to_csv():

	flags = [x for x in fits.open('/Users/lahayes/ssw/hessi/dbase/hessi_flare_list_200202.fits')[2].data['FLAG_IDS'][0]]

	data = Table(fits.open("full_hessi_flares.fits")[1].data)

	data_flares = data[data['GOES_CLASS'] != " "]

	flag_df = pd.DataFrame(data=np.array(data_flares['FLAGS']), columns=flags)



	data_flares['X'], data_flares['Y'] = data_flares['POSITION'][:,0], data_flares['POSITION'][:,1]
	data_flares['flag_solar'] = flag_df['SOLAR']
	data_flares['flag_pos_quality'] = flag_df['POSITION_QUALITY']
	data_flares['flag_solar_unconfimed'] = flag_df['SOLAR_UNCONFIRMED']

	data_df = data_flares[['START_TIME', 'PEAK_TIME', 'GOES_CLASS', 'X', 'Y', 
						   'TOTAL_COUNTS', 'PEAK_COUNTRATE', 'flag_solar', 'flag_pos_quality',
						   	'flag_solar_unconfimed']].to_pandas()

	tt = [parse_time(x, format='utime').datetime for x in data_df['START_TIME']] 

	data_df['time_dt'] = tt

	data_df['short_goes_class'] = [x[0] for x in data_df['GOES_CLASS']]

	#coord_hpc_nofix = SkyCoord(data_df['X']*u.arcsec, data_df['Y']*u.arcsec, frame=frames.Helioprojective(observer='Earth', obstime='2002-02-28')) 
	coords_hpc = SkyCoord(data_df['X']*u.arcsec, data_df['Y']*u.arcsec, frame=frames.Helioprojective(observer='Earth', obstime=list(data_df['time_dt']))) 

	#coord_hgc_nofix = coord_hpc_nofix.transform_to(frames.HeliographicCarrington)
	coord_hgc = coords_hpc.transform_to(frames.HeliographicCarrington)

	data_df['hgc_lat'] = coord_hgc.lat.value
	data_df['hgc_lon'] = coord_hgc.lon.value

	data_df.to_csv('full_hessi_flares_cleaned.csv', index_label=False)
	

data_df = pd.read_csv('full_hessi_flares_cleaned.csv')
# xx = data_df['X']
# yy = data_df['Y']
# size = data_df['goes_class_size']
# fig, ax = plt.subplots()
# circle1 = plt.Circle((0, 0), 959.63, color='k', fill=False)
# cs = ax.scatter(xx, yy, c=size, s=size, cmap='jet')#, alpha=0.5, edgecolor='k')
# ax.add_artist(circle1)
# ax.set_xlim(-1500, 1500)
# ax.set_ylim(-1500, 1500)
# ax.set_aspect('equal', adjustable='box')
# fig.colorbar(cs)
# plt.show()




