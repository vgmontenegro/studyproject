import geopandas
import matplotlib.pyplot as plt

gf = geopandas.read_file("Nova_Holanda_2022.shx")
gf['area'] = gf.area
gf.plot('area')
plt.show()