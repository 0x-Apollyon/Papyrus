import lzma
import base64
import random
import string
import os

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

variables_reference["modules"]["lzma"] = variable_noise()
variables_reference["modules"]["base64"] = variable_noise()
variables_reference["modules"]["lzmadecomp"] = variable_noise()

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

def compress_code(code):
    code = base64.b85encode(code.encode()).decode()
    compressed = lzma.compress(code.encode())

    return compressed

def compress_executor(code):
    some_default_values = [
        (variables_reference["modules"]["lzma"] , f'__import__({long_string_obf("lzma")})'),
        (variables_reference["modules"]["base64"] , f'__import__({long_string_obf("base64")})'),
    ]

    more_stuff = f'{variables_reference["modules"]["lzmadecomp"]} = eval({long_string_obf(variables_reference["modules"]["lzma"] + ".LZMADecompressor()")})'

    random.shuffle(some_default_values)
    math_expr_part_1 = ""
    math_expr_part_2 = ""
    for expr in some_default_values:
        math_expr_part_1 = f"{math_expr_part_1}, {expr[0]}"
        math_expr_part_2 = f"{math_expr_part_2}, {expr[1]}"
    maths_expr = math_expr_part_1[2::] + " =" + math_expr_part_2[1::]
    
    compressed_code = compress_code(code)


    main_value = f'exec(getattr({variables_reference["modules"]["base64"]}, {long_string_obf("b85decode")})(getattr({variables_reference["modules"]["lzmadecomp"]}, {long_string_obf("decompress")})({compressed_code})).__getattribute__({long_string_obf("decode")})())'

    return maths_expr + "\n" + more_stuff + "\n" + main_value


def primary_compress_function(input_file , output_file):
    with open(input_file , "r") as f:
        file_content = compress_executor(f.read())

    with open(output_file , "w") as f:
        f.write(file_content)

