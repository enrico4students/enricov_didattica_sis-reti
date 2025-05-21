import os
import shutil
import subprocess
import sys

def check_executable(name):
    path = shutil.which(name)
    print(f"{name}: {'✅ trovato in ' + path if path else '❌ NON trovato'}")
    return path is not None

def check_windows():
    if os.name == 'nt':
        print("Sistema operativo: ✅ Windows")
        return True
    else:
        print("Sistema operativo: ❌ Non Windows (richiesto)")
        return False

def check_gpp_version():
    try:
        output = subprocess.check_output(['g++', '--version'], stderr=subprocess.STDOUT)
        print("g++: ✅ presente" + output.decode().splitlines()[0])
        return True
    except Exception as e:
        print("g++: ❌ NON trovato o errore esecuzione")
        return False

def check_compile_link():
    test_code = '''
    #include <winsock2.h>
    int main() {
        WSADATA wsa;
        return WSAStartup(MAKEWORD(2,2), &wsa);
    }
    '''
    with open("check_link.cpp", "w") as f:
        f.write(test_code)
    result = os.system("g++ check_link.cpp -o check_link.exe -lws2_32")
    os.remove("check_link.cpp")
    if os.path.exists("check_link.exe"):
        os.remove("check_link.exe")
    print("Compilazione con -lws2_32: " + ("✅ OK" if result == 0 else "❌ FALLITA"))
    return result == 0

def main():
    print("Verifica ambiente di sviluppo per progetto TCP/UDP:")
    ok = True
    ok &= check_windows()
    ok &= check_executable("g++")
    ok &= check_gpp_version()
    ok &= check_compile_link()
    print("Esito finale:", "✅ Ambiente OK" if ok else "❌ Ambiente NON pronto")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()