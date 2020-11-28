# solomon-analysis

## Usage

**Before anything, you need to install the [ChildProject package](https://github.com/LAAC-LSCP/ChildRecordsData#installation)**

### Install solomon's dataset

Read the instructions to install a dataset [here](https://laac-lscp.github.io/ChildRecordsData/PROJECTS.html#installing-a-dataset).

Once the dataset has been installed, `cd` into it and retrieve the annotations :

```
# Install the dataset
child-project import-data https://github.com/LAAC-LSCP/solomon-data.git --destination /path/to/solomon/dataset --storage-hostname foberon

Remember that if you have an identification error, your GitHub SSH keys may not be set up properly. See instructions to fix that [here](https://jdblischak.github.io/2014-09-18-chicago/novice/git/05-sshkeys.html).

# Fetch annotations from Oberon
cd solomon-data
datalad get annotations
```

### Run the analysis

1. `cd` into your local solomon-analysis repository after cloning it
2. Generate the metrics :

```
python scripts/vc.py /path/to/solomon/dataset
```




