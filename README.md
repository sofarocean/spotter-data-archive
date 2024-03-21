# Spotter Data Archive

Data in this archive is to be used in accordance with the [Sofar Ocean Spotter Data Archive License](https://sofarocean.notion.site/Sofar-Data-Access-Agreement-fe4e091fa0b5453d9a8bd97c4b6940d5).

![example_spotter_map](https://github.com/sofarocean/spotter-data-archive/assets/54418491/2c0949f6-6f67-4497-b3dc-8062fba01ef7)

This repository is for getting started with the Sofar Spotter data archive using Python. 
The S3 bucket with the files (zarr and netCDF) can be viewed [here](https://sofar-spotter-archive.s3.amazonaws.com/index.html).

Example scripts are provided in the `examples/` directory to get started with the data.

## Data Overview
This archive includes two datasets - one containing bulk wave parameters and the other containing wave spectra
from the Sofar Spotter global buoy network, named spotter_data_bulk* and spotter_data_spectra*, respectively.
Two versions of each dataset are available, one as a traditional NetCDF (.nc) and one in
[Zarr](https://wiki.earthdata.nasa.gov/display/ESO/Zarr+Format#:~:text=Zarr%20is%20a%20relatively%20new,the%20data%20in%20predefined%20chunks.) format (_zarr/). 
Data utilizes `trajectory` as a primary dimension in order to concatentate multiple records of varying length.
### `spotter_data_bulk`
Dimensions of the data are index (count in full record) and trajectory (ID associated with buoy).

Data variables include `latitude`, `longitude`, `meanDirection`, `meanDirectionalSpread`, `meanPeriod`, `peakDirection`,
`peakDirectionalSpread`, `peakPeriod`, and `significantWaveHeight` with coordinate `index` (i.e. all observations in 
record concatenated in one long array). An additional variable `rowsize` has the dimension `trajectory`, and describes
how many observations from a given buoy. `rowsize` can then be used to slice the observations by `trajectory` (buoy ID). See
`examples/spotter_bulk.ipynb` for an example of how to use this variable.

### `spotter_data_spectra`
Dimensions of the data are index (count in full record), frequency (Hz), and trajectory (ID associated with buoy).

Data variables include `variance_density`, `a1` , `a2`,`b1`, `b2`, `latitude`, `longitude`, `rowsize`, `significantWaveHeight`, and
`u10` (windspeed at 10 m). See [Spotter Technical Manual](https://content.sofarocean.com/hubfs/Spotter%20product%20documentation%20page/Sofar%20-%20Technical_Reference_Manual.pdf) 
for details on wave spectra definitions from directional wave buoys like Spotter.




## Setup
To get started, in your terminal,

via ssh:
```bash
git clone git@github.com:sofarocean/spotter-data-archive.git  # for ssh clone
````
or if you prefer https: 
```bash
git clone https://github.com/sofarocean/spotter-data-archive.git
```


```bash
# (optional, set up python environment)
python3 -m venv ./.venv
source ./.venv/bin/activate  # this activates the new environment

# install dependencies that are listed in requirements.txt
pip3 install -r requirements.txt

```

## Running Jupyter notebooks
In your terminal, with your environment activated,
```bash
jupyter notebook
```
This should open a directory navigator in your browser where you can navigate to `examples/` and select an .ipynb notebook.

If you encounter an error when importing packages related to the Python package `libproj`, install the following in your virtual environment. 

```bash
brew install gdal
```

Make sure to restart terminal/Jupyter Notebook before attempting to rerun the scripts. 

## Contributing
We encourage community contribution of example scripts and specific analysis done using this dataset via pull request. Contact isabel.houghton@sofarocean.com with any questions.
