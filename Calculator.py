from tkinter import *
import math  # lib for math functions
from tkinter.scrolledtext import ScrolledText  # import for scrollable text

class CalclModel:  # model
    def __init__(self, root):  # initialization
        self.root = root  # window
        self.total = 0  # sum
        self.current = ''  # current value
        self.op = ''  # operation
        self.num = ""  # number
        # dictionary for storing values in memory. M0 - for one-line field, others for multi-line
        self.memory_store = {"M0": 0, "M1": 0, "M2": 0, "M3": 0, "M4": 0, "M5": 0, "M6": 0, "M7": 0, "M8": 0}

    def reset_memory(self):  # clear memory (clear dictionary)
        self.memory_store = {"M0": 0, "M1": 0, "M2": 0, "M3": 0, "M4": 0, "M5": 0, "M6": 0, "M7": 0, "M8": 0}

    def valid_function(self, num1, num2, op):  # execute operations
        self.current = float(num2)  # current value
        self.total = float(num1)  # sum
        self.op = op  # operation
        if self.op == " + ":  # addition
            self.total += self.current
        elif self.op == " - ":  # subtraction
            self.total -= self.current
        elif self.op == " * ":  # multiplication
            self.total *= self.current
        elif self.op == " / ":  # division
            if self.current == 0:  # division by zero
                self.total = 0  # sum equals zero
                self.current = "ERROR"  # division error
                return self.current  # return error
            else:  # otherwise
                self.total /= self.current  # division
        elif self.op == " ** ":  # power
            self.total **= self.current
        elif self.op == "log_xy":  # logarithm of the number to the base
            try:  # try to perform operation
                self.current = math.log(float(self.total), int(self.current))
                self.total = self.current
            except (ArithmeticError, ValueError):  # catch error
                self.current = "ERROR"  # return error
                self.total = 0  # sum equals zero
            return f'{self.current}'  # return result
        return self.total  # return sum

    def find_memo(self, memo_op, key, value=0):  # function for working with memory
        self.current = float(value)  # current value
        if memo_op == "MS":  # record in memory
            self.memory_store[key] = self.current  # record in memory the current value
            self.total = self.current  # sum equals current value
            return
        elif memo_op == "MR":  # read from memory
            self.current = self.memory_store[key]  # current value equals value from memory
            return self.current  # return current value
        elif memo_op == "M+":  # addition in memory
            self.memory_store[key] += value  # addition of the current value and the number in memory
            return
        elif memo_op == "M-":  # subtraction from memory
            self.memory_store[key] -= value  # subtraction of the current value from the number in memory
            return
        elif memo_op == "MC":  # clear memory
            self.memory_store[key] = 0  # clear memory
            return

    def function(self, num, fun):
        try:
            if fun == "asin":
                self.current = math.asin(float(num))
            elif fun == "acos":
                self.current = math.acos(float(num))
            elif fun == "atg":
                self.current = math.atan(float(num))
            elif fun == "sqrt":
                self.current = math.sqrt(float(num))
            elif fun == "mathPM":
                self.current = -(float(num))
            else:
                raise ValueError("Invalid function: {}".format(fun))
        except (ArithmeticError, ValueError, OverflowError) as e:
            self.current = "ERROR"
        return self.current

    def fact(self, num):  # factorial
        if int(float(num)) >= 0:  # if number is positive or zero
            self.current = float(num)
            self.current = math.factorial(int(self.current))
        elif int(float(num)) < 0:  # if number is negative
            self.current = "ERROR"  # return error
        return self.current


class CalcView:  # View
    def __init__(self, model, root):
        self.model = model
        self.root = root

    def create_labels(self):  # create labels
        fnt, g, w, bl = ('Arial', 30, 'bold'), 'grey','white', 'blue'
        lblDisplay = Label(self.root, text="Scientific Calculator", font=fnt, background=g, foreground=w,justify=CENTER)  # метка
        lblDisplay.grid(row=0, column=4, columnspan=5)  # location of the label
        labels_list = "12345678"  # list of labels on the right side of the screen for memory cells
        s = 0
        labs = []
        for j in range(2, 10):  # row
            for k in range(9, 10):  # column
                labs.append(Label(self.root, width=1, background=w, foreground=bl, font=fnt, text=labels_list[s]))
                labs[s].grid(row=j, column=k)  # location of the labels
                s += 1  # counter is increased by 1


class CalcController:  # Controller
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.input = True  # flag for input
        self.cur_field = 0  # current field
        self.sum_check = False  # flag for sum
        self.here = False  # flag of sign
        self.op = ''  # operation
        self.num = 0  # number
        self.cur_val = ""  # current value
        self.total = 0  # total
        self.result = False  # flag of result
        self.flag_memo = False  # flag of memory

    def load(self):  # load program
        self.view.create_labels()
        self.create_buttons_and_inputs()  # create buttons and inputs

    def on_focus(self, event="entry"):  # focus on the input field
        if event == "entry":  # if the input field is one line
            self.cur_field = 0  # flag zero
        else:  # if the input field is multy lines
            self.cur_field = 1  # flag one

    def check_error(self):  # check error
        if self.cur_val != "ERROR" and (self.cur_val != "" or self.cur_val != "0"
                                            or self.cur_val != 0.0):  # if current value is not error
            self.total = self.cur_val
        elif self.cur_val == "ERROR":  # if current value is error
            self.total = 0  # sum equals zero
            self.op = ""  # operation is empty
        self.sum_check = False  # sum flag is false

    def operation(self, entry, multi, op):  # Perform the specified operation based on the current state of the calcul
        if self.op != op and self.op != "":  # Check if the operation is different from the current and not empty
            if self.cur_field == 1:  # If the current field is multi-line
                if multi.get("1.0", END).endswith(f" \n"):  # Check if the last symbol is a space
                    self.op = ""  # Reset the operation
                    multi.delete("end-4c", "end-1c")  # Delete last symbols
                else:
                    return
            elif self.cur_field == 0:  # If single-line
                self.op = ""  # Reset the operator
                self.sum_check = False  # Reset the sum flag
                self.result = True  # Set the result flag
            self.input = True  # Set the input flag
        if self.cur_field == 1:  # If multi-line
            if self.total == 0:  # If total is zero
                self.total = float(self.cur_val)  # Update total with current value
                self.input = True  # Set the input flag
            self.sum_check = True  # Set the sum flag
            self.op = op  # Set the operation sign
            self.result = False  # Reset the result flag
            if self.op != "" and not self.here:  # If the operation sign is not empty
                self.print_multi(entry, multi)  # Display in the multi-line field
        elif self.cur_field == 0 and entry.get() != "0":  # If single-line and entry is not "0"
            if self.cur_val == "":  # If current value is empty
                self.cur_val = "0"  # Set it to zero
            self.cur_val = float(self.cur_val)  # Convert to floating point number
            if self.sum_check:  # If sum flag is on
                result = self.model.valid_function(self.total, self.cur_val, self.op)  # Calculate the operation
                if result == 0.0:  # If the result is zero
                    result = 0  # Set it to zero
                self.display(entry, multi, result)  # Display in the single-line field
                self.sum_check = False  # Reset the sum flag
            elif not self.result:  # If result flag is not set
                if not self.flag_memo:  # If memory flag is not set
                    self.total = self.cur_val  # Update total with current value
                self.input = True  # Set the input flag
            self.sum_check = True  # Set the sum flag
            self.op = op  # Set the operation sign
            self.result = False  # опускаем флаг результата

    def enter_num(self, entry, multi, num):  # Method to handle entering a number
        self.result = False  # Reset the result flag
        if self.cur_field == 0:  # If it's a single-line field
            first = entry.get()  # Get the current value from the entry widget
            if first == "ERROR":
                entry.delete(0, END)
                first = ""
            second = str(num)
            if self.input:
                self.cur_val = second
                self.input = False
            else:
                if second == '.':
                    if second in first:
                        return
                elif first == "0" and second != ".":
                    first = ""
                self.cur_val = first + second
            self.display(entry, multi, self.cur_val)
        else:
            if self.op != "":
                self.here = True
            first = multi.get("1.0", END)
            if len(first) == 2 and first[0] == "0" and first[1] != ".":
                self.reduce(entry, multi)
            elif multi.get("1.0", END).endswith(" 0\n"):
                multi.delete("end-2c")
            self.num = str(num)
            if self.num == "." and (self.cur_val == "" or self.cur_val == "0"):
                self.num = "0."
                self.cur_val = self.num
            elif self.cur_val == "0." and self.num == ".":
                return
            elif self.num == "." and "." in self.cur_val:
                self.num = ""
                return
            elif self.cur_val == "0." and self.num.isnumeric():
                self.cur_val += self.num
            else:
                if self.input:
                    self.cur_val = self.num
                    self.input = False
                else:
                    self.cur_val += self.num
            self.display(entry, multi, self.num)

    def Clear_Entry(self, entry, multi):  # This function clears the input fields based on the type of field
        if self.cur_field == 0:  # Single-line field
            self.result = False
            self.cur_val = "0"
            self.total = 0
            self.op = ""
            self.display(entry, multi, 0)
        else:  # Multi-line field
            self.display(entry, multi, "\nC\n  ")
            self.cur_val = "0"
            self.total = 0
            self.op = ""
        self.input = True

    def reduce(self, entry, multi):  # Reduce the multi-line field. Resets values and flags.
        self.result = False  # Result flag lowered
        self.total = 0
        self.cur_val = ""
        self.flag_memo = False  # Memory flag lowered (not working with memory)
        self.op = ""  # No operator
        multi.delete("1.0", END)  # Clear the multi-line field
        self.input = True  # Input flag raised
        self.here = False  # Here flag lowered

    def all_clean(self, entry, multi):  # Clear the entire content from the multi-line field.
        self.result = False  # Reset result flag
        self.total = 0  # Reset total
        self.cur_val = ""  # Reset current value
        self.flag_memo = False  # Reset memory flag
        self.here = False  # Reset here flag
        self.op = ""  # Reset operation
        self.model.reset_memory()  # Reset memory in the model
        self.input = True  # Set input flag to True
        multi.delete("1.0", END)  # Clear the multi-line field
        multi.insert("1.0", "0", "justified")  # Insert '0' justified at the beginning

    def check_s_to_total(self, s):  # Check the value of 's' and update the current value and total accordingly.
        if s == 0.0 or s == "0.0":  # If 's' is equal to 0.0 or "0.0", update the current value to an empty string.
            self.cur_val = ""
        elif s == "ERROR": # If 's' is equal to ERROR, set the current value to 's', total to 0, and here flag to False.
            self.cur_val = s
            self.total = 0
            self.here = False
        else:  # Otherwise, update the total with the value of 's'.
            self.total = s

    def sum_of_total(self, entry, multi): # function for sum of total
        self.result = True
        if self.cur_field == 1:  # if the input field is multy lines
            try:  # try to convert the current value to a number
                self.cur_val = float(self.cur_val)
            except ValueError:  # if the current value is not a number
                self.cur_val = ""  # then set the current value to an empty string
        if self.sum_check:  # if the sum flag is raised
            s = self.model.valid_function(self.total, self.cur_val, self.op)  # execute the valid function
            if s == 0.0:  # if the result is 0.0
                s = 0
            self.sum_check = False  # flag is lowered
            if self.cur_field == 0:  # if the input field is one line
                self.display(entry, multi, s)  # display the result in  one-line field
                self.total = float(entry.get())  # set the total to the current value
                self.cur_val = ""
            else:  # if the input field is multy lines
                if self.op == "log_xy":  # if the operation is log_xy
                    self.display(entry, multi, f')')  # then display the ')'
                self.check_s_to_total(s)  # check the value of 's'
                self.display(entry, multi, f'\n=\n{s}')  # print the result in the multi-line field
                self.op = ""  # operation is set to an empty string
                self.cur_val = ""  # current value is set to an empty string
                self.here = False  # flag is lowered
                self.input = True  # flag is raised for input

    def func_cont(self, entry, multi, func):
        # This function calculates the result based on the provided function and current value.
        self.result = False  # Reset the result flag
        if self.total == 0 or self.total == "0":  # If the total is zero
            if func != "sqrt" and func != "mathPM":  # If the function is not sqrt or mathPM
                self.display(entry, multi,
                             f"\n{func}({float(self.cur_val)})\n=\n")  # Display the function and calculation
            elif func == "mathPM":  # If the function is mathPM
                self.display(entry, multi, f"x(-1)\n=\n")  # Display special mathPM calculation
            self.cur_val = self.model.function(float(self.cur_val), func)  # Update the current value
        else:  # If the total is not zero
            if func != "sqrt" and func != "mathPM":  # If the function is not sqrt or mathPM
                self.display(entry, multi,
                             f"\n{func}({float(self.total)})\n=\n")  # Display the function and calculation
            elif func == "mathPM":  # If the function is mathPM
                self.display(entry, multi, f"x(-1)\n=\n")  # Display special mathPM calculation
            self.cur_val = self.model.function(float(self.total), func)  # Update the current value
        self.check_error()  # Check for errors
        if func != "sqrt":  # If the function is not sqrt
            self.display(entry, multi, self.cur_val)  # Display the current value in the multi-line field
        else:
            self.display(entry, multi, f'**(-1/2)\n=\n{self.cur_val}')  # Display special calculation for sqrt
        self.cur_val = ""  # Reset the current value

    def fact_cont(self, entry, multi):
        """Calculate the factorial of the current value and display it in the multi-line field."""
        self.result = False  # Reset the result flag
        self.display(entry, multi, f"!\n=\n")  # Display '!' and '=' with line breaks in the multi-line field
        if (self.total == "0" or self.total == 0) and int(float(self.cur_val)) >= 0:
            # If the total is 0 and the current value is greater than or equal to 0
            self.cur_val = self.model.fact(int(float(self.cur_val)))  # Calculate factorial of the current value
        elif int(float(self.total)) < 0 or (self.total == 0 and int(float(self.cur_val)) < 0):
            # If the total is less than 0 or total is 0 and current value is less than 0
            self.cur_val = "ERROR"  # Set the current value to "ERROR"
        else:
            self.cur_val = self.model.fact(int(float(self.total)))  # Calculate factorial of the total
        self.check_error()  # Check for errors
        self.display(entry, multi, self.cur_val)  # Display the calculated value in the multi-line field
        self.cur_val = ""  # Reset the current value

    def squared_cont(self, entry, multi, func):
        # This function calculates the square root of a number and displays the result.
        self.result = False  # Reset the result flag
        if self.cur_field == 0:  # If it's a single-line field
            self.cur_val = self.model.function(float(entry.get()), func)  # Calculate the square root
            self.check_error()  # Check for errors
            self.display(entry, multi, f'{self.cur_val}')  # Display in single-line field
            if self.cur_val == "ERROR":  # If there is an error
                self.cur_val = ""  # Reset the current value
        else:  # If it's a multi-line field
            self.func_cont(entry, multi, func)  # Call the func_cont function

    def mathPM_cont(self, entry, multi):  # This function changes the sign of the current value (absolute value).
        self.result = False  # Reset the result flag
        if self.cur_field == 0:  # If it's a single-line field
            self.check_error()  # Check for errors
            self.display(entry, multi, f'{self.cur_val}')  # Display in single-line field
            if self.cur_val == "0.0" or self.cur_val == 0.0 or self.cur_val == "ERROR":  # If there is an error
                return
            else:
                self.cur_val = -float(self.cur_val)  # Change the sign and convert to float
                self.display(entry, multi, f'{self.cur_val}')  # Display the updated value
        else:
            self.func_cont(entry, multi, "mathPM")  # Call the func_cont function

    def find_m(self, entry, multi, memo_op_cont, key_cont):  # search in memory
        self.result = False  # flag of result is false
        if self.cur_val == "":  # if current value is empty
            self.cur_val = "0"  # then set current value is 0
        self.cur_val = float(self.cur_val)  # then convert current value to float
        if memo_op_cont == "MS":  # if operation MS - save in memory
            self.flag_memo = True  # flag of memory is true
            if self.total == 0:    # if sum is 0
                # then save current value in memory
                self.model.find_memo(memo_op_cont, key_cont, self.cur_val)
                self.total = self.cur_val  # then set sum to current value
            else:
                self.model.find_memo(memo_op_cont, key_cont, self.total)  # then save sum in memory
            return  # exit function
        elif memo_op_cont == "MR":  # if operation MR - read from memory
            self.flag_memo = True  # flag of memory is true
            self.cur_val = self.model.find_memo(memo_op_cont, key_cont)  # then return value from memory
            if self.cur_field == 0:  # if it's a single-line field -  entry
                self.display(entry, multi, self.cur_val)
                if self.op == "":  # if there is no operation
                    self.total = self.cur_val  # then set sum to current value
                elif self.op != "":
                    self.flag_memo = False  # flag of memory is false
            else:  # if it's a multi-line field - multi
                # if the last symbol is "C\n  \n" or "ERROR\n\n" in the multi-line field
                if multi.get("1.0", END).endswith("C\n  \n") or multi.get("1.0", END).endswith("ERROR\n\n"):
                    self.display(entry, multi, self.cur_val)  # then display current value
                    self.total = self.cur_val  # then set sum to current value
                elif multi.get("1.0", END).endswith(" \n"):  # if the last symbol is a space
                    self.display(entry, multi, f'({self.cur_val})')
                elif self.op == "":  # if there is no operation
                    self.total = 0  # then set sum to 0
                    self.display(entry, multi, f'\n{self.cur_val}')  # then display current value
            return
        elif memo_op_cont == "M+" or memo_op_cont == "M-":  # if operation M+ or M-
            self.flag_memo = True  # flag of memory is true
            if self.total == 0:  # if sum is 0
                self.model.find_memo(memo_op_cont, key_cont, self.cur_val)  # then add or subtract current value
                self.total = self.cur_val  # then set sum to current value
                self.cur_val = ""
            else:
                self.model.find_memo(memo_op_cont, key_cont, self.total)  # then add or subtract sum in memory
                return
        elif memo_op_cont == "MC":  # if operation MC - clear memory
            self.flag_memo = True  # flag of memory is true
            self.model.find_memo(memo_op_cont, key_cont, 0)  # then clear memory
            return

    def print_multi(self, entry, multi):  # print in multi-line field
        if self.op != "log_xy" and not self.here:
            self.display(entry, multi, self.op)
        elif self.op == "log_xy":  # if operation is log_xy
            if self.total == 0:  # if sum is 0
                self.total = float(self.cur_val)  # then sum equals current value
            self.display(entry, multi, f"\nlog({self.total}, base = ")  # print in multi-line field

    def check_on_error(self, entry, multi, value):  # Check for errors and handle accordingly.
        if multi.get("1.0", END).endswith("ERROR\n") or value == "ERROR":
            self.display(entry, multi, "\n")  # Insert a newline
            self.cur_val = ""  # Reset current value
            self.total = 0  # Reset the total
            self.op = ""  # Reset the operation
        elif multi.get("1.0", END).endswith("=\n0.0\n"):  # If the multi-line field ends with "= 0.0"
            self.display(entry, multi, "\n")  # Insert a newline
            self.cur_val = ""  # Reset current value
            self.total = 0  # Reset the total
            self.op = ""  # Reset the operation
        else:
            return

    def display(self, entry, multi, value):  # display value
        if self.cur_field == 0:  # if entry
            entry.delete(0, END)  # clear entry
            entry.insert(0, value)  # insert value
        else:  # if multi-line
            if multi.get("1.0", END).endswith("\n=\n\n") and self.total != 0:
                multi.insert(END, f"{self.total}", "justified")
                self.here = False
                self.check_on_error(entry, multi, self.total)
            elif multi.get("1.0", END).endswith("\n=\n\n") and self.total == 0:
                multi.insert(END, f"{self.cur_val}", "justified")
                self.here = False  # flag sign lowered
                self.check_on_error(entry, multi, self.cur_val)  # check on error
            else:
                multi.insert(END, value, "justified")  # insert value
                self.check_on_error(entry, multi, value)  # check on error

    def create_buttons_and_inputs(self):  # create buttons and inputs
        fnt, B, w, CB, r, g, o, bl = ('Arial', 20, 'bold'), 'black', 'white', 'CadetBlue1', 'red', 'grey', 'olive', 'blue'
        entry = Entry(self.view.root, font=fnt, background=B, foreground=w, bd=10, width=28, justify=RIGHT)  # entry
        entry.bind("Focus_in", self.on_focus("entry"))  # focus on entry
        entry.grid(row=1, column=0, columnspan=4, pady=1)  # location of the entry
        entry.insert(0, "0")  # insert "0"
        multi = ScrolledText(self.view.root, font=fnt, bg=B, fg=w, width=28, height=7)  # multiline
        multi.tag_config('justified', justify="right")  # justify right
        numbers = "789456123"
        i = 0  # counter
        btn = []  # list of buttons
        for j in range(6, 9):  # row
            for k in range(3):  # column
                btn.append(Button(self.view.root, width=6, height=1, bg=CB, fg=bl, font=fnt, bd=4, text=numbers[i]))
                btn[i].grid(row=j, column=k, pady=1)  # рlocation of buttons
                btn[i]["command"] = lambda x=entry, y=multi, z=numbers[i]: self.enter_num(x, y, z)
                i += 1  # counter increment
        btnC = Button(self.view.root, text=chr(67), width=6, height=1, bg=r, fg=w, font=fnt, bd=4,
                          command=lambda: self.Clear_Entry(entry, multi))
        btnClear = Button(self.view.root, text=chr(67), width=6, height=1, bg=r, fg=w, font=fnt, bd=4,
                          command=lambda: self.Clear_Entry(entry, multi))
        btnAllClear = Button(self.view.root, text=chr(65) + chr(67), width=6, height=1, bg=r, fg=w, font=fnt, bd=4,
                             command=lambda: self.all_clean(entry, multi))
        btnPow = Button(self.view.root, text="xⁿ", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                        command=lambda: self.operation(entry, multi, " ** ")).grid(row=5, column=1, pady=1)
        btnsq = Button(self.view.root, text="\u221A", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                       command=lambda: self.squared_cont(entry, multi, "sqrt")).grid(row=5, column=2, pady=1)
        oper = ["+", "-", "x", "/"]  # list of operators
        val = [' + ', ' - ', ' * ', ' / ']  # list of values for operators for display in multi line field
        bt_op = []  # list of buttons
        m = 0  # counter
        for j in range(5, 9):  # row
            for k in range(3, 4):  # column
                bt_op.append(Button(self.view.root, width=6, height=1, bg=g, fg=w, font=fnt, bd=4, text=oper[m]))
                bt_op[m].grid(row=j, column=k, pady=1)
                bt_op[m]["command"] = lambda x=entry, y=multi, z=val[m]: self.operation(x, y, z)
                m += 1
        btnZero = Button(self.view.root, text="0", width=13, height=1, bg=CB, fg=bl, font=fnt, bd=4,
                         command=lambda: self.enter_num(entry, multi, 0)).grid(row=9, column=0, pady=1, columnspan=2)
        btnDot = Button(self.view.root, text=".", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                        command=lambda: self.enter_num(entry, multi,".")).grid(row=9, column=2, pady=1)
        btnPM = Button(self.view.root, text=chr(177), width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                       command=lambda: self.mathPM_cont(entry, multi)).grid(row=5, column=0, pady=1)
        btnEquals = Button(self.view.root, text="=", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                           command=lambda:self.sum_of_total(entry, multi)).grid(row=9, column=3, pady=1)
        # ROW 1 :
        btnasin = Button(self.view.root, text="asin", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                         command=lambda: self.func_cont(entry, multi, "asin")).grid(row=1, column=4, pady=1)
        btnacos = Button(self.view.root, text="acos", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                         command=lambda: self.func_cont(entry, multi,"acos")).grid(row=1, column=5, pady=1)
        btnatg = Button(self.view.root, text="atg", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                        command=lambda: self.func_cont(entry, multi, "atg")).grid(row=1, column=6, pady=1)
        btnlog_xy = Button(self.view.root, text="log_xy", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                           command=lambda: self.operation(entry, multi, "log_xy")).grid(row=1, column=7, pady=1)
        btnfactorial = Button(self.view.root, text="n!", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                              command=lambda:self.fact_cont(entry, multi)).grid(row=1, column=8, pady=1)

        def memory(btn_row, x, ro):  # This function creates memory buttons with specific commands.
            memcom = ["MC", "MR", "MS", "M+", "M-"]  # List of memory commands
            m = 0  # Counter
            for j in range(x, x + 1):  # Row
                for k in range(4, 9):  # Column
                    btn_row.append(Button(self.view.root, width=6, height=1, bg=g, fg=w, font=fnt, bd=4, text=memcom[m]))
                    btn_row[m].grid(row=j, column=k, pady=1)
                    btn_row[m]["command"] = lambda a=entry, b=multi, c=memcom[m], d=ro: self.find_m(a, b, c, d)
                    if m == 4:  # If counter is 4
                        break  # Exit loop
                    else:
                        m += 1

        # ROW 2, 3, 4, 5, 6, 7, 8, 9 :
        btn_r2, btn_r3, btn_r4, btn_r5, btn_r6, btn_r7, btn_r8, btn_r9 = [], [], [], [], [], [], [], []
        btn_rows = [btn_r2, btn_r3, btn_r4, btn_r5, btn_r6, btn_r7, btn_r8, btn_r9]
        memory_row = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]
        for v in range(8):
            memory(btn_rows[v], v + 2, memory_row[v])

        def Standard():  # standard mode
            def Sc():  # Switches to the engineer calculator mode.
                # Hide elements related to the standard calculator mode
                self.view.root.resizable(width=False, height=False)
                self.view.root.geometry("1070x610+0+0")
                lblCalc.grid_forget()
                entry.grid_forget()
                btnToSc.grid_forget()
                btnMemSave.grid_forget()
                btnMemClear.grid_forget()
                btnMemReturn.grid_forget()
                btnMemPlus.grid_forget()
                btnMemMinus.grid_forget()
                # Display elements related to the engineer calculator mode
                multi.grid(row=0, column=0, columnspan=4, rowspan=4, sticky=NE)
                multi.bind('Return', self.on_focus("multiline"))
                multi.delete("1.0", END)
                multi.insert("1.0", "0", 'justified')
                btnAllClear.grid(row=4, column=3, pady=1)
                self.all_clean(entry, multi)
                btnC.grid(row=4, column=2, pady=1)
                btnClear.grid_forget()

                def back():  #Returns to the standard calculator mode.
                    btnToStd.grid_forget()
                    multi.grid_forget()
                    btnAllClear.grid_forget()
                    btnC.grid_forget()
                    entry.grid(row=1, column=0, columnspan=4, pady=1)
                    entry.bind("Return", self.on_focus("entry"))
                    entry.delete(0, END)
                    entry.insert(0, "0")
                    Standard()
                    # Button to switch back to the standard calculator mode
                btnToStd = Button(self.view.root, text="≡", width=13, height=1, bg=o, fg=w, font=fnt, bd=4,
                                  command=back)
                btnToStd.grid(row=4, column=0, pady=1, columnspan=2)

            self.view.root.resizable(width=False, height=False)  # not resizable
            self.view.root.geometry("464x610+0+0")  # size of window
            btnToSc = Button(self.view.root, text="≡", width=13, height=1, bg=o, fg=w, font=fnt, bd=4, command=Sc)
            btnToSc.grid(row=3, column=0, pady=1, columnspan=2)
            lblCalc = Label(self.view.root, text="Standard Calculator", font=('Arial', 30, 'bold'), bg=g, fg=w,
                            justify=CENTER)
            lblCalc.grid(row=0, column=0, columnspan=4)
            btnMemSave = Button(self.view.root, text="MS", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                                command=lambda: self.find_m(entry, multi, "MS", "M0"))
            btnMemSave.grid(row=4, column=0, pady=1)
            btnMemClear = Button(self.view.root, text="MC", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                                 command=lambda: self.find_m(entry, multi, "MC", "M0"))
            btnMemClear.grid(row=3, column=3, pady=1)
            btnMemReturn = Button(self.view.root, text="MR", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                                  command=lambda: self.find_m(entry, multi, "MR", "M0"))
            btnMemReturn.grid(row=4, column=1, pady=1)
            btnMemPlus = Button(self.view.root, text="M+", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                                command=lambda: self.find_m(entry, multi, "M+", "M0"))
            btnMemPlus.grid(row=4, column=2, pady=1)
            btnMemMinus = Button(self.view.root, text="M-", width=6, height=1, bg=g, fg=w, font=fnt, bd=4,
                                 command=lambda: self.find_m(entry, multi, "M-", "M0"))
            btnMemMinus.grid(row=4, column=3, pady=1)
            btnClear.grid(row=3, column=2, pady=1)
            self.Clear_Entry(entry, multi)  # clear entry
        Standard()

def main():  # main function
    root = Tk()  # create main window
    root.title("Standard and Scientific calculator")  # name of window
    root.resizable(width=False, height=False)  # not resizable
    root.geometry("464x610+606+0")  # size of window
    root.grid()  # location of window
    model = CalclModel(root)  # create model
    view = CalcView(model, root)  # create view
    controller = CalcController(model, view)  # create controller
    controller.load()  # load program
    root.mainloop()  # load program


if __name__ == "__main__":  # main function
    main()