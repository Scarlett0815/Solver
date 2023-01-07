import string
import sys
sys.path.append("py-mip")

# 求解器类型
from pymip.Config import LP_SOLVER, SCIP_SOLVER
# 求解器类
from pymip.Solver import Solver


solver = Solver(solver_name = SCIP_SOLVER)

var = 'Please input your variables to be used:\n'
var_list = []
var = str(input(var)).strip()
index = 0
while len(var) != 0:
    var = var.split(' ')
    if len(var) == 2:
        locals()[str(var[0])] = solver.new_bool_var(str(var[0]))
    elif len(var) == 4:
        if str(var[3]) == "int":
            locals()[str(var[0])] = solver.new_int_var(int(var[1]), int(var[2]), str(var[0]))
        elif str(var[3]) == 'float':
            locals()[str(var[0])] = solver.new_var(int(var[1]), int(var[2]), 0, str(var[0]))
    else:
        exit(1)
    var_list.append(locals()[str(var[0])])
    var = str(input())


const = 'Please input the constraints:\n'
const = str(input(const)).strip()
index = 0
while len(const) != 0:
    result = eval(const)
    solver.add_constraint(result, name = "constraint" + str(index))
    index += 1
    const = str(input())

target = 'Please input the target expression:\n'
target = str(input(target)).strip()
solver.set_obj(1, eval(target))


status = solver.solve()
print(f"status: {status}")
print(f"solution: ")
for var in var_list:
    print(f"{var.name} = {solver.get_var_value(var)}")
print("objective value: ", solver.objective_value)
'''
status = solver.solve()
solver.export_model(file_path="./model/model.txt")
print(f"status: {status}")
print(f"solution: ")
print(f"{a.name} = {solver.get_var_value(a)}")
print(f"{b.name} = {solver.get_var_value(b)}")
[print(f"{x[i].name} = {solver.get_var_value(x[i])}") for i in range(len(x))]
print("objective value: ", solver.objective_value)
'''