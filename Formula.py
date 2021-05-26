from Gate import Gate

class Formula:
    def __init__(self, gate: Gate):
        self.f = gate
        #self.sibling_classes = [[], [], []]
        self.dnf_size = self.count_dnf(gate)
        self.cnf_size = self.count_cnf(gate)
        self.goal_value = self.cnf_size * self.dnf_size
        #self.get_sibling_classes(self.f)
        self.array_type = [[], []]
        self.get_array_type(self.f)
        self.lambda_type = self.get_lambda_type()

    def get_array_type(self, gate):
        ret = [gate.gate_type]
        for each in gate.variables:
            ret.append(each)
        self.array_type[0].append(ret)
        self.array_type[1].append(gate)

        for num in range(len(gate.variables)):
            if gate.types[num] == 'gate':
                self.get_array_type(gate.variables[num])

#    def get_sibling_classes(self, gate):
#        # print(gate.to_string())
#        ret = []
#        for i in range(len(gate.variables)):
#            if gate.types[i] == 'variable':
#                ret.append(gate.variables[i])
#            else:
#                self.get_sibling_classes(gate.variables[i])
#        if len(ret) > 0:
#            self.sibling_classes[0].append(ret)
#            self.sibling_classes[1].append(gate.gate_type)
#            self.sibling_classes[2].append(gate)

    def show(self):
        print(self.f.to_string())
        # print('Done')
        return self.f.to_string()

    def find_gate_contains_variable(self, variable):
        for num in range(len(self.array_type[0])):
            each = self.array_type[0][num]
            if variable in each:
                # return each
                return [each, self.array_type[1][num]]

    def get_lambda_type(self):
        return lambda x: eval(str(self.to_lambda(self.f))[1:-1])

    def to_lambda(self, gate):
        ret = '('
        g_type = ' ' + gate.gate_type.lower() + ' '
        for i in range(len(gate.variables)):
            if gate.types[i] == 'variable':
                ret += gate.variables[i][0] + '[' + gate.variables[i][1:] + ']' + g_type
            else:
                ret += self.to_lambda(gate.variables[i]) + g_type
        ret = ' '.join(ret.split(' ')[:-2])
        ret += ')'
        return ret

    def resolve(self, variable, value):
        # print(variable)
        parent = self.find_gate_contains_variable(variable)[1]
        parent.remove(variable)
        parent.add_variable(str(value))
        # self.show()
        self.if_resolved(self.f)
        # self.show()
        # self.simplify_tree(f.f)
        self.dnf_size = self.count_dnf(self.f)
        self.cnf_size = self.count_cnf(self.f)
        self.goal_value = self.cnf_size * self.dnf_size
        #self.show()

    def count_dnf(self, gate):
        total = 1 if gate.gate_type == 'AND' else 0
        for i in range(len(gate.variables)):
            each = gate.variables[i]
            if type(each) is Gate:
                if not each.resolved:
                    newnum = self.count_dnf(each)
                    if gate.gate_type == 'AND': total *= newnum
                    if gate.gate_type == 'OR': total += newnum
            if type(each) is str:
                if not str(each[0]).isdigit():
                    newnum = 1
                    if gate.gate_type == 'AND': total *= newnum
                    if gate.gate_type == 'OR': total += newnum
        return total

    def count_cnf(self, gate):
        total = 0 if gate.gate_type == 'AND' else 1
        for i in range(len(gate.variables)):
            each = gate.variables[i]
            if type(each) is Gate:
                if not each.resolved:
                    newnum = self.count_cnf(each)
                    if gate.gate_type == 'AND': total += newnum
                    if gate.gate_type == 'OR': total *= newnum
            if type(each) is str:
                if not str(each[0]).isdigit():
                    newnum = 1
                    if gate.gate_type == 'AND': total += newnum
                    if gate.gate_type == 'OR': total *= newnum
        return total
        
    def if_resolved(self, gate):
        child_unresolved = []
        for i in range(len(gate.variables)):
            each = gate.variables[i]
            if type(each) is Gate:
                self.if_resolved(each)
                if (gate.gate_type == 'AND' and each.value == '0') or (gate.gate_type == 'OR' and each.value == '1'):
                    gate.value = each.value
                    gate.resolved = True
                    return True
                elif not each.resolved:
                    child_unresolved += [each]

            elif type(each) is str:
                if (gate.gate_type == 'AND' and each == '0') or (gate.gate_type == 'OR' and each == '1'):
                    gate.value = each
                    gate.resolved = True
                    return True
                elif not str(each[0]).isdigit():
                    child_unresolved += [each]
        # REMOVE RESOLVED VARIABLES
        # Otherwise, we get weird errors in the expression
        for each in gate.variables: 
            if each not in child_unresolved:
                gate.remove(each)
        gate.variables = child_unresolved
        if len(child_unresolved) > 0:
            gate.resolved = False
            return False
        gate.value = '0' if gate.gate_type == 'OR' else '1'
        return True

