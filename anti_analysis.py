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


#technique 1: basic debugger detection , (incode) (cross platform)

basic_debugger = """
import sys

if sys.gettrace() is not None:
    <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

#technique 2: module inspection , (incode) (cross platform)

module_inpsection = """
analysis_tools = [1191842125,1571033776,2113409923,395972688,816320867,764416249,1841697332,1170084281,881988028,775754072,106696775,1521488409,1007620532,1271271902,1161433683,1113133645,921178501,1157370361,42340314,1811419765,1041568110,1206129152,470618262,1289228939,994906562,417534136,985272649,1862800097,974000417,1280381382,163254465,810291723,724898128,1862800097,1322783176,710283526,1585910316,1255608817,702746923,484446469,916394549,913510568,630722883,561713358,448204989,903025034,1081872824,1311314431,898371886,447877327]

import sys
import hashlib
import zlib

for module in sys.modules:
    if zlib.adler32(hashlib.sha256(module.encode()).hexdigest().encode()) in analysis_tools:
        <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

#technique 3: stack frame analysis (incode) (cross platform)
stack_frame = """
analysis_tools = ['pydevd', 'ptvsd', 'pdb', 'ipdb', 'rpdb', 'wdb', 'debugpy', 'pydbg', 'pytrace', 'pyinspector', 'pydev', 'pycharm-debug', 'pycharm_debugger', 'pyringe', 'celery.worker', 'bpdb', 'pytest', 'nose', 'unittest', 'doctest', 'trace', 'cProfile', 'profile', 'line_profiler', 'memory_profiler', 'pyinstrument', 'yappi', 'pyvmmonitor', 'bpython', 'ipython', 'jupyter_client', 'jupyter_core', 'tox', 'pyvmmonitor', 'vprof', 'pympler', 'objgraph', 'pycallgraph', 'coverage', 'mypy', 'pylint', 'flake8', 'bandit', 'radon', 'pyflame', 'pyspy', 'strace', 'ltrace', 'ptrace', 'sysdig']

import inspect

for frame in inspect.stack():
    for tool in analysis_tools:
        if tool in frame.filename:
            <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

#technique 4: env detection (exec) (cross platform)

env_detection = """
import os
import hashlib
import zlib

analysis_env_vars = ["776278249","1111888327","1367806477","1170543018","1998787301","1087705466","452071581","1378423221","1242567102","1493045800","857477574","1318850996","4033155066","3990491076","1786647183","1052643804","1658131022","902697418","830476603","332533825","1313214994","809767329","1602490858","539562146","1700860593","274862286","908726710","1338315219","1275007458","784077075","998773027","1613239041","2099974920","1493832183","1404440972","1215893910","1049104847","1092751688","227086589","1019482442","767037780","519835822","532353308","1341788554","999428540","323227797","1928467300","1227362987","1135481458","1593381504","1306202625","1049760197","578752673","1518146152","1329992174","425005245"]
    
virtualization_indicators = ["1717900002","707072256","808456527","541593886","1830621725","1091703215","587600270","535761121","2048529078","1181225349","461115608","419827880"]

all_env_vars = analysis_env_vars + virtualization_indicators

for key in os.environ.keys():
    if str(zlib.adler32(hashlib.sha256(key.encode()).hexdigest().encode())) in all_env_vars:
        <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""


#technique 6: mac address check (exec) (cross platform)

mac_address_check = """
import hashlib
import zlib

mac_addresses = ["664539362","1207243232","403247428","1410863634","861737218","670044362","606015699","1368002982","1432883765","1156583742","1145705023","452136971","379195637","1082921352","1832522492","1140331129","1200296400","691933454","1415254604","1170149666","951980471","1249710597","961483385","240324751","1016140062","1071780261","1127944677","1069224407","864358742","1538134586","907415753","915149339","291115167","1469321733","1267929550","908005542","851841200","685248985","1820987978","748425631","530780443","575279354","955650420","661262767","1148391885","1269502479","505614631","1180307903","1183584670","1341198877","1231622596","363008141","522195075","1048056227","955847021","816582935","973214220","1348473265","1313542691","954339610","446566536","1201738209","1249907147","1277629051","871109101","691933622","1475416744","655102383","1400967672","1191580154","487657829","1009521088","649531607","1269895571","1173164475","39325680","794759467","717492520","757469662","856690964","675221890","1113723272","1649086977","1351881281","990712302","473960612","406065341","1261310489","1671238415","1091441205","584847682","866259279","1334317459","361697470","1045959254","842142046","1055461807","1224938057","1531187890","456659267","797118999","1908937486","1097470399","1995575955","1513034375","890769751","1088033187","908595321","1663636043","1396183517","530190465","1496191546","1700729416","868487621","1557074567","1364660751","781127879","962466184","1374687701","820121862","1021448761","820711675","1555173848","1276121569","1093472733","1602949732","884150580","956698923","704975252","809570772","494211114","878383401","1343296016","579670227","799543762","571543733","1023349356","1481249449","1293881746","1688605209","593891437","1316295097","4273934443","1264521773","797118827","725684468","1035997553","853217555","1015746983","1294864971","791024023"]

import uuid

mac_id = ":".join(f"{b:02x}" for b in uuid.getnode().to_bytes(6))
hash = hashlib.sha256(mac_id.encode()).hexdigest()
hash = str(zlib.adler32(hash.encode()))
if mac_id in mac_addresses:
    <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

#technique 7: username check (exec) (cross platform)

username_check = """
import os
import hashlib
import zlib

blacklisted_username = ["332140601","918294753","1637290713","1134629437","1545212389","1284182524","541266085","446107840","940773797","1142428068","174198701","1195119068","635769043","1056969187","973476238","875172136","1398936189","1306857955","1075384693","1250890260","946999661","419107102","1383797389","1112085048","1172050426","645533968","1211896246","418255071","437456951","866324776","1104679365","519311580","997396857","940511528","851710180","1356993049","201658363","1115492883","1109135853","1376457289","1195512130","173740090","324931805","878449021","1600787129","874975518","1238438199","1079513541","538055068","673386836","1210126734","1334382956","694948105","790958309","1260065174","1199968628","1645941416","576590111","1099436467","944378306","768413854","1340674533","1122832825","314904839","732500349","1025118434","815206541","1235358236","680726893","1843925603","648024422","427561141","564203674","1328943571","254611506","1774916309","2066486122","841224598","507646106","1457918526","583930086","1673794077","1157239368","627052844","1367282318","1666322956","883298438","1204359538","1284510240","908136727","1469780540","1030099302","603525360","881987773","1473581594","1525092930","1622741655","245239896","1679102562","401936604","1156518473","739053852","651694369","848171352","22089777","2087785422","884805947","1010241953","962531686","966463842","1329205765","713298138","914428201","768741657","1281692164","951783871","1154290079","1610879566","1282478382","874516791","1265373702","296161213","1238634921","444666176","1416630800","636424502","1417286192","1194201666","483397738","984289793","1209930169","1153831468","1867911913","1665667839","1415188976","924783086","1619661481","1371869646","45879417","1996755634","1626018462","1587679923","1273893458","127012819","1354109291","467996814","654315811","1498092115","855773575","1251218049","707334344","1282543987","517017850","597233861","1291326190","1230377322","1291784735","3783462797","1251938815","818745603","867635623","572657879","1285099901","524292438","922292671","620958119","1293357699","1783829295","1051595075","965349710","136384627","1790251571","892932372","921047337","474419357","1559433847","490279259","615387431","4143386561","1390154365","685248854","1519260130","793776423","1175130452","1325142518","467406928","603590947","1366233556","737743245","128257958","904925350","1181880814","1807618722","181473378","1463685440","4120907912","4283568042","821629470","1204949412","380178708","1016467966","1303253371","1666060865","480448795","1231163954","854855912","360321166","1264194012","893129109","1430786504","1988170452","472846613","1151472146","795611366","1422660150","1201541474","762646740","1384976942","1135612378","1425347164","234426475","535498870","734663021","338628911","799740171","1190007202","607916312","542576745","1412829796","1312428563","1165693351","900403588","1176637964","1199378967","689639893","1193415042","678760657","151589079","709300492","237703220","1101926671","1167593935","1074860544","978194963","1342050839","1007882842","1500713497","1265373708","2059211422","958796221","790892996","839782780","182718532","746524827","384635090","168824868","977801602","681447733","1581453867","1196102142","603459859","935334265","1628771052","730927310","1399394879","1571230224","668537210","430051518","1232998783","318902220","1393627610","897782330","1361515147","839389562","1265963317","968102286","679743756","4139454379","818549075","536023419","1312362905","325128409","987500857","693637615","1099960898","499912963","1028985294","1089147340","294654120","1070993872","1185091988","604180839","967577791","1049104847","1137250718","4280815605","1434587712","257167454","826347927","722211072","1661866768"]


username = os.getlogin()
hash = hashlib.sha256(username.encode()).hexdigest()
hash = str(zlib.adler32(hash.encode()))
if hash in blacklisted_username:
    <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

#technique 8: hwid check (exec) (cross platform)

hwid_check = """
import uuid

blacklisted_hwid = ["734466325","1090458014","1153110591","1517425347","1144066451","268111865","4029485082","1779569547","1078661644","1229853215","970658170","764350743","895947106","1059000751","593563969","1673466464","1463816847","642519289","1204490711","1741886015","1671828060","2044924596","419696771","725946678","310317076","902631789","1336349211","426578188","1183977776","1457459786","1474368252","960696756","95948817","1141248474","820253099","1010242170","247402824","1346572834","770642200","2097681040","1894781738","867569894","1977684685","692588872","1380389367","802165017","758518037","366284948","1359417851","1045958982","558961044","705958172","1239945677","836309349","932843908","684200152","618336469","987959737","1776358088","2123764356","405147739","757731841","1218187588","842010839","1327239734","1157239053","1510543784","1418334766","1071452727","219943031","1081938163","109252587","1034424749","1489637913","1532367446","4285992976","218107906","1298272716","1723142803","768479697","600445152","483660064","747442573","1712853655","1132532323","344789293","1015812448","1402868330","151719959","776999271","563941667","940511587","844435847","1431966190","2056524443","702615936","1627591295","1032262206","1847464606","1225134470","761532809","2667647783","309137669","1380913710","684855497","1261310537","1349521933","1036980638","997003602","1990988478","950669843","647500076","409800840","227283142","1624379996","564072837","1528828439","516886775","702353775","1456214671","876417577","493490499","1112871265","968692097","2101285613","1127158080","754389288","1078530489","4247130166","182194381","633540921","1024725385","913838372","1351029286","970002917","820908314","613748835","1642926642","575541456","551686467","1195905490","1289032227","347279611","1410339260","1623855696","710676823","670372065","841683183","282267962","1704464938","1034228355","607719699","1296044548","1004278290","274010325","803475707","981209512","824840536","185143421","1322259055","209194954","622203106","48173093","811012470","1152520550","865472848","950604343","1463620300","1183977776","1977684685","1213075907","1318195817","1310069213","895947106","734466325","1859654396","880742679","1335693808","1133777441","488051058","123867284","1779569547","478810279","121835609","492900768","475664642","430379233","1298272716","550375743","1193087221","733352127","1589842523","1578111579","3733131184","1246892534","820253099","1098060106","445059270","692588872","1380389367","440471830","1327239734","1239028296","1090458014","2044924596","364384266","718934313","1025380839","315297920","1612648883","1673466464","1033703807","916525438","1110708722","219943031","2167280477","2123764356","218107906","1510543784","712839500","866914592","1081938163","685445326","504762666","798364214","942674295","753733969","4267511827","717361387","95948817","1068831230","902631789","1977684685"]

mac_address = uuid.getnode()
hwid = str(uuid.UUID(int=mac_address)).upper()
hash = hashlib.sha256(hwid.encode()).hexdigest()
hash = str(zlib.adler32(hash.encode()))
if hash in blacklisted_hwid:
    <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

#technique 9: time detection (incode) (cross platform)

time_detection = """
import datetime
import time

stat_max = 0.018253
threshold = 0.018253 + (0.018253*0.5) #50%

detect_score = 0
for i in range(3):
    now = datetime.datetime.now()
    time.sleep(0.01)
    diff = datetime.datetime.now() - now
    if float(str(diff).split(":")[-1]) > threshold:
        detect_score = detect_score + 1

if detect_score > 2:
    <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

#uptime check (exec) (cross platform)

uptime_check = """
import ctypes
import platform
import hashlib

if hashlib.sha256(platform.system().encode()).hexdigest().lower() == "d598026a9cbc60505f138ce53ac78088d582100c196d0f70c7e2538d4a8d7e10":
    import ctypes
    lib = ctypes.windll.kernel32
    uptime = lib.GetTickCount64()
    uptime = int(str(uptime)[:-3])
    if uptime < 7200:
        <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
else:
    import subprocess
    result = subprocess.run(["uptime", "-s"], capture_output=True, text=True, check=True)
    from datetime import datetime
    uptime_start = datetime.strptime(result.stdout.strip(), "%Y-%m-%d %H:%M:%S")
    current_time = datetime.now()
    uptime_seconds = (current_time - uptime_start).total_seconds()
    if uptime_seconds < 7200:
        <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

#technique 14: disk size check (exec) (ross platform)

disk_size_check = """
import shutil
import os

if os.name == "nt":
    total, used, free = shutil.disk_usage(r"C:\")
    total = total // (1000 ** 3)
    if total < 100:
        <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
else:
    total, used, free = shutil.disk_usage("/")
    total = total // (1000 ** 3)
    if total < 100:
        <|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>
"""

def apply_anti_analysis(inputfile , outputfile , placeholder="quit()"):
    placeholder = f"exec({long_string_obf(placeholder)})"
    techniques_incode = [basic_debugger , module_inpsection , stack_frame, username_check , time_detection]
    techniques_incode = []
    techniques_exec = [env_detection , mac_address_check,hwid_check,uptime_check, disk_size_check]
    with open(inputfile , "r+") as f:
        content = f.read()
        f.seek(0,0)
        for technique in techniques_incode:
            technique = technique.replace("<|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>" , placeholder)
            f.write(technique)
            f.write("\n")
        for technique in techniques_exec:
            technique = technique.replace("<|PLACEHOLDER FOR ANALYSIS DETECTION CODE|>" , placeholder)
            technique = f"exec({long_string_obf(technique)})"
            f.write(technique)
            f.write("\n")
        f.write(content)
        









