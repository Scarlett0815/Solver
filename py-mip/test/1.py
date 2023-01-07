import sys
sys.path.append("..")

# 求解器类型
from pymip.Config import CP_SAT_SOLVER, LP_SOLVER, SCIP_SOLVER
# 求解器类
from pymip.Solver import Solver
solver = Solver(solver_name = SCIP_SOLVER)

# 创建决策变量、添加约束及目标函数
a = solver.new_var(-0.5, 0.1, 0,"a")
b = solver.new_var(-0.5, 0.1, 0, "b")
x = [solver.new_bool_var(f"x{i}") for i in range(10)]
sum_x = sum([item for item in x])
#a, b,x, sum_x
# 添加约束
con_1 = (3 * a + b / 2) - 10 + sum_x == 0
con_2 = x[0] >= x[1]
solver.add_constraint(con_1, name = "constraint 1")
solver.add_constraint(con_2, name = "constraint 2")
#con_1, con_2
# 添加目标函数
solver.set_obj(3, a)
for item_x in x:
    solver.set_obj(2, item_x)
solver.set_obj(5, b)
# 求解、输出模型文件及查看解
status = solver.solve()
solver.export_model(file_path="./model/model.txt")
print(f"status: {status}")
print(f"solution: ")
print(f"{a.name} = {solver.get_var_value(a)}")
print(f"{b.name} = {solver.get_var_value(b)}")
[print(f"{x[i].name} = {solver.get_var_value(x[i])}") for i in range(len(x))]
print("objective value: ", solver.objective_value)
