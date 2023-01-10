import string
import sys
sys.path.append("py-mip")
import wx

# 求解器类型
from pymip.Config import LP_SOLVER, SCIP_SOLVER
# 求解器类
from pymip.Solver import Solver

import eyed3
import glob

var_list = []
solver = Solver(solver_name = SCIP_SOLVER)

class Mp3Panel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.row_obj_dict = {}

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 100), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, 'Var', width=100)
        self.list_ctrl.InsertColumn(1, 'Type', width=100)
        self.list_ctrl.InsertColumn(2, 'Lower', width=100)
        self.list_ctrl.InsertColumn(3, 'Upper', width=100)
        self.var_list = []
        self.type_list = []
        self.lower_list = []
        self.upper_list = []

    def update_mp3_listing(self):
        self.row_obj_dict = {}

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 100), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, 'Var', width=100)
        self.list_ctrl.InsertColumn(1, 'Type', width=100)
        self.list_ctrl.InsertColumn(2, 'Lower', width=100)
        self.list_ctrl.InsertColumn(3, 'Upper', width=100)
        index = 0
        for var, type, lower, upper in zip(self.var_list, self.type_list, self.lower_list, self.upper_list):
            #print(var)
            #print(type)
            #print(lower)
            #print(upper)
            self.list_ctrl.InsertItem(index,str(var))
            self.list_ctrl.SetItem(index, 1,str(type))
            self.list_ctrl.SetItem(index, 2,str(lower))
            self.list_ctrl.SetItem(index, 3,str(upper))
            index += 1

class Mp3Panel1(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.row_obj_dict = {}

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 100), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, 'Constraints', width=400)

        self.const_list = []

    def update_mp3_listing(self):
        self.row_obj_dict = {}

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 100), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, 'Constraints', width=400)

        index = 0
        for constraint in self.const_list:
            #print(var)
            #print(type)
            #print(lower)
            #print(upper)
            self.list_ctrl.InsertItem(index,constraint)
            index += 1

class MyFrame3(wx.Frame):    
    def __init__(self, parent):
        super().__init__(parent, title='Solver')
        const_text = wx.StaticText(self, label='Target', pos = (10, 10))
        self.target = wx.TextCtrl(self, pos = (100, 10))

        finish_btn = wx.Button(self, label='Solve',pos = (175, 50))
        finish_btn.Bind(wx.EVT_BUTTON, self.finish_on_press)
        self.index = 0
        self.Show()

    def finish_on_press(self, event):
        for var in var_list:
            locals()[var.name] = var
        target_con = eval(self.target.GetValue())
        solver.set_obj(1, target_con)
        solver.solve()
        status = solver.solve()
        wx.StaticText(self ,label = "status: " + str(status), pos = (10, 90))
        wx.StaticText(self ,label = "solution: ", pos = (10, 110))
        index = 130
        for var in var_list:
            wx.StaticText(self ,label =str(var.name) + " = "+ str(solver.get_var_value(var)), pos = (10, index))
            index += 20
        wx.StaticText(self ,label = "objective value: "+ str(solver.objective_value), pos = (10, index))

class MyFrame2(wx.Frame):    
    def __init__(self, parent):
        super().__init__(parent, title='Solver')
        self.panel = Mp3Panel1(self)
        const_text = wx.StaticText(self.panel, label='Constraint', pos = (10, 110))
        self.const = wx.TextCtrl(self.panel, pos = (100, 110))

        add_btn = wx.Button(self.panel, label='Add Constraint',pos = (70, 175))
        add_btn.Bind(wx.EVT_BUTTON, self.add_on_press)
        finish_btn = wx.Button(self.panel, label='Finish',pos = (215, 175))
        finish_btn.Bind(wx.EVT_BUTTON, self.finish_on_press)
        self.index = 0
        self.Show()
    def add_on_press(self, event):
        const_con = self.const.GetValue()
        for var in var_list:
            locals()[var.name] = var
        self.panel.const_list.append(const_con)
        result = eval(const_con)
        solver.add_constraint(result, name = "constraint" + str(self.index))
        self.index += 1
        self.panel.update_mp3_listing()

    def finish_on_press(self, event):
        MyFrame3(self)

class MyFrame1(wx.Frame):    
    def __init__(self, parent):
        super().__init__(parent, title='Solver')
        self.panel = Mp3Panel(self)
        var_text = wx.StaticText(self.panel, label='Var', pos = (10, 110))
        type_text = wx.StaticText(self.panel, label='Type', pos = (180, 110))
        self.var = wx.TextCtrl(self.panel, pos = (70, 110))
        self.type = wx.TextCtrl(self.panel, pos = (230, 110))
        lower_text = wx.StaticText(self.panel, label='Lower', pos = (10, 143))
        upper_text = wx.StaticText(self.panel, label='Upper', pos = (180, 143))
        self.lower = wx.TextCtrl(self.panel, pos = (70, 143))
        self.upper = wx.TextCtrl(self.panel, pos = (230, 143))
        add_btn = wx.Button(self.panel, label='Add Variable',pos = (70, 175))
        add_btn.Bind(wx.EVT_BUTTON, self.add_on_press)
        finish_btn = wx.Button(self.panel, label='Finish',pos = (215, 175))
        finish_btn.Bind(wx.EVT_BUTTON, self.finish_on_press)
        self.Show()
    def add_on_press(self, event):
        var_con = self.var.GetValue()
        type_con = self.type.GetValue()
        lower_con = self.lower.GetValue()
        upper_con = self.upper.GetValue()
        self.panel.var_list.append(var_con)
        self.panel.type_list.append(type_con)
        self.panel.lower_list.append(lower_con)
        self.panel.upper_list.append(upper_con)
        if type_con == "int":
            locals()[var_con] = solver.new_int_var(int(lower_con), int(upper_con), var_con)
        elif type_con == "float":
            locals()[var_con] = solver.new_var(int(lower_con), int(upper_con), 0, var_con)
        var_list.append(locals()[var_con])
        self.panel.update_mp3_listing()

    def finish_on_press(self, event):
        MyFrame2(self)

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Solver')
        panel = wx.Panel(self)
        '''
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        '''
        my_btn = wx.Button(panel, label='Get Started',pos = (130, 55))
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        self.Show()

    def on_press(self, event):
        MyFrame1(self)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()