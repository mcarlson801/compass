from compass.validate import compare_variables
from compass.ocean.tests.global_ocean.forward import ForwardTestCase, \
    ForwardStep


class DecompTest(ForwardTestCase):
    """
    A test case for performing two short forward runs to make sure the results
    are identical with 4 and 8 cores
    """

    def __init__(self, test_group, mesh, init, time_integrator):
        """
        Create test case

        Parameters
        ----------
        test_group : compass.ocean.tests.global_ocean.GlobalOcean
            The global ocean test group that this test case belongs to

        mesh : compass.ocean.tests.global_ocean.mesh.Mesh
            The test case that produces the mesh for this run

        init : compass.ocean.tests.global_ocean.init.Init
            The test case that produces the initial condition for this run

        time_integrator : {'split_explicit', 'RK4'}
            The time integrator to use for the forward run
        """
        super().__init__(test_group=test_group, mesh=mesh, init=init,
                         time_integrator=time_integrator,
                         name='decomp_test')
        for procs in [4, 8]:
            name = '{}proc'.format(procs)
            self.add_step(
                ForwardStep(test_case=self, mesh=mesh, init=init,
                            time_integrator=time_integrator, name=name,
                            subdir=name, cores=procs, threads=1))

    def run(self):
        """
        Run each step of the testcase
        """
        # get cores, threads from config options and run the steps
        super().run()

        variables = ['temperature', 'salinity', 'layerThickness',
                     'normalVelocity']
        steps = self.steps_to_run
        if '4proc' in steps and '8proc' in steps:
            compare_variables(variables, self.config, work_dir=self.work_dir,
                              filename1='4proc/output.nc',
                              filename2='8proc/output.nc')
