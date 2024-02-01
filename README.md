# Spotter Data Archive
A repo for getting started with the Sofar Spotter data archive using Python. The S3 bucket with the files (zarr and netCDF) can be viewed [here](https://sofar-spotter-archive.s3.amazonaws.com/index.html).

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
