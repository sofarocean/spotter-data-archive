# Spotter Data Archive
A repo for getting started with the Sofar Spotter data archive using Python.

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

## Contributing
We encourage community contribution of example scripts and specific analysis done using this dataset via pull request. Contact isabel.houghton@sofarocean.com with any questions.
