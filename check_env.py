import os
import shutil
import subprocess
import sys
from pathlib import Path

def check_executable(name: str):
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
        first_line = output.decode(errors="replace").splitlines()[0]
        print(f"g++: ✅ presente - {first_line}")
        return True
    except Exception:
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
    with open("check_link.cpp", "w", encoding="utf-8") as f:
        f.write(test_code)

    result = os.system("g++ check_link.cpp -o check_link.exe -lws2_32")

    os.remove("check_link.cpp")
    if os.path.exists("check_link.exe"):
        os.remove("check_link.exe")

    print("Compilazione con -lws2_32: " + ("✅ OK" if result == 0 else "❌ FALLITA"))
    return result == 0


def check_env_paths():
    """Controlla se le variabili di ambiente che sembrano contenere un singolo path esistono.
    Ignora sequenze (PATH) e ignora device/named pipe. Gestisce errori di stat()."""

    print("Verifica variabili di ambiente:")

    ok = True
    for var_name, value in os.environ.items():

        if not value or not isinstance(value, str):
            continue

        value = value.strip().strip('"')

        # Ignora variabili che contengono sequenze di percorsi (es. PATH)
        if os.pathsep in value:
            continue

        # Ignora device path / named pipe / extended-length path
        # Esempi:
        #   \\.\pipe\crashpad_...
        #   \\?\C:\...
        low = value.lower()
        if low.startswith("\\\\.\\") or low.startswith("\\\\?\\"):
            continue

        # Euristica: sembra un path?
        is_windows_drive = (
            sys.platform.startswith("win")
            and len(value) > 1
            and value[1] == ":"
        )

        if not ("/" in value or "\\" in value or is_windows_drive):
            continue

        path_obj = Path(value)

        try:
            # is_file / is_dir fanno stat(): possono generare OSError su device/named pipe
            if path_obj.is_file():
                # print(f"OK file {value}")
                pass
            elif path_obj.is_dir():
                # print(f"OK directory {value}")
                pass
            else:
                # Se non è file né dir, controllare comunque se "esiste"
                try:
                    if path_obj.exists():
                        print(f"OK esiste ma non è file né directory {value}")
                    else:
                        print(f"variabile {var_name} non esiste directory {value}")
                        ok = False
                except OSError:
                    # Esiste come oggetto speciale, ma non gestibile in modo standard
                    continue

        except (OSError, ValueError):
            # OSError: WinError 231 e simili (pipe busy, permessi, path speciali)
            # ValueError: path non valido per Windows (raro ma possibile)
            continue

    return ok

import os
from pathlib import Path

def check_path_directories():
    """
    Controlla se tutte le directory presenti nella variabile PATH esistono.
    """

    path_value = os.environ.get("PATH", "")

    if not path_value:
        print("PATH non definita")
        return False

    print("Verifica directory contenute in PATH:")

    ok = True
    for entry in path_value.split(os.pathsep):

        entry = entry.strip().strip('"')

        if not entry:
            continue

        path_obj = Path(entry)

        try:
            if path_obj.is_dir():
                pass
                # print(f"OK directory {entry}")
            elif path_obj.exists():
                print(f"path entry {entry} esiste ma non è directory")
                ok = False
            else:
                print(f"non esiste directory {entry}")
                ok = False

        except OSError:
            # gestisce casi rari (permessi o path speciali)
            print(f"errore accesso directory {entry}")
            ok = False

    return ok


def main():
    env_ok = check_env_paths()
    check_path_directories()
    print("Verifica ambiente di sviluppo per progetto TCP/UDP:")
    ok = True
    ok &= check_windows()
    ok &= check_executable("g++")
    ok &= check_gpp_version()
    ok &= check_compile_link()

    ok &= env_ok

    print("Esito finale:", "✅ Ambiente OK" if ok else "❌ Ambiente NON pronto")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
