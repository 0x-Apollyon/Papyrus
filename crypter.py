import os
import ast
import keyword
import random
import string
import math
import builtins


cwd = os.getcwd()


global variables_reference
variables_reference = {}
variables_reference["modules"] = {}
variables_reference["variables"] = {}
variables_reference["functions"] = {}
variables_reference["objects"] = {}



def variable_noise(count=1):
    returnable_arr = []

    if count != 1:
        while len(returnable_arr) != count:
            var_name = "_0x"
            hex_chars = "1234567890abcdef"
            var_name_size = random.randint(1 , 5)*4
            for x in range(var_name_size):
                var_name = var_name + random.choice(list(hex_chars))
            if var_name not in returnable_arr:
                returnable_arr.append(var_name)
        return returnable_arr
    else:
        var_name = "_0x"
        hex_chars = "1234567890abcdef"
        var_name_size = random.randint(1 , 4)*4
        for x in range(var_name_size):
            var_name = var_name + random.choice(list(hex_chars))

        return var_name

variables_reference["modules"]["math"] = variable_noise()
variables_reference["variables"]["__builtins__"] = variable_noise()
variables_reference["functions"]["ord"] = variable_noise()
variables_reference["functions"]["int"] = variable_noise()
variables_reference["functions"]["round"] = variable_noise()
variables_reference["functions"]["chr"] = variable_noise()
variables_reference["functions"]["globals"] = variable_noise()


def basic_integer_noise(orginal_number):
    basic_operators = ["+" , "-" , "*"]
    random.shuffle(basic_operators)
    expr_val = hex(random.randint(500000 , 1000000))
    expr = f"{expr_val}"
    for operator in basic_operators:
        if random.random() > 0.8:
            noise = random.randint(500000 , 1000000)
            expr = f"({expr} {operator} {hex(noise)})"
            expr_val = eval(expr)
    
    fix_dif = orginal_number - eval(expr)
    if random.random() > 0.5:
        expr = f"{expr} + {hex(fix_dif)}"
    else:
        expr = f"{expr} - {hex((-1)*fix_dif)}"
    return expr

def long_string_obf(strng):
    random_noise_start = random.randint(5 , 50)
    random_noise_end = random.randint(5 , 50)
    random_noise_gap = random.randint(0 , 3)

    strng_new = ""
    for char in strng:
        strng_new = strng_new + char
        for x in range(random_noise_gap):
            strng_new = strng_new + random.choice(list(string.ascii_letters))

    for i in range(random_noise_start):
        strng_new = random.choice(list(string.ascii_letters)) + strng_new

    for i in range(random_noise_end):
        strng_new = strng_new + random.choice(list(string.ascii_letters))    

    xor_key = os.urandom(len(strng_new))

    xored_strng = bytes(a ^ b for a, b in zip(strng_new.encode(), xor_key))
    
    var_names = variable_noise(2)
    var_1 , var_2 = var_names[0] , var_names[1]

    random_noise_start_2 = random.randint(2 , 10)
    random_noise_end_2 = random.randint(2 , 10)
    random_noise_gap_2 = random.randint(0 , 2)

    dcode_new = ""
    for char in "decode":
        dcode_new = dcode_new + char
        for x in range(random_noise_gap_2):
            dcode_new = dcode_new + random.choice(list(string.ascii_letters))

    for i in range(random_noise_start_2):
        dcode_new = random.choice(list(string.ascii_letters)) + dcode_new

    for i in range(random_noise_end_2):
        dcode_new = dcode_new + random.choice(list(string.ascii_letters))  

    byte_dcode = dcode_new.encode()
    hex_dcode = ''.join([f'\\x{byte:02x}' for byte in byte_dcode])

    hex_dcode = f"'{hex_dcode}'[{basic_integer_noise(random_noise_start_2)}:{basic_integer_noise((-1)*random_noise_end_2)}:{basic_integer_noise(random_noise_gap_2+1)}]"

    return f'getattr(bytes({var_1} ^ {var_2} for {var_1}, {var_2} in zip({xored_strng}, {xor_key})) , {hex_dcode})()[{basic_integer_noise(random_noise_start)}:{basic_integer_noise((-1)*random_noise_end)}:{basic_integer_noise(random_noise_gap+1)}]'

def hexify(expr):
    if random.random() < 0.5:
        return f"int('{hex(expr)}' , {basic_integer_noise(16)})"
    else:
        return expr

def bool_to_int(bool_value):
    rand_1 = random.randint(1000000 , 10000000)
    rand_2 = random.randint(1000000 , 10000000)

    if bool_value:
        if rand_1 > rand_2:
            expr = f"{basic_integer_noise(rand_1)} > {basic_integer_noise(rand_2)}"
        elif rand_1 < rand_2:
            expr = f"{basic_integer_noise(rand_1)} < {basic_integer_noise(rand_2)}"
        else:
            expr = f"{basic_integer_noise(rand_1)} == {basic_integer_noise(rand_2)}"
    else:
        if rand_1 > rand_2:
            expr = f"{basic_integer_noise(rand_1)} < {basic_integer_noise(rand_2)}"
        elif rand_1 < rand_2:
            expr = f"{basic_integer_noise(rand_1)} > {basic_integer_noise(rand_2)}"
        else:
            if random.random() > 0.5:
                expr = f"{basic_integer_noise(rand_1)} > {basic_integer_noise(rand_2 +  random.randint(100 , 1000))}"
            else:
                expr = f"{basic_integer_noise(rand_1 + random.randint(100 , 1000)) } > {basic_integer_noise(rand_2) }"

    return expr

def boolean_obf(bool_value):
    if random.random() > 0.5:
        expr = f"{bool_to_int(True)}"
    else:
        expr = f"{bool_to_int(False)}"

    operations = ["and" , "or" , "^"]
    random.shuffle(operations)
    for op in operations:
        if random.random() > 0.5:
            new_bool = True
        else:
            new_bool = False
        expr = f"(({expr}) {op} ({bool_to_int(new_bool)}))"

    if eval(expr) == bool_value:
        return expr
    else:
        return f"not {expr}"

def integer_noise(original_number , no_math = False):
    global variables_reference
    string_form = str(original_number)
    if "." in string_form:
        number_of_decimal_places = len(string_form.split(".")[1])
    else:
        number_of_decimal_places = 0
    basic_operators = ["+" , "-" , "*"]
    advance_operators = ["** {}" , "math.log2({})" , f"math.log({{}} , {basic_integer_noise(3)})" , f"math.log({{}} , {basic_integer_noise(5)})"]
    random.shuffle(basic_operators)
    
    current_value_of_returnable = random.randint(1000 , 100000)
    returnable_expression = f"{hexify(current_value_of_returnable)}"

    for operator in basic_operators:
        noise = random.randint(100 , 100000)
        #advance transform the noise

        if random.random() > 0.4:
            if not no_math:
                noise_value = random.randint(5 , 10)
                noise_expression = f"{noise_value}"
                random.shuffle(advance_operators)
                for op in advance_operators:
                    if "log" in op:
                        noise_adv = random.randint(10 , 1000)
                        noise_expression = f"({noise_expression} {random.choice(basic_operators)} {op.format(noise_adv)})"
                        noise_value = eval(noise_expression)
                    else:
                        noise_adv = random.randint(2 , 6)
                        noise_expression = f"({noise_expression} {op.format(noise_adv)})"
                        noise_value = eval(noise_expression)

                noise_fix = noise - noise_value
                noise_expression = f"({noise_expression} + {noise_fix})"
            else:
                noise_expression = hexify(noise) 
        else:
            noise_expression = hexify(noise)  

        returnable_expression = f"({returnable_expression} {operator} {noise_expression})"
        try:
            current_value_of_returnable = eval(returnable_expression)
        except:
            print("an error occured")
            print(returnable_expression)
            quit()

        

    fix = original_number - current_value_of_returnable
    #represent fix as ax + c
    if fix < 0:
        fix_t = fix*(-1)
    else:
        fix_t = fix
    noise_for_fix = random.randint(1 , 100000)
    noise_for_fix_actual = hexify(noise_for_fix)
    x_val = random.randint(1 , 10)
    c_val = fix - noise_for_fix*x_val
    fix_expression = f"({x_val}*{noise_for_fix_actual}) + {hexify(int(c_val))} + {c_val - int(c_val)}"
    returnable_expression = f"({returnable_expression} + {fix_expression})"
    
    #binary obfuscation for the number of decimal places
    binary_ops = ["^" , "|" , ">>" , "<<" , "&"]
    random.shuffle(binary_ops)
    decimal_places_value = random.randint(2 , 256)
    decimal_places_expression = f"{bin(decimal_places_value)}"
    for operation in binary_ops:
        if random.random() > 0.2:
            noise = random.randint(2 , 64)
            decimal_places_expression = f"({decimal_places_expression} {operation} {bin(noise)})"
            decimal_places_value = eval(decimal_places_expression)
    decimal_places_fix = decimal_places_value - number_of_decimal_places
    decimal_places_expression = f"({decimal_places_expression} - {bin(decimal_places_fix)})"

    return f"int(round({returnable_expression} , {decimal_places_expression}))".replace("math" , variables_reference['modules']['math']).replace("int" , variables_reference["functions"]["int"]).replace("round" , variables_reference["functions"]["round"])



def string_obfuscation(strng):
    if len(strng) > 70:
        return long_string_obf(strng)
    #caesar cipher
    caesar_string = ""
    shift = random.randint(3 , 9)
    for char in strng:
        if char.isupper():
            caesar_string = caesar_string + chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():
            caesar_string = caesar_string + chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            caesar_string = caesar_string + char
    
    #breaking into array of numbers with noise
    trash_in_start = random.randint(1 , 5)
    trash_in_mid = random.randint(0 , 2)
    if random.random() > 0.5:
        reversed_state = True 
    else:
        reversed_state = False

    charr_expression = f"["

    for x in range(trash_in_start):
        noise_char = random.choice(list(string.ascii_letters))
        charr_expression = f"{charr_expression} chr(int({integer_noise(ord(noise_char))})) ,"

    
    for char in caesar_string:
        charr_expression = f"{charr_expression} chr(int({integer_noise(ord(char))})) ,"
        for x in range(trash_in_mid):
            noise_char = random.choice(list(string.ascii_letters))
            charr_expression = f"{charr_expression} chr(int({integer_noise(ord(noise_char))})) ,"
    else:
        charr_expression = f"{charr_expression[:-1:]}]"

    hex_chars = "1234567890abcdef"
    variable_name = variable_noise()

    charr_expression = f"''.join(chr(({variables_reference["functions"]["ord"]}({variable_name}) - int({integer_noise(97)}) - int({integer_noise(shift)})) % int({integer_noise(26)}) + int({integer_noise(97)})) if {variable_name}.islower() else chr(({variables_reference["functions"]["ord"]}({variable_name}) - int({integer_noise(65)}) - int({integer_noise(shift)})) % int({integer_noise(26)}) + int({integer_noise(65)})) if {variable_name}.isupper() else {variable_name} for {variable_name} in {charr_expression}[int({integer_noise(trash_in_start)})::int({integer_noise(trash_in_mid+1)})])"

    return charr_expression.replace("int" , variables_reference["functions"]["int"]).replace("chr" , variables_reference["functions"]["chr"])

def obfuscate_float(float_number):
    global variables_reference

    string_numb = str(float_number)
    string_numb_obf = long_string_obf(string_numb)


    return f"getattr({variables_reference["variables"]["__builtins__"]} , {long_string_obf('eval')})({string_numb_obf})"

def special_arg_obf(special_arg):
    return f"getattr({long_string_obf(special_arg)} , {long_string_obf('eval')})"
    

class Obfuscator(ast.NodeTransformer):

    def __init__(self):
        super().__init__()
        self.current_scope_variables = {}

    def visit_BinOp(self, node):
        if isinstance(node.left, ast.Name) and node.left.id in variables_reference["variables"]:
            node.left.id = variables_reference["variables"][node.left.id]

        if isinstance(node.right, ast.Name) and node.right.id in variables_reference["variables"]:
            node.right.id = variables_reference["variables"][node.right.id]

        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        global variables_reference
        if isinstance(node.value, ast.Name) and node.value.id in variables_reference["modules"]:
            original_module = node.value.id
            new_name = variables_reference["modules"][original_module]
            node.value.id = new_name

        if isinstance(node.value, ast.Name) and node.value.id in variables_reference["variables"]:
            original_module = node.value.id
            new_name = variables_reference["variables"][original_module]
            node.value.id = new_name
        

        return node

    def visit_Constant(self, node):
        if isinstance(node.value, int):
            new_value_expr = ast.parse(integer_noise(node.value), mode='eval').body
            return new_value_expr

        elif isinstance(node.value, str):
            new_value_expr = ast.parse(string_obfuscation(node.value), mode='eval').body
            return new_value_expr

        elif isinstance(node.value, bool):
            new_value_expr = ast.parse(boolean_obf(node.value), mode='eval').body
            return new_value_expr

        elif isinstance(node.value, float):
            new_value_expr = ast.parse(obfuscate_float(node.value), mode='eval').body
            return new_value_expr

        else:
            return node

    def visit_Import(self, node):
        global variables_reference
        new_nodes = []

        for alias in node.names:

            original_name = alias.name
            if alias.asname:
                target_name = alias.asname
            else:
                target_name = original_name
                
            target_name_obf = variable_noise()

            variables_reference["modules"][target_name] = target_name_obf

            import_name_expr = ast.parse(string_obfuscation(original_name))

            new_node = ast.Assign(
                targets=[ast.Name(id=target_name_obf, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="__import__", ctx=ast.Load()),
                    args=[import_name_expr],
                    keywords=[]
                )
            )

            ast.copy_location(new_node, node)
            new_nodes.append(new_node)

        return new_nodes

    def visit_Call(self, node):
        global variables_reference
        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            
            if func_name in variables_reference["objects"]:
                actual_func_name = variables_reference["objects"][func_name]
                func_name_expr = ast.parse(string_obfuscation(actual_func_name), mode="eval").body

                new_func = ast.Subscript(
                    value=ast.Call(
                        func=ast.Name(id=variables_reference["functions"]["globals"], ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    ),
                    slice=func_name_expr,  
                    ctx=ast.Load()
                )

                pos_args = []
                for arg in node.args:
                    if isinstance(arg, ast.Constant):
                        if isinstance(arg.value, int):
                            pos_arg_expr = ast.parse(integer_noise(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, str):
                            pos_arg_expr = ast.parse(string_obfuscation(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, bool):
                            pos_arg_expr = ast.parse(boolean_obf(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, float):
                            pos_arg_expr = ast.parse(obfuscate_float(arg.value))
                            pos_args.append(pos_arg_expr)
                        else:
                            pos_args.append(arg)
                    elif isinstance(arg, ast.Name):
                        var_name = arg.id
                        if var_name in variables_reference["variables"]:
                            obfuscated_var_name = variables_reference["variables"][var_name]
                            obfuscated_arg = ast.Name(id=obfuscated_var_name, ctx=ast.Load())
                            pos_args.append(obfuscated_arg)
                        else:
                            pos_args.append(arg)
                    elif isinstance(arg, ast.BinOp):
                        pos_arg_expr = self.visit(arg)
                        pos_args.append(pos_arg_expr)
                    elif isinstance(arg, ast.Call):
                        nested_call = self.visit(arg)
                        pos_args.append(nested_call)
                    else:
                        pos_args.append(arg)

                keyword_args = []

                for arg in node.keywords:
                    if arg.arg in variables_reference["variables"]:
                        arg_actual_name = variables_reference["variables"][arg.arg]
                    else:
                        arg_actual_name = arg.arg
                    if isinstance(arg.value, ast.Constant):
                        if isinstance(arg.value.value, int):
                            kw_arg_expr = ast.parse(integer_noise(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value.value, str):
                            kw_arg_expr = ast.parse(string_obfuscation(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value, bool):
                            kw_arg_expr = ast.parse(boolean_obf(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value, float):
                            kw_arg_expr = ast.parse(obfuscate_float(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        else:
                            keyword_args.append(arg)
                    elif isinstance(arg.value, ast.Name):
                        var_name = arg.value.id
                        if var_name in variables_reference["variables"]:
                            obfuscated_var_name = variables_reference["variables"][var_name]
                            obfuscated_arg = ast.Name(id=obfuscated_var_name, ctx=ast.Load())
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=obfuscated_arg))
                        else:
                            keyword_args.append(arg)
                    elif isinstance(arg.value, ast.BinOp):
                        kw_arg_expr = self.visit(arg.value)
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                    elif isinstance(arg.value, ast.Call):  # Handle nested function calls
                        nested_call = self.visit(arg.value)  # Visit the nested call
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=nested_call))
                    else:
                        keyword_args.append(arg)

                new_call = ast.Call(
                    func=new_func,
                    args=pos_args,
                    keywords=keyword_args,
                )

                return new_call

                return self.generic_visit(node)
            if func_name in dir(builtins):
                func_name_expr = ast.parse(string_obfuscation(func_name), mode="eval").body
                
                dynamic_func = ast.Call(
                    func=ast.Name(id="getattr", ctx=ast.Load()),
                    args=[
                        ast.Name(id=variables_reference["variables"]["__builtins__"], ctx=ast.Load()),
                        func_name_expr,
                    ],
                    keywords=[],
                )

                pos_args = []
                for arg in node.args:
                    if isinstance(arg, ast.Constant):
                        if isinstance(arg.value, int):
                            pos_arg_expr = ast.parse(integer_noise(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, str):
                            pos_arg_expr = ast.parse(string_obfuscation(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, bool):
                            pos_arg_expr = ast.parse(boolean_obf(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, float):
                            pos_arg_expr = ast.parse(obfuscate_float(arg.value))
                            pos_args.append(pos_arg_expr)
                        else:
                            pos_args.append(arg)
                    elif isinstance(arg, ast.Name):
                        var_name = arg.id
                        if var_name in variables_reference["variables"]:
                            obfuscated_var_name = variables_reference["variables"][var_name]
                            obfuscated_arg = ast.Name(id=obfuscated_var_name, ctx=ast.Load())
                            pos_args.append(obfuscated_arg)
                        else:
                            pos_args.append(arg)
                    elif isinstance(arg, ast.BinOp):
                        pos_arg_expr = self.visit(arg)
                        pos_args.append(pos_arg_expr)
                    elif isinstance(arg, ast.Call):
                        nested_call = self.visit(arg)
                        pos_args.append(nested_call)
                    else:
                        pos_args.append(arg)

                keyword_args = []

                for arg in node.keywords:
                    if arg.arg in variables_reference["variables"]:
                        arg_actual_name = variables_reference["variables"][arg.arg]
                    else:
                        arg_actual_name = arg.arg
                    if isinstance(arg.value, ast.Constant):
                        if isinstance(arg.value.value, int):
                            kw_arg_expr = ast.parse(integer_noise(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value.value, str):
                            kw_arg_expr = ast.parse(string_obfuscation(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value, bool):
                            kw_arg_expr = ast.parse(boolean_obf(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value, float):
                            kw_arg_expr = ast.parse(obfuscate_float(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        else:
                            keyword_args.append(arg)
                    elif isinstance(arg.value, ast.Name):
                        var_name = arg.value.id
                        if var_name in variables_reference["variables"]:
                            obfuscated_var_name = variables_reference["variables"][var_name]
                            obfuscated_arg = ast.Name(id=obfuscated_var_name, ctx=ast.Load())
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=obfuscated_arg))
                        else:
                            keyword_args.append(arg)
                    elif isinstance(arg.value, ast.BinOp):
                        kw_arg_expr = self.visit(arg.value)
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                    elif isinstance(arg.value, ast.Call):  # Handle nested function calls
                        nested_call = self.visit(arg.value)  # Visit the nested call
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=nested_call))
                    else:
                        keyword_args.append(arg)

                new_node = ast.Call(
                    func=dynamic_func,
                    args=pos_args,
                    keywords=keyword_args,
                )
                
                return ast.copy_location(new_node, node)
            

            else:
                pos_args = []
                for arg in node.args:
                    if isinstance(arg, ast.Constant):
                        if isinstance(arg.value, int):
                            pos_arg_expr = ast.parse(integer_noise(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, str):
                            pos_arg_expr = ast.parse(string_obfuscation(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, bool):
                            pos_arg_expr = ast.parse(boolean_obf(arg.value))
                            pos_args.append(pos_arg_expr)
                        elif isinstance(arg.value, float):
                            pos_arg_expr = ast.parse(obfuscate_float(arg.value))
                            pos_args.append(pos_arg_expr)
                        else:
                            pos_args.append(pos_arg_expr)
                    elif isinstance(arg, ast.Name):
                        var_name = arg.id
                        if var_name in variables_reference["variables"]:
                            obfuscated_var_name = variables_reference["variables"][var_name]
                            obfuscated_arg = ast.Name(id=obfuscated_var_name, ctx=ast.Load())
                            pos_args.append(obfuscated_arg)
                        else:
                            pos_args.append(arg)
                    elif isinstance(arg, ast.BinOp):
                        pos_arg_expr = self.visit(arg)
                        pos_args.append(pos_arg_expr)
                    elif isinstance(arg, ast.Call):
                        nested_call = self.visit(arg)
                        pos_args.append(nested_call)
                    else:
                        pos_args.append(arg)

                keyword_args = []

                for arg in node.keywords:
                    if arg.arg in variables_reference["variables"]:
                        arg_actual_name = variables_reference["variables"][arg.arg]
                    else:
                        arg_actual_name = arg.arg
                    if isinstance(arg.value, ast.Constant):
                        if isinstance(arg.value.value, int):
                            kw_arg_expr = ast.parse(integer_noise(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value.value, str):
                            kw_arg_expr = ast.parse(string_obfuscation(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value, bool):
                            kw_arg_expr = ast.parse(boolean_obf(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        elif isinstance(arg.value, float):
                            kw_arg_expr = ast.parse(obfuscate_float(arg.value.value))
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                        else:
                            keyword_args.append(arg)
                    elif isinstance(arg.value, ast.Name):
                        var_name = arg.value.id
                        if var_name in variables_reference["variables"]:
                            obfuscated_var_name = variables_reference["variables"][var_name]
                            obfuscated_arg = ast.Name(id=obfuscated_var_name, ctx=ast.Load())
                            keyword_args.append(ast.keyword(arg=arg_actual_name, value=obfuscated_arg))
                        else:
                            keyword_args.append(arg)
                    elif isinstance(arg.value, ast.BinOp):
                        kw_arg_expr = self.visit(arg.value)
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                    elif isinstance(arg.value, ast.Call):  # Handle nested function calls
                        nested_call = self.visit(arg.value)  # Visit the nested call
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=nested_call))
                    else:
                        keyword_args.append(arg)

                if node.func.id in variables_reference["functions"]:
                    function_actual_name = variables_reference["functions"][node.func.id]
                else:
                    function_actual_name = variable_noise()
                    variables_reference["functions"][node.func.id] = function_actual_name

                new_node = ast.Call(
                    func=ast.Name(id=function_actual_name, ctx=ast.Load()),
                    args=pos_args,
                    keywords=keyword_args,
                )

            return ast.copy_location(new_node, node)

        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            var_name = node.func.value.id
            method_name = node.func.attr

            if method_name in variables_reference["functions"]:
                method_name = variables_reference["functions"][method_name]

            if var_name in variables_reference["modules"]:
                var_name = variables_reference["modules"][var_name]
            
            if var_name in variables_reference["objects"]:
                var_name = variables_reference["objects"][var_name]

            if var_name in variables_reference["variables"]:
                var_name = variables_reference["variables"][var_name]

            function_call_expr = ast.parse(string_obfuscation(method_name))

            new_node = ast.Call(
                func=ast.Name(id="getattr", ctx=ast.Load()),
                args=[
                    ast.Name(id=var_name, ctx=ast.Load()),
                    function_call_expr
                ],
                keywords=[]
            )
            pos_args = []
            for arg in node.args:
                if isinstance(arg, ast.Constant):
                    if isinstance(arg.value, int):
                        pos_arg_expr = ast.parse(integer_noise(arg.value))
                        pos_args.append(pos_arg_expr)
                    elif isinstance(arg.value, str):
                        pos_arg_expr = ast.parse(string_obfuscation(arg.value))
                        pos_args.append(pos_arg_expr)
                    elif isinstance(arg.value, bool):
                        pos_arg_expr = ast.parse(boolean_obf(arg.value))
                        pos_args.append(pos_arg_expr)
                    elif isinstance(arg.value, float):
                        pos_arg_expr = ast.parse(obfuscate_float(arg.value))
                        pos_args.append(pos_arg_expr)
                    else:
                        pos_args.append(arg)
                elif isinstance(arg, ast.Name):
                    var_name = arg.id
                    if var_name in variables_reference["variables"]:
                        obfuscated_var_name = variables_reference["variables"][var_name]
                        obfuscated_arg = ast.Name(id=obfuscated_var_name, ctx=ast.Load())
                        pos_args.append(obfuscated_arg)
                    else:
                        pos_args.append(arg)
                elif isinstance(arg, ast.BinOp):
                        pos_arg_expr = self.visit(arg)
                        pos_args.append(pos_arg_expr)
                elif isinstance(arg, ast.Call):
                    nested_call = self.visit(arg)
                    pos_args.append(nested_call)
                else:
                    pos_args.append(arg)

            keyword_args = []
            for arg in node.keywords:
                if arg.arg in variables_reference["variables"]:
                    arg_actual_name = variables_reference["variables"][arg.arg]
                else:
                    arg_actual_name = arg.arg
                if isinstance(arg.value, ast.Constant):
                    if isinstance(arg.value.value, int):
                        kw_arg_expr = ast.parse(integer_noise(arg.value.value))
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                    elif isinstance(arg.value.value, str):
                        kw_arg_expr = ast.parse(string_obfuscation(arg.value.value))
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                    elif isinstance(arg.value, bool):
                        kw_arg_expr = ast.parse(boolean_obf(arg.value.value))
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                    elif isinstance(arg.value, float):
                        kw_arg_expr = ast.parse(obfuscate_float(arg.value.value))
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                    else:
                        keyword_args.append(arg)
                elif isinstance(arg.value, ast.Name):
                    var_name = arg.value.id
                    if var_name in variables_reference["variables"]:
                        obfuscated_var_name = variables_reference["variables"][var_name]
                        obfuscated_arg = ast.Name(id=obfuscated_var_name, ctx=ast.Load())
                        keyword_args.append(ast.keyword(arg=arg_actual_name, value=obfuscated_arg))
                    else:
                        keyword_args.append(arg)
                elif isinstance(arg.value, ast.BinOp):
                    kw_arg_expr = self.visit(arg.value)
                    keyword_args.append(ast.keyword(arg=arg_actual_name, value=kw_arg_expr))
                elif isinstance(arg.value, ast.Call):  # Handle nested function calls
                    nested_call = self.visit(arg.value)  # Visit the nested call
                    keyword_args.append(ast.keyword(arg=arg_actual_name, value=nested_call))
                else:
                    keyword_args.append(arg)

            new_node = ast.Call(
                func=new_node,
                args=pos_args,  # Use original positional arguments
                keywords=keyword_args  # Use original keyword arguments
            )
            

            return ast.copy_location(new_node, node)
        
        return self.generic_visit(node)  # Visit other nodes normally

    def visit_FunctionDef(self, node):

        in_a_class = False
        parent = getattr(node, "parent", None)
        while parent:
            if isinstance(parent, ast.ClassDef):
                in_a_class = True
                break
            parent = getattr(parent, "parent", None)

        global variables_reference

        reserved_function_names = ["__init__", "__del__","__repr__", "__str__","__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__","__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__","__mod__", "__pow__","__getattr__", "__setattr__", "__delattr__", "__dir__","__len__", "__getitem__", "__setitem__", "__delitem__","__iter__", "__next__","__call__","__enter__", "__exit__","__hash__", "__bool__", "__copy__", "__deepcopy__", "__slots__"]

        reserved_argument_names = ["self","cls","mcs","args","kwargs"]


        original_name = node.name
        if not in_a_class:
            obfuscated_name = variable_noise()
            variables_reference["functions"][original_name] = obfuscated_name

            node.name = obfuscated_name
        else:
            if original_name not in reserved_function_names:
                obfuscated_name = variable_noise()
                variables_reference["functions"][original_name] = obfuscated_name

                node.name = obfuscated_name


        for arg in node.args.args:
            if arg.arg not in reserved_argument_names:
                if arg.arg not in variables_reference["variables"]:
                    variables_reference["variables"][arg.arg] = variable_noise()
                    print(variables_reference)
                    arg.arg = variables_reference["variables"][arg.arg]
                else:
                    arg.arg = variables_reference["variables"][arg.arg]

        # Check if the function is inside a class
        

        self.generic_visit(node)
        return node


    def visit_ClassDef(self, node):
        global variables_reference
        orignal_name = node.name
        if orignal_name in variables_reference["objects"]:
            node.name = variables_reference["objects"][orignal_name]
        else:
            variables_reference["objects"][orignal_name] = variable_noise()
            node.name = variables_reference["objects"][orignal_name]

        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        global variables_reference
        
        if isinstance(node.id, dict):
            node.id = list(node.id.keys())[0]
        #very hacky code idk why i need this
        #node.id somehow becomes dict sometimes

        if node.id in variables_reference["functions"]:
            node.id = variables_reference["functions"][node.id]

        if node.id in variables_reference["variables"]:
            node.id = variables_reference["variables"][node.id]

        return node

    def visit_Assign(self, node):
        global variables_reference
        reserved_argument_names = ["self","cls","mcs","args","kwargs"]
        for target in node.targets:
            if isinstance(target, ast.Name):
                original_var_name = target.id
                if original_var_name not in reserved_argument_names:
                    if original_var_name not in variables_reference["variables"]:

                        obfuscated_var_name = variable_noise()

                        variables_reference["variables"][original_var_name] = obfuscated_var_name

                    else:

                        obfuscated_var_name = variables_reference["variables"][original_var_name]
                else:
                    obfuscated_var_name = special_arg_obf(original_var_name)

                target.id = obfuscated_var_name

        self.generic_visit(node)
        return node

    def visit_For(self, node):
        global variables_reference

        if isinstance(node.target, ast.Name):
            original_name = node.target.id
            if original_name not in variables_reference["variables"]:
                obfuscated_name = variable_noise()
                variables_reference["variables"][original_name] = obfuscated_name
            else:
                obfuscated_name = variables_reference["variables"][original_name]
            node.target.id = obfuscated_name

        self.generic_visit(node)
        return node
        
def set_parents(node, parent=None):
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        set_parents(child, node)


def primary_crypt_function(file_name , output_path):
    with open(file_name, "r") as f:
        tree = ast.parse(f.read())
        set_parents(tree)
        vis = Obfuscator()
        new_tree = vis.visit(tree)



    with open(output_path , "w") as f:
        #make sure to write the math line
        some_default_values = [
            (variables_reference["variables"]["__builtins__"], f'eval({long_string_obf("__builtins__")})'), #__builtins__
            (variables_reference["modules"]["math"] , f'__import__({long_string_obf("math")})'), #math
            (variables_reference["functions"]["ord"], f'eval({long_string_obf("ord")})'),
            (variables_reference["functions"]["int"], f'eval({long_string_obf("int")})'),
            (variables_reference["functions"]["round"], f'eval({long_string_obf("round")})'),
            (variables_reference["functions"]["chr"], f'eval({long_string_obf("chr")})'),
            (variables_reference["functions"]["globals"], f'eval({long_string_obf("globals")})'),
        ] #__builtins__ , math module , ord function
        #maths_expr = f'{} , {} = eval({long_string_obf("__builtins__")}) , __import__({long_string_obf("math")})'
        random.shuffle(some_default_values)
        math_expr_part_1 = ""
        math_expr_part_2 = ""
        for expr in some_default_values:
            math_expr_part_1 = f"{math_expr_part_1}, {expr[0]}"
            math_expr_part_2 = f"{math_expr_part_2}, {expr[1]}"
        maths_expr = math_expr_part_1[2::] + " =" + math_expr_part_2[1::]
        f.write(maths_expr)
        f.write("\n")
        f.write(ast.unparse(new_tree))
