import os
from crypter import primary_crypt_function
from encryption import primary_encryption_function
from compressor import primary_compress_function
from polymorphic_engine import polymorph
import argparse
from anti_analysis import apply_anti_analysis


if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

print("""

   ▄███████▄    ▄████████    ▄███████▄ ▄██   ▄      ▄████████ ███    █▄     ▄████████ 
  ███    ███   ███    ███   ███    ███ ███   ██▄   ███    ███ ███    ███   ███    ███ 
  ███    ███   ███    ███   ███    ███ ███▄▄▄███   ███    ███ ███    ███   ███    █▀  
  ███    ███   ███    ███   ███    ███ ▀▀▀▀▀▀███  ▄███▄▄▄▄██▀ ███    ███   ███        
▀█████████▀  ▀███████████ ▀█████████▀  ▄██   ███ ▀▀███▀▀▀▀▀   ███    ███ ▀███████████ 
  ███          ███    ███   ███        ███   ███ ▀███████████ ███    ███          ███ 
  ███          ███    ███   ███        ███   ███   ███    ███ ███    ███    ▄█    ███ 
 ▄████▀        ███    █▀   ▄████▀       ▀█████▀    ███    ███ ████████▀   ▄████████▀  
                                                   ███    ███                         

""")
print("Python obfuscation and evasion")
print("Disclaimer: Im not responsible for how you use papyrus")
print("v1.1")

input_file = input("Enter file path to obfuscate (.py) |> ").strip()
if input_file[-3::].lower() != ".py":
    print("[X] Only python files ending in .py")
    quit()

input_file_2 = input_file
output_file = f"{os.path.basename(input_file)}_obf.py"

if not os.path.isfile(input_file):
    print("[X] File does not exist, please recheck the path")
    quit()

crypt_input = input("Perform basic crypt and obfuscation on the file (Y)es/(N)o |> ").strip()
compression_input = input("Perform compression based obfuscation on the file (Y)es/(N)o |> ").strip()
anti_analysis_input = input("Add anti analysis and debugging code to the file (Y)es/(N)o |> ").strip()

if crypt_input.lower() in ("yes" , "ye" , "y" , "yeah"):
    primary_crypt_function(input_file , output_file)
    input_file = output_file

if compression_input.lower() in ("yes" , "ye" , "y" , "yeah"):
    primary_compress_function(input_file , output_file)
    input_file = output_file

if anti_analysis_input.lower() in ("yes" , "ye" , "y" , "yeah"):
    anti_analysis_trigger_input = input("Path of the python code to be run if analysis is detected (it quits by default) |> ")
    try:
        with open(anti_analysis_trigger_input , "r") as f:
            anti_analysis_code = f.read()
        apply_anti_analysis(input_file , output_file , anti_analysis_code)
    except:
        apply_anti_analysis(input_file , output_file)

    input_file = output_file

encryption_input = input("Perform XOR encryption based obfuscation to the file (Y)es/(N)o |> ").strip()
polymorph_input = input("Make your code polymorphic (WARNING:YOU CANT COMPILE OR TAMPER WITH POLYMORPHIC CODE) (Y)es/(N)o |> ").strip()

if encryption_input.lower() in ("yes" , "ye" , "y" , "yeah"):
    primary_encryption_function(input_file , output_file)
    input_file = output_file

if polymorph_input.lower() in ("yes" , "ye" , "y" , "yeah"):
    polymorph(input_file , output_file)


print(f"[*] File {input_file_2} has been obfuscated successfully. You can see it at {output_file}")


