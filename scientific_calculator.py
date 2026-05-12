import tkinter as tk
import math

class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Scientific Calculator")
        master.geometry("400x550")
        master.resizable(False, False)
        master.configure(bg="#2c3e50")

        self.equation = ""
        
        # Display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display = tk.Entry(master, textvariable=self.display_var, font=('Arial', 24), bg="#ecf0f1", fg="#2c3e50", bd=10, justify="right")
        display.grid(row=0, column=0, columnspan=5, pady=10, padx=10, ipadx=8, ipady=10)
        display.bind("<Key>", lambda e: "break") # Disable manual typing to prevent errors
        
        # Create Buttons
        self.create_buttons()

    def create_buttons(self):
        button_style = {
            'font': ('Arial', 14),
            'bg': '#34495e',
            'fg': 'white',
            'activebackground': '#2980b9',
            'activeforeground': 'white',
            'bd': 1,
            'relief': 'flat'
        }
        
        operator_style = button_style.copy()
        operator_style['bg'] = '#e67e22'
        
        scientific_style = button_style.copy()
        scientific_style['bg'] = '#16a085'

        buttons = [
            ('sin', 1, 0, scientific_style), ('cos', 1, 1, scientific_style), ('tan', 1, 2, scientific_style), ('AC', 1, 3, operator_style), ('C', 1, 4, operator_style),
            ('sqrt', 2, 0, scientific_style), ('log', 2, 1, scientific_style), ('ln', 2, 2, scientific_style), ('(', 2, 3, scientific_style), (')', 2, 4, scientific_style),
            ('^', 3, 0, scientific_style), ('7', 3, 1, button_style), ('8', 3, 2, button_style), ('9', 3, 3, button_style), ('/', 3, 4, operator_style),
            ('pi', 4, 0, scientific_style), ('4', 4, 1, button_style), ('5', 4, 2, button_style), ('6', 4, 3, button_style), ('*', 4, 4, operator_style),
            ('e', 5, 0, scientific_style), ('1', 5, 1, button_style), ('2', 5, 2, button_style), ('3', 5, 3, button_style), ('-', 5, 4, operator_style),
            ('DEL', 6, 0, operator_style), ('0', 6, 1, button_style), ('.', 6, 2, button_style), ('+', 6, 3, operator_style), ('=', 6, 4, operator_style)
        ]

        for (text, row, col, style) in buttons:
            btn = tk.Button(self.master, text=text, width=5, height=2, **style,
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, padx=5, pady=5)

    def on_button_click(self, char):
        if char == 'AC' or char == 'C':
            self.equation = ""
            self.display_var.set("0")
        elif char == 'DEL':
            # Need to handle backspace properly, especially for multi-char math functions
            self.equation = self.equation[:-1]
            if not self.equation:
                self.display_var.set("0")
            else:
                self.update_display()
        elif char == '=':
            self.evaluate()
        else:
            if char == 'sin':
                self.equation += 'math.sin(math.radians('
            elif char == 'cos':
                self.equation += 'math.cos(math.radians('
            elif char == 'tan':
                self.equation += 'math.tan(math.radians('
            elif char == 'sqrt':
                self.equation += 'math.sqrt('
            elif char == 'log':
                self.equation += 'math.log10('
            elif char == 'ln':
                self.equation += 'math.log('
            elif char == '^':
                self.equation += '**'
            elif char == 'pi':
                self.equation += 'math.pi'
            elif char == 'e':
                self.equation += 'math.e'
            else:
                self.equation += str(char)
            
            self.update_display()

    def update_display(self):
        # Show a cleaner version of the equation to the user
        display_text = self.equation.replace('math.sin(math.radians(', 'sin(') \
                                    .replace('math.cos(math.radians(', 'cos(') \
                                    .replace('math.tan(math.radians(', 'tan(') \
                                    .replace('math.sqrt(', 'sqrt(') \
                                    .replace('math.log10(', 'log(') \
                                    .replace('math.log(', 'ln(') \
                                    .replace('**', '^') \
                                    .replace('math.pi', 'pi') \
                                    .replace('math.e', 'e')
        
        # If display is empty after DEL, show 0
        if not display_text:
            display_text = "0"
            
        self.display_var.set(display_text)

    def evaluate(self):
        if not self.equation:
            return
            
        try:
            # We use a restricted dictionary for eval to prevent security issues
            safe_dict = {
                'math': math,
                '__builtins__': None
            }
            # Balance brackets if any are missing at the end
            open_brackets = self.equation.count('(')
            close_brackets = self.equation.count(')')
            if open_brackets > close_brackets:
                self.equation += ')' * (open_brackets - close_brackets)
            
            result = str(eval(self.equation, safe_dict))
            
            # Formatting to remove unnecessary decimals
            if result.endswith('.0'):
                result = result[:-2]
                
            self.display_var.set(result)
            self.equation = result # Allows chaining operations
        except ZeroDivisionError:
            self.display_var.set("Math Error")
            self.equation = ""
        except Exception:
            self.display_var.set("Syntax Error")
            self.equation = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
