# Standard imports
import os

# Third-party library imports
import pandas as pd
import numpy as np
import datetime
# Internal imports
from pypsse.modes.abstract_mode import AbstractMode

class Static(AbstractMode):
    def __init__(self,psse, dyntools, settings, export_settings, logger, subsystem_buses, raw_data):
        super().__init__(psse, dyntools, settings, export_settings, logger, subsystem_buses, raw_data)
        self.time = settings.simulation.start_time
        self._StartTime = settings.simulation.start_time
        self.incTime = settings.simulation.simulation_step_resolution 
        return

    def init(self, bussubsystems):
        super().init(bussubsystems)
        self.initialization_complete = True
        return

    def step(self, dt):
        ierr = self.PSSE.fnsl()
        # check if powerflow completed successfully
        if ierr == 0:
            self.time = self.time + self.incTime
        else:
            raise Exception(f'Error code {ierr} returned from PSSE while running powerflow, please follow \
                            PSSE doumentation to know more about error')

    def resolveStep(self, t):
        ierr = self.PSSE.fnsl()
        if ierr > 0:
            raise Exception(f'Error code {ierr} returned from PSSE while running powerflow, please follow \
                                        PSSE doumentation to know more about error')
    def getTime(self):
        return self.time

    def GetTotalSeconds(self):
        return (self.time - self._StartTime).total_seconds()

    def GetStepSizeSec(self):
        return self.settings.simulation.simulation_step_resolution.total_seconds()

    def export(self):
        self.logger.debug('Starting export process. Can take a few minutes for large files')
        excelpath = os.path.join(self.export_path, self.settings["Excel file"])
        achnf = self.dyntools.CHNF(self.outx_path)
        achnf.xlsout(channels='', show=False, xlsfile=excelpath, outfile='', sheet='Sheet1', overwritesheet=True)
        self.logger.debug('{} exported'.format(self.settings.export.excel_file))
