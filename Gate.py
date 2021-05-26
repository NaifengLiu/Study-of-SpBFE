class Gate:
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.variables = []
        self.types = []
        self.resolved = False
        self.value = None

    def add_variable(self, variable):
        self.variables.append(variable)
        self.types.append('variable')

    def add_gate(self, gate):
        self.variables.append(gate)
        self.types.append('gate')

    def remove(self, variable):
        tmp_variables = []
        tmp_types = []
        for i in range(len(self.variables)):
            if self.variables[i] != variable:
                tmp_variables.append(self.variables[i])
                tmp_types.append(self.types[i])
        self.variables = tmp_variables
        self.types = tmp_types

    def to_string(self):
        if self.resolved is False:
            s = self.gate_type
            content = []
            for i in range(len(self.variables)):
                if self.types[i] == 'variable':
                    content.append(self.variables[i])
                else:
                    content.append(self.variables[i].to_string())
            return s + '(' + ','.join(content) + ')'
        else:
            return ''

