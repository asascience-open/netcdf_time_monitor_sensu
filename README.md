# NetCDF time checker

A Sensu plugin written in Python which checks the last recorded time in a local or remote NetCDF dataset against a threshold time.

## Requirements

The plugin requires the Python package `sensu_plugin` and `netCDF4`.

## Invocation/options

Set up the sensu checks to point at `netcdf_time_monitor.py`

Command line arguments for this module are

`-d, --dataset` A required string argument with either a local file path to a netCDF file or a remote OPeNDAP dataset.
`-w --warntime` A floating point number representing the number of hours before the present time is reported as the warn state.  Defaults to 12 hours if left unspecified.
`-c --crittime` A floating point number representing the number of hours before the present time is reported as the warn state.  Defaults to 24 hours if left unspecified.
`-v --variable`  A string with the desired time variable name to check.  Defaults to 'time' if left unspecified.

*Example invocation*

```./netcdf_time_monitor.py -d 'http://data.oceansmap.com/thredds/dodsC/ndbc_agg/ygnn6/ygnn6.ncml' -w 12 -c 6 -v 'time'```

Retrieves the aggregated THREDDS dataset from [http://data.oceansmap.com/thredds/dodsC/ndbc_agg/ygnn6/ygnn6.ncml](http://data.oceansmap.com/thredds/dodsC/ndbc_agg/ygnn6/ygnn6.ncml), sets the warn threshold to 12 hours, sets the critical threshold to 6 hours, and uses the variable named 'time' to compare against the current time.

## Known issues/quirks

Setting critical time less than or equal to warn time will make warning state unreachable.
