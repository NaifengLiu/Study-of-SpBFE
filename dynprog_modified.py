class Gate:
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.variables = []
        self.types = []

    def add_variable(self, variable):
        self.variables.append(variable)
        self.types.append('variable')

    def add_gate(self, gate):
        self.variables.append(gate)
        self.types.append('gate')

    def to_string(self):
        s = self.gate_type
        content = []
        for i in range(len(self.variables)):
            if self.types[i] == 'variable':
                content.append(self.variables[i])
            else:
                content.append(self.variables[i].to_string())
        return s+'('+','.join(content)+')'


gate_1 = Gate('OR')
gate_1.add_variable('x1')
gate_1.add_variable('x2')

gate_2 = Gate('AND')
gate_2.add_variable('x3')
gate_2.add_variable('x4')

gate_3 = Gate('AND')
gate_3.add_gate(gate_1)
gate_3.add_gate(gate_2)

print(gate_3.to_string())
