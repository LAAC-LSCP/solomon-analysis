# solomon-analysis

## Usage

**Before anything, you need to install the [ChildProject package](https://github.com/LAAC-LSCP/ChildRecordsData#installation)**

### Setup

```
datalad install -r https://github.com/LAAC-LSCP/solomon-analysis.git
cd solomon-data
datalad run-procedure setup oberon
datalad get annotations
```

- **Replace `oberon` by whatever alias you use to ssh into oberon if it is different. The ssh hostname should be configured into your ssh config file, usually in `~/.ssh/config`. Instructions on how to configure your ssh access to Oberon are available [here](https://wiki.syntheticlearner.net/Computer_resources/ssh_conf.html).**
- Remember that if you have an identification error, your GitHub SSH keys may not be set up properly. See instructions to fix that [here](https://jdblischak.github.io/2014-09-18-chicago/novice/git/05-sshkeys.html).


### Run the scripts

From the root of the repository:

```bash
python scripts/vc.py solomon-data       # compute vocalization counts and other statistics for each recording
```


