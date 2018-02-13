__author__ = "Christian Kongsgaard"
__license__ = "MIT"

# -------------------------------------------------------------------------------------------------------------------- #
# Imports

# Module imports
import os
import subprocess

# Livestock imports
import misc as gh_misc
import templates

# Grasshopper imports
import Grasshopper.Kernel as gh
import scriptcontext as sc

# -------------------------------------------------------------------------------------------------------------------- #
# Grasshopper Component Class


class GHComponent:

    def __init__(self, ghenv):
        self.outputs = None
        self.inputs = None
        self.description = None
        self.gh_env = ghenv
        self.name = 'Test'
        self.nick_name = None
        self.message = None
        self.category = None
        self.subcategory = None

    # COMPONENT STUFF
    def config_component(self):
        """
        Sets up the component, with the following steps:
        - Load component data
        - Generate component data
        - Generate outputs
        - Generate inputs
        """


        # Generate component data
        self.gh_env.Component.Name = self.name
        self.gh_env.Component.NickName = self.nick_name
        self.gh_env.Component.Message = self.message
        self.gh_env.Component.IconDisplayMode = self.gh_env.Component.IconDisplayMode.application
        self.gh_env.Component.Category = self.category
        self.gh_env.Component.SubCategory = self.subcategory
        self.gh_env.Component.Description = self.description

        # Generate outputs:
        for output_ in range(len(self.outputs)):
            self.add_output_parameter(output_)

        # Generate inputs:
        for input_ in range(len(self.inputs)):
            self.add_input_parameter(input_)

    def add_warning(self, warning):
        """
        Adds a Grasshopper warning to the component.
        :param warning: Warning text.
        """

        print(warning)
        w = gh.GH_RuntimeMessageLevel.Warning
        self.gh_env.Component.AddRuntimeMessage(w, warning)

    def add_output_parameter(self, output_):
        """
        Adds an output to the Grasshopper component.
        :param output_: Output index.
        """

        self.gh_env.Component.Params.Output[output_].NickName = self.outputs[output_]['name']
        self.gh_env.Component.Params.Output[output_].Name = self.outputs[output_]['name']
        self.gh_env.Component.Params.Output[output_].Description = self.outputs[output_]['description']

    def add_input_parameter(self, input_):
        """
        Adds an input to the Grasshopper component.
        :param input_: Input index.
        """

        # Set information
        self.gh_env.Component.Params.Input[input_].NickName = self.inputs[input_]['name']
        self.gh_env.Component.Params.Input[input_].Name = self.inputs[input_]['name']
        self.gh_env.Component.Params.Input[input_].Description = self.inputs[input_]['description']

        # Set type access
        if self.inputs[input_]['access'] == 'item':
            self.gh_env.Component.Params.Input[input_].Access = gh.GH_ParamAccess.item
        elif self.inputs[input_]['access'] == 'list':
            self.gh_env.Component.Params.Input[input_].Access = gh.GH_ParamAccess.list
        elif self.inputs[input_]['access'] == 'tree':
            self.gh_env.Component.Params.Input[input_].Access = gh.GH_ParamAccess.tree

    def add_default_value(self, parameter, param_number):
        """
        Adds a default value to a parameter.
        :param parameter: Parameter to add default value to
        :param param_number: Parameter number
        :return: Parameter
        """

        if not parameter:
            return self.inputs[param_number]['default_value']
        else:
            return parameter


class PythonExecutor(GHComponent):

    def __init__(self, ghenv):
        GHComponent.__init__(self, ghenv)

        def inputs():
            return {0: {'name': 'PythonPath',
                        'description': 'Path to python.exe',
                        'access': 'item',
                        'default_value': None}}

        def outputs():
            return {0: {'name': 'readMe!',
                        'description': 'In case of any errors, it will be shown here.'}}

        self.inputs = inputs()
        self.outputs = outputs()
        self.description = 'Path to python executor'
        self.name = 'Python Executor'
        self.py_exe = None
        self.checks = False
        self.results = None

    def check_inputs(self):
        """
        Checks inputs and raises a warning if an input is not the correct type.
        """

        if os.path.exists(self.py_exe):
            self.checks = True
        else:
            warning = 'Component can not find Python'
            self.add_warning(warning)

    def config(self):
        """
        Generates the Grasshopper component.
        """

        self.config_component()

    def run_checks(self, py_exe):
        """
        Gathers the inputs and checks them.
        :param py_exe: Path to python.exe
        """

        # Gather data
        self.py_exe = py_exe

        # Run checks
        self.check_inputs()

    def run(self):
        """
        In case all the checks have passed the component runs.
        It prints the python.exe path and creates a scriptcontext.sticky with the path.
        """

        if self.checks:
            print('Python Executor is set to: ' + self.py_exe)

            sc.sticky['PythonExe'] = self.py_exe


class MyComponent(GHComponent):

    def __init__(self, ghenv):
        GHComponent.__init__(self, ghenv)

        def inputs():
            return {0: {'name': 'MyInput',
                        'description': 'Input',
                        'access': 'item',
                        'default_value': None},

                    1: {'name': 'ResultFolder',
                        'description': 'Folder where the result files should be saved',
                        'access': 'item',
                        'default_value': None},

                    2: {'name': 'Run',
                        'description': 'Run the component',
                        'access': 'item',
                        'default_value': None}
                    }

        def outputs():
            return {0: {'name': 'readMe!',
                        'description': 'In case of any errors, it will be shown here.'},

                    1: {'name': 'MyResult',
                        'description': 'Result'},
                    }

        self.inputs = inputs()
        self.outputs = outputs()
        self.name = 'My Component'
        self.my_input = None
        self.folder = None
        self.run_component = None
        self.py_exe = gh_misc.get_python_exe()
        self.checks = False
        self.results = None

    def check_inputs(self):
        """
        Checks inputs and raises a warning if an input is not the correct type.
        """

        if self.run_component:
            self.checks = True

    def config(self):
        """
        Generates the Grasshopper component.
        """

        # Generate Component
        self.config_component()

    def run_checks(self, my_input, folder, run):

        """
        Gathers the inputs and checks them.

        :param my_input: Input
        :param folder: Folder where the result files should be saved.
        :param run: Whether or not to run the component.
        """

        # Gather data
        self.my_input = my_input
        self.folder = self.add_default_value(folder, 1)
        self.run_component = self.add_default_value(run, 2)

        # Run checks
        self.check_inputs()

    def write_files(self):
        """
        Write the files.
        """

        # Initialize
        files_written = []

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        # Write
        my_file = 'my_file.txt'
        file_obj = open(self.folder + '/' + my_file, 'w')
        for row in self.my_input:
            file_obj.write(','.join(str(element)
                                    for element in row) + '\n')
        file_obj.close()
        files_written.append(my_file)

        # Template
        files_written.append(templates.pick_template('my_template', self.folder))

        return True

    def do_case(self):
        """
        Runs the case. Spawns a subprocess to run either the local or ssh template.
        """

        template_to_run = self.folder + '/my_template.py'

        # Run template
        thread = subprocess.Popen([self.py_exe, template_to_run])
        thread.wait()
        thread.kill()

        return True

    def load_results(self):
        """
        Loads the results from the results files and adds them to self.results.
        """

        self.results = open(self.folder + '/my_result.txt', 'r').readlines()

        return True

    def run(self):
        """
        In case all the checks have passed and run is True the component runs.
        The following functions are run - in this order.
        write_files()
        do_case()
        load_results()
        """

        if self.checks and self.run_component:
            self.write_files()
            self.do_case()
            self.load_results()