# solomon-analysis

## Usage

**Before anything, you need to install the [ChildProject package](https://github.com/LAAC-LSCP/ChildRecordsData#installation)**

### Setup

```
datalad install -r https://github.com/LAAC-LSCP/solomon-analysis.git
cd solomon-data
datalad run-procedure setup foberon
datalad get annotations
```

### Run the scripts

```
cd ..
python scripts/vc.py solomon-data
```


