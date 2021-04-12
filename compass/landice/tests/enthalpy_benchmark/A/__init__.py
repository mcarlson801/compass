from importlib.resources import path

from compass.io import symlink
from compass.config import add_config
from compass.validate import compare_variables
from compass.landice.tests.enthalpy_benchmark.setup_mesh import SetupMesh
from compass.landice.tests.enthalpy_benchmark.run_model import RunModel
from compass.landice.tests.enthalpy_benchmark.A.visualize import Visualize
from compass.testcase import TestCase


class A(TestCase):
    """
    The Kleiner enthalpy benchmark test case A

    Attributes
    ----------
    """

    def __init__(self, test_group):
        """
        Create the test case

        Parameters
        ----------
        test_group : compass.landice.tests.enthalpy_benchmark.EnthalpyBenchmark
            The test group that this test case belongs to
        """
        super().__init__(test_group=test_group, name='A')
        module = self.__module__

        SetupMesh(test_case=self)

        restart_filenames = ['../setup_mesh/landice_grid.nc',
                             '../phase1/restart.100000.nc',
                             '../phase2/restart.150000.nc']
        for index, restart_filename in enumerate(restart_filenames):
            name = 'phase{}'.format(index+1)
            step = RunModel(test_case=self, cores=1, threads=1, name=name,
                            subdir=name, restart_filename=restart_filename)

            suffix = 'landice{}'.format(index+1)
            step.add_namelist_file(module, 'namelist.{}'.format(suffix))
            step.add_streams_file(module, 'streams.{}'.format(suffix))

        Visualize(test_case=self)

    def configure(self):
        """
        Modify the configuration options for this test case
        """
        add_config(self.config, 'compass.landice.tests.enthalpy_benchmark.A',
                   'A.cfg', exception=True)

        with path('compass.landice.tests.enthalpy_benchmark', 'README') as \
                target:
            symlink(str(target), '{}/README'.format(self.work_dir))

    def run(self):
        """
        Run each step of the test case
        """
        # run the steps
        super().run()
        variables = ['temperature', 'basalWaterThickness',
                     'groundedBasalMassBal']
        compare_variables(variables, self.config, work_dir=self.work_dir,
                          filename1='phase3/output.nc')
