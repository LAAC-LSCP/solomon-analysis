# solomon-analysis

## Usage

**Before anything, you need to install the [ChildProject package](https://github.com/LAAC-LSCP/ChildRecordsData#installation)**

### Install solomon's dataset

Read the instructions to install a dataset [here](https://laac-lscp.github.io/ChildRecordsData/PROJECTS.html#installing-a-dataset).

Once the dataset has been installe, `cd` into it and retrieve the annotations :

```
# Install the dataset
child-project import-data https://github.com/LAAC-LSCP/solomon-data.git --destination /path/to/solomon/dataset --storage-hostname foberon

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




