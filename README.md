# solomon-analysis

## Instructions for reproducing these analyses

- Get a copy of these analyses

`git clone https://github.com/LAAC-LSCP/solomon-analysis.git`

### Reproducing the extraction of stats

To get the raw annotation data from the recordings, you need to:

- have created a github account and communicated your username so that you have been added to the private repository containing links to the data, have a way to access the secure server (so you must have credentials to access it & have set it up correctly)
- if you've never worked with our datasets before, install git-annex `apt install git-annex` or `brew install git-annex` and datalad `pip install datalad` (or `pip install datalad --user in case of permission issues)
- (sometimes, depending on your system) create a local environment based on python 3 and activate it: `python3.6 -m venv ~/ChildProjectVenv` followed by `source ~/ChildProjectVenv/bin/activate`
-  open a terminal window and follow these steps to make a local copy of the data:

```
datalad install https://github.com/LAAC-LSCP/solomon-data.git
cd solomon-data
datalad run-procedure setup f-oberon #this step needs to be revised depending on how you access the secure server
datalad get annotations
```

Then navigate to the solomon-analysis and launch vc.py like this:

`python scripts/vc.py $DATA`

where $DATA is the absolute path to your local copy of the solomon-data


### Reproducing the shift analyses

**TODO**

### Reproducing the report

**TODO**