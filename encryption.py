import random
import os
import hashlib
import string

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

variables_reference["variables"]["code"] = variable_noise()
variables_reference["variables"]["initial_number"]= variable_noise()
variables_reference["variables"]["end_number"]= variable_noise() 
variables_reference["variables"]["initial_hash"] = variable_noise()
variables_reference["variables"]["key"] = variable_noise()
variables_reference["variables"]["j"] = variable_noise()
variables_reference["variables"]["i"] = variable_noise()
variables_reference["variables"]["data"] = variable_noise()
variables_reference["variables"]["None"] = variable_noise()


variables_reference["functions"]["range"] = variable_noise()
variables_reference["functions"]["len"] = variable_noise()
variables_reference["functions"]["next"] = variable_noise()
variables_reference["functions"]["bytearray"] = variable_noise()
variables_reference["functions"]["str"] = variable_noise()
variables_reference["functions"]["decryption"] = variable_noise()

variables_reference["modules"]["hashlib"] = variable_noise()



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

def polymorphic_encryption(code):
    key_range = random.randint(2**4 , 2**8)
    initial_number = random.randint(10000 , 10000000)
    end_number = initial_number + key_range

    actual_key = random.randint(initial_number , end_number)
    actual_key = hashlib.sha256(str(actual_key).encode()).hexdigest()

    initial_hash = hashlib.sha256(code.encode()).hexdigest()

    data = bytearray(code , "latin-1")
    key = bytearray(actual_key , "latin-1")

    encrypted_data = bytearray()

    for i in range(len(data)):
        encrypted_data.append(data[i] ^ key[i % len(key)])

    return encrypted_data.decode("latin-1") , initial_number , end_number , initial_hash

def decryption(code , initial_number , end_number , initial_hash):
    data = bytearray(code , "latin-1")
    for i in range(initial_number , end_number+1):
        actual_key = hashlib.sha256(str(i).encode()).hexdigest()
        key = bytearray(actual_key , "latin-1")

        decrypted_data = bytearray()

        for i in range(len(data)):
            decrypted_data.append(data[i] ^ key[i % len(key)])

        decrypted_data = decrypted_data.decode("latin-1")

        if hashlib.sha256(decrypted_data.encode()).hexdigest() == initial_hash:
            return decrypted_data

def primary_encryption_function(input_file , output_file):
    decryption_text = f'{variables_reference["functions"]["decryption"]} = ' + f'lambda {variables_reference["variables"]["code"]}, {variables_reference["variables"]["initial_number"]}, {variables_reference["variables"]["end_number"]}, {variables_reference["variables"]["initial_hash"]}: {variables_reference["functions"]["next"]}(({variables_reference["functions"]["bytearray"]}([{variables_reference["variables"]["data"]}[{variables_reference["variables"]["j"]}] ^ {variables_reference["variables"]["key"]}[{variables_reference["variables"]["j"]} % {variables_reference["functions"]["len"]}({variables_reference["variables"]["key"]})] for {variables_reference["variables"]["j"]} in {variables_reference["functions"]["range"]}({variables_reference["functions"]["len"]}({variables_reference["variables"]["data"]}))]).decode("latin-1") for {variables_reference["variables"]["i"]} in {variables_reference["functions"]["range"]}({variables_reference["variables"]["initial_number"]}, {variables_reference["variables"]["end_number"]}+1) if ({variables_reference["variables"]["key"]} := {variables_reference["functions"]["bytearray"]}(hashlib.sha256(str({variables_reference["variables"]["i"]}).encode()).hexdigest(), "latin-1")) and ({variables_reference["variables"]["data"]} := {variables_reference["functions"]["bytearray"]}({variables_reference["variables"]["code"]}, "latin-1")) and hashlib.sha256({variables_reference["functions"]["bytearray"]}([{variables_reference["variables"]["data"]}[{variables_reference["variables"]["j"]}] ^ {variables_reference["variables"]["key"]}[{variables_reference["variables"]["j"]} % {variables_reference["functions"]["len"]}({variables_reference["variables"]["key"]})] for {variables_reference["variables"]["j"]} in {variables_reference["functions"]["range"]}({variables_reference["functions"]["len"]}({variables_reference["variables"]["data"]}))]).decode("latin-1").encode()).hexdigest() == {variables_reference["variables"]["initial_hash"]}), {variables_reference["variables"]["None"]})'.replace('.decode("latin-1")' , f'.__getattribute__({long_string_obf("decode")})({long_string_obf("latin-1")})').replace('.encode()' , f'.__getattribute__({long_string_obf("encode")})()').replace('.hexdigest()' , f'.__getattribute__({long_string_obf("hexdigest")})()').replace("hashlib" , variables_reference["modules"]["hashlib"])

    with open(input_file, "r") as f:
        file_content = f.read()
        x = polymorphic_encryption(file_content)
    decryption_function_call = f'exec({variables_reference["functions"]["decryption"]}({x[0].encode("latin-1")}.decode("latin-1") , {x[1]} , {x[2]} , {long_string_obf(x[3])}))'



    with open(output_file , "w") as f:
        some_default_values = [
            (variables_reference["functions"]["range"], f'eval({long_string_obf("range")})'), 
            (variables_reference["functions"]["len"] , f'eval({long_string_obf("len")})'),
            (variables_reference["functions"]["next"], f'eval({long_string_obf("next")})'),
            (variables_reference["functions"]["bytearray"], f'eval({long_string_obf("bytearray")})'),
            (variables_reference["variables"]["None"], f'eval({long_string_obf("None")})'),
            (variables_reference["functions"]["str"], f'eval({long_string_obf("str")})'),
            (variables_reference["modules"]["hashlib"] , f'__import__({long_string_obf("hashlib")})'),
        ] #__builtins__ , math module , ord function
        random.shuffle(some_default_values)
        math_expr_part_1 = ""
        math_expr_part_2 = ""
        for expr in some_default_values:
            math_expr_part_1 = f"{math_expr_part_1}, {expr[0]}"
            math_expr_part_2 = f"{math_expr_part_2}, {expr[1]}"
        maths_expr = math_expr_part_1[2::] + " =" + math_expr_part_2[1::]
        f.write(maths_expr)
        f.write("\n")
        f.write(decryption_text)
        f.write("\n")
        f.write(decryption_function_call)





