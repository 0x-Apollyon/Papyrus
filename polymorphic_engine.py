import marshal 
import random
import string
import os
from collections import Counter
import math

# Run-Length Encoding (RLE)
def run_length_encoding(data):
    if not data:
        return b''
    
    encoded = []
    prev_byte = data[0]
    count = 1
    max_count = 255
    
    for byte in data[1:]:
        if byte == prev_byte and count < max_count:
            count += 1
        else:
            encoded.append(count)
            encoded.append(prev_byte)
            prev_byte = byte
            count = 1
    # Append the last run
    encoded.append(count)
    encoded.append(prev_byte)
    
    return bytes(encoded)

 
# Lempel-Ziv-Welch (LZW)
def lzw_compress(data):
    dictionary = {bytes([i]): i for i in range(256)}
    result = []
    current_string = b""
    dict_size = 256

    for byte in data:
        current_string += bytes([byte])
        if current_string not in dictionary:
            result.append(dictionary[current_string[:-1]])
            dictionary[current_string] = dict_size
            dict_size += 1
            current_string = bytes([byte])

    if current_string:
        result.append(dictionary[current_string])

    return result

def to_bytecode(py_code):
    xor_key = os.urandom(64)
    byte_code = marshal.dumps(compile(py_code, "<string>", "exec"))
    xored_bytecode = bytearray()
    for i in range(len(byte_code)):
        key_byte = xor_key[i % 64]
        xored_bytecode.append(byte_code[i] ^ key_byte)

    xored_bytecode = bytes(xored_bytecode)
    return xored_bytecode, xor_key

def calc_entropy(text):
    char_counts = Counter(text)
    total_chars = len(text)
    
    probabilities = [count / total_chars for count in char_counts.values()]
    
    entropy = 0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy

def anti_entropy(obf_code):

    entropy_dict = {
        "orginal":0,
        "lzw":0,
        "rle":0
    }

    entropy_dict["orginal"] = calc_entropy(obf_code)
    entropy_dict["rle"] = calc_entropy(str(run_length_encoding(obf_code)))
    entropy_dict["lzw"] = calc_entropy(str(lzw_compress(obf_code)))
    least_distance_method = ""
    least_distance = 99999
    for method in entropy_dict:
        entropy = entropy_dict[method]
        if entropy > 3.5 and entropy < 5:
            distance = 0
        elif entropy < 3.5:
            distance = 3.5 - entropy
        else:
            distance = entropy - 5
        
        if distance < least_distance:
            least_distance = distance
            least_distance_method = method

    if least_distance_method == "rle":
        encoded_data = run_length_encoding(obf_code)
        return encoded_data,"rle"
    elif least_distance_method == "lzw":
        compressed_data = lzw_compress(obf_code)
        return compressed_data,"lzw"
    else:
        return obf_code,"obf"


def polymorph(filepath , outpath):

    with open(filepath , "r") as f:
        code_sample = f.read()



    x = to_bytecode(code_sample)
    z = anti_entropy(x[0])
    anti_entropy_bytecode = z[0]

    xz = anti_entropy(x[1])

    global var_names_used
    var_names_used = []
    def random_var_name():
        global var_names_used
        words = words = ["apple", "banana", "cherry", "dog", "elephant", "friend", "guitar", "house", "idea", "jungle", "kiwi", "lion", "mountain", "notebook", "orange", "parrot", "quilt", "river", "sunflower", "tree", "umbrella", "violet", "window", "xylophone", "yellow", "zebra", "actor", "bicycle", "cloud", "dolphin", "energy", "forest", "grape", "horizon", "insect", "jewel", "kangaroo", "lemon", "mango", "night", "ocean", "peacock", "quiz", "rainbow", "star", "tiger", "universe", "vulture", "whale", "xenon", "yoga", "alien", "balloon", "carrot", "dinosaur", "earth", "flame", "green", "honey", "ink", "jump", "key", "lamp", "nut", "octopus", "plane", "question", "rose", "sun", "train", "umbrella", "vampire", "watch", "xerox", "yacht", "zero", "apple", "grape", "kiwi", "lemon", "mango", "peach", "pear", "plum", "strawberry", "blueberry", "blackberry", "raspberry", "melon", "papaya", "pineapple", "watermelon", "coconut", "fruit", "juice", "smoothie", "nectar", "vinegar", "salt", "sugar", "spice", "pepper", "mustard", "oregano", "basil", "rosemary", "thyme", "cilantro", "mint", "garlic", "onion", "tomato", "carrot", "broccoli", "spinach", "lettuce", "cucumber", "zucchini", "eggplant", "celery", "pea", "bean", "chili", "potato", "squash", "corn", "chicken", "beef", "pork", "fish", "shrimp", "lobster", "crab", "octopus", "squid", "tuna", "salmon", "cod", "mackerel", "herring", "bass", "trout", "catfish", "eel", "shark", "whale", "dolphin", "turtle", "seal", "penguin", "parrot", "eagle", "falcon", "hawk", "owl", "sparrow", "pigeon", "robin", "crow", "peacock", "flamingo", "woodpecker", "bat", "snake", "lizard", "frog", "toad", "alligator", "crocodile", "horse", "donkey", "mule", "sheep", "goat", "cow", "camel", "llama", "alpaca", "buffalo", "kangaroo", "koala", "platypus", "sloth", "monkey", "chimpanzee", "gorilla", "orangutan", "baboon", "lemur", "rabbit", "hare", "squirrel", "mole", "mouse", "rat", "hamster", "gerbil", "ferret", "bat", "antelope", "gazelle", "deer", "elk", "moose", "bison", "ram", "goose", "duck", "turkey", "chicken", "quail", "pheasant", "partridge", "hen", "rooster", "pigeon", "dove", "swan", "eagle", "buzzard", "hawk", "vulture", "pelican", "stork", "heron", "crane", "egret", "tern"]

        word_choosen = False
        while not word_choosen:
            word = random.choice(words)
            if word not in var_names_used:
                var_names_used.append(word)
                word_choosen = True
                return word


    lzw_string = random_var_name()
    lzw_data = random_var_name()

    rle_string = random_var_name()
    rle_data = random_var_name()

    anti_entropy_bytecode_name = random_var_name()

    final_code_name = random_var_name()

    exec_func_name = random_var_name()
    exec_xor_code_name = random_var_name()
    exec_xor_key_name = random_var_name()

    final_code_exec = random_var_name()

    final_key_name = random_var_name()
    anti_entropy_xor_key_name = random_var_name()

    rle_encoding_func_name = random_var_name()
    rle_encoding_func_var = random_var_name()
    rle_encoding_string = f"""
def {rle_encoding_func_name}({rle_encoding_func_var}):
    D={rle_encoding_func_var}
    if not D:return b''
    A=[];C=D[0];B=1;F=255
    for E in D[1:]:
        if E==C and B<F:B+=1
        else:A.append(B);A.append(C);C=E;B=1
    A.append(B);A.append(C);return bytes(A)
    """

    lzw_bytes_string_name = random_var_name()
    lzw_com_func_name = random_var_name()
    lzw_com_func_var = random_var_name()
    lzw_com_string = f"""
{lzw_bytes_string_name}=bytes
def {lzw_com_func_name}({lzw_com_func_var}):
    B={{{lzw_bytes_string_name}([A]):A for A in range(256)}};D=[];A=b'';E=256
    for F in {lzw_com_func_var}:
        A+={lzw_bytes_string_name}([F])
        if A not in B:D.append(B[A[:-1]]);B[A]=E;E+=1;A={lzw_bytes_string_name}([F])
    if A:D.append(B[A])
    return D
    """

    bytecode_func_name = random_var_name()
    bytecode_func_var = random_var_name()
    bytecode_creator_string = f"""
def {bytecode_func_name}({bytecode_func_var}):
    B=os.urandom(64);C=marshal.dumps(compile({bytecode_func_var},'<string>','exec'));A=bytearray()
    for D in range(len(C)):E=B[D%64];A.append(C[D]^E)
    A=bytes(A);return A,B
    """

    entropy_func_name = random_var_name()
    entropy_func_var = random_var_name()
    entropy_calc_string = f"""
def {entropy_func_name}({entropy_func_var}):
    C=Counter({entropy_func_var});D=len({entropy_func_var});E=[A/D for A in C.values()];B=0
    for A in E:
        if A>0:B-=A*math.log2(A)
    return B
    """

    anti_entropy_func_name = random_var_name()
    anti_entropy_func_var = random_var_name()
    anti_entropy_string = f"""
def {anti_entropy_func_name}({anti_entropy_func_var}):
    J='orginal';G='rle';D='lzw';A={anti_entropy_func_var};B={{J:0,G:0,D:0}};B[J]={entropy_func_name}(A);B[G]={entropy_func_name}({rle_encoding_func_name}(A));B[D]={entropy_func_name}({lzw_com_func_name}(A));E='';H=99999
    for I in B:
        C=B[I]
        if C>3.5 and C<5:F=0
        elif C<3.5:F=3.5-C
        else:F=C-5
        if F<H:H=F;E=I
    if E==G:K={rle_encoding_func_name}(A);return K,G
    elif E==D:L={lzw_com_func_name}(A);return L,D
    else:return A,'obf'
    """

    f"""
def {anti_entropy_func_name}({anti_entropy_func_var}):
    J='orginal';F='rle';E='lzw';A={anti_entropy_func_var};B={{J:0,E:0,F:0}};B[J]={entropy_func_name}(A);B[F]={entropy_func_name}(str({rle_encoding_func_name}(A)));B[E]={entropy_func_name}(str({lzw_com_func_name}(A)));G='';H=99999
    for I in B:
        C=B[I]
        if C>3.5 and C<5:D=0
        elif C<3.5:D=3.5-C
        else:D=C-5
        if D<H:H=D;G=I
    if G==F:K={rle_encoding_func_name}(A);return K,F
    elif G==E:L={lzw_com_func_name}(A);return L,E
    else:return A,'obf'
    """

    lzw_decom_string = f"""
def {lzw_string}({lzw_data}):
    E=b'';C=[bytes([A])for A in range(256)];G=256;F=E;A=E;D=None;B=E
    for D in {lzw_data}:
        if D<len(C):B=C[D]
        else:B=A+A[0:1]
        F+=B
        if A:C.append(A+B[0:1]);G+=1
        A=B
    return F
    """

    rle_decom_string =  f"""
def {rle_string}({rle_data}):
    return bytes([byte for i in range(0, len({rle_data}), 2) for byte in [{rle_data}[i+1]] * {rle_data}[i]])
    """

    execution_code = f"""
def {exec_func_name}({exec_xor_code_name},{exec_xor_key_name}):
    B={exec_xor_code_name};A=bytearray()
    for C in range(len(B)):D={exec_xor_key_name}[C%64];A.append(B[C]^D)
    A=marshal.loads(A);return A
    """

    dexor_func_name = random_var_name()
    dexor_content_name = random_var_name()
    dexor_xor_key_name = random_var_name()
    dexor_string = f"""
def {dexor_func_name}({dexor_content_name},{dexor_xor_key_name}):
    B={dexor_content_name};A=bytearray()
    for C in range(len(B)):D={dexor_xor_key_name}[C%64];A.append(B[C]^D)
    return A
    """

    bytecode_string = f"""
{anti_entropy_bytecode_name} = {anti_entropy_bytecode}
    """

    xorcode_string = f"""
{anti_entropy_xor_key_name} = {xz[0]}
    """

    my_own_file_path_newname = random_var_name()
    decrypted_bytecode_newname = random_var_name()
    new_xorkey_newname = random_var_name()
    readfile_newname = random_var_name()
    new_bytecode_newname = random_var_name()
    new_anti_entropy_newname = random_var_name()
    new_anti_entropy_2_newname = random_var_name()
    new_anti_entropy_bytecode_newname = random_var_name()
    new_anti_entropy_xorkey_newname = random_var_name()
    bytecode_entropy_method_newname = random_var_name()
    xorkey_entropy_method_newname = random_var_name()
    new_file_content_line_newname = random_var_name()
    new_xorkey_line_newname = random_var_name()
    new_data_decoding_line_newname = random_var_name()
    new_xorkey_decoding_line_newname = random_var_name()
    new_file_content_newname = random_var_name()
    write_file_newname = random_var_name()

    polymorphism_string = f"""
{my_own_file_path_newname} = os.path.join(os.path.dirname(__file__) , os.path.basename(__file__))
with open({my_own_file_path_newname} , "r") as {readfile_newname}:
    file_content = {readfile_newname}.readlines()

{decrypted_bytecode_newname } = {dexor_func_name}({final_code_name} , {final_key_name});{new_xorkey_newname} = os.urandom(64);{new_bytecode_newname} = {dexor_func_name}({decrypted_bytecode_newname } , {new_xorkey_newname});{new_anti_entropy_newname} = {anti_entropy_func_name}({new_bytecode_newname});{new_anti_entropy_bytecode_newname} = {new_anti_entropy_newname}[0];{bytecode_entropy_method_newname} = {new_anti_entropy_newname}[1];{new_anti_entropy_2_newname} = {anti_entropy_func_name}({new_xorkey_newname});{new_anti_entropy_xorkey_newname} = {new_anti_entropy_2_newname}[0];{xorkey_entropy_method_newname} = {new_anti_entropy_2_newname}[1];{new_file_content_line_newname} = f"{anti_entropy_bytecode_name} = {{{new_anti_entropy_bytecode_newname}}}";{new_xorkey_line_newname} = f"{anti_entropy_xor_key_name} = {{{new_anti_entropy_xorkey_newname}}}"

if {bytecode_entropy_method_newname} == "rle":{new_data_decoding_line_newname} = f"{final_code_name} = {rle_string}({anti_entropy_bytecode_name})"
elif {bytecode_entropy_method_newname} == "lzw":{new_data_decoding_line_newname} = f"{final_code_name} = {lzw_string}({anti_entropy_bytecode_name})"
else:{new_data_decoding_line_newname} = f"{final_code_name} = {anti_entropy_bytecode_name}"

if {xorkey_entropy_method_newname} == "rle":{new_xorkey_decoding_line_newname} = f"{final_key_name} = {rle_string}({anti_entropy_xor_key_name})"
elif {xorkey_entropy_method_newname} == "lzw":{new_xorkey_decoding_line_newname} = f"{final_key_name} = {lzw_string}({anti_entropy_xor_key_name})"
else:{new_xorkey_decoding_line_newname} = f"{final_key_name} = {anti_entropy_xor_key_name}"

{new_file_content_newname} = []
for i in range(len(file_content)):
    if i == 79:{new_file_content_newname}.append({new_file_content_line_newname});{new_file_content_newname}.append("<newline-placeholder>")
    elif i == 82:{new_file_content_newname}.append({new_xorkey_line_newname});{new_file_content_newname}.append("<newline-placeholder>")
    elif i == 84:{new_file_content_newname}.append({new_data_decoding_line_newname});{new_file_content_newname}.append("<newline-placeholder>")
    elif i == 85:{new_file_content_newname}.append({new_xorkey_decoding_line_newname});{new_file_content_newname}.append("<newline-placeholder>")
    else:{new_file_content_newname}.append(file_content[i])

with open({my_own_file_path_newname} , "w") as {write_file_newname}:
    {write_file_newname}.writelines({new_file_content_newname})
    """.replace("<newline-placeholder>" , r"\n")

    with open(outpath , "w") as f:
        f.write("from collections import Counter")
        f.write("\n")
        f.write("import random")
        f.write("\n")
        f.write("import math")
        f.write("\n")
        f.write("import os")
        f.write("\n")
        f.write("import marshal")
        f.write("\n")
        poly_neccessary_funcs = [rle_encoding_string , lzw_com_string , bytecode_creator_string , entropy_calc_string , anti_entropy_string , dexor_string]
        for func in poly_neccessary_funcs:
            f.writelines(func)
            f.write("\n")
        f.writelines(execution_code)
        f.write("\n")
        f.writelines(lzw_decom_string)
        f.write("\n")
        f.writelines(rle_decom_string)
        f.write("\n")
        f.writelines(bytecode_string)
        f.write("\n")
        f.writelines(xorcode_string)

        if z[1] == "rle":
            entrop_string = f"{final_code_name} = {rle_string}({anti_entropy_bytecode_name})"
        elif z[1] == "lzw":
            entrop_string = f"{final_code_name} = {lzw_string}({anti_entropy_bytecode_name})"
        else:
            entrop_string = f"{final_code_name} = {anti_entropy_bytecode_name}"
        f.write("\n")
        f.write(entrop_string)
        if xz[1] == "rle":
            entrop_string = f"{final_key_name} = {rle_string}({anti_entropy_xor_key_name})"
        elif xz[1] == "lzw":
            entrop_string = f"{final_key_name} = {lzw_string}({anti_entropy_xor_key_name})"
        else:
            entrop_string = f"{final_key_name} = {anti_entropy_xor_key_name}"
        f.write("\n")
        f.write(entrop_string)
        f.write("\n")
        f.write(f"{final_code_exec} = {exec_func_name}({final_code_name} , {final_key_name})")
        f.write("\n")
        f.writelines(polymorphism_string)
        f.write("\n")
        f.write(f"exec({final_code_exec})")

    



