#!/usr/bin/env python
from sensu_plugin import SensuPluginCheck
from netCDF4 import Dataset, num2date
from datetime import datetime

"""Check that a thredds data source is up to date."""


class NetCDFTimeCheck(SensuPluginCheck):
    def setup(self):
        self.parser.add_argument('-d', '--dataset', type=str, required=True,
                                 help='Path to remote or local NetCDF dataset')
        self.parser.add_argument('-w', '--warntime', type=float, default=12,
                                 help='Number of hours before considered warn')
        self.parser.add_argument('-c', '--crittime', type=float, default=24,
                                 help='Number of hours before considered '
                                      'crit')
        self.parser.add_argument('-v', '--variable', type=str, default='time',
                                 help='Time variable to check')

    def run(self):
        self.check_name('netcdf_time_check')
        try:
            ds = Dataset(self.options.dataset)
        except IOError as io_exc:
            self.critical(io_exc)
        time_var = ds.variables[self.options.variable]
        if not len(time_var):
            self.critical("No data present in variable {}".format(time_var))
        # check for calendar, or default to gregorian if unspecified
        calendar = getattr(time_var, 'calendar', 'gregorian')
        # times should be monotonically increasing, so take final time as latest
        last_time = num2date(time_var[-1], time_var.units, calendar)
        # get the time in hours since last updated.
        delta_t_hours = (datetime.utcnow() - last_time).total_seconds() / 3600
        # should crittime < warntime be considered an error condition?
        thresh_msg = "Last time of {} UTC exceeds {} threshold of {} hours"
        if delta_t_hours >= self.options.crittime:
            self.critical(thresh_msg.format(last_time, 'critical', self.options.crittime))
        if delta_t_hours >= self.options.warntime:
            self.warning(thresh_msg.format(last_time, 'warning', self.options.warntime))
        else:
            self.ok("Last update time of {} UTC is within acceptable time "
                    "bounds".format(last_time))

if __name__ == "__main__":
    f = NetCDFTimeCheck()
