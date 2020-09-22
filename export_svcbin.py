#coding: utf-8
import pywintypes, win32api, win32con

def main():

    with open("./service_bin.txt", "w") as fd:

        read_perm = ( win32con.KEY_READ | win32con.KEY_ENUMERATE_SUB_KEYS | win32con.KEY_QUERY_VALUE )

        hkey = win32api.RegOpenKeyEx( win32con.HKEY_LOCAL_MACHINE, "SYSTEM\ControlSet001\Services", 0, read_perm )


        names = [ data[0] for data in win32api.RegEnumKeyEx(hkey) ]

        for name in names:

            name = name.lower()
            fd.write("=========== %s ============\n" % name)
#            print("=========== %s ============" % name)

            # Image Path
            try:
                subkey = win32api.RegOpenKeyEx( hkey, name, 0, read_perm )
                image_path = win32api.RegQueryValueEx( subkey, "ImagePath" )
                path = win32api.ExpandEnvironmentStrings( image_path[0] )
                path = path.lower()

            except pywintypes.error:
                path = ""

            fd.write("Image Path: %s\n" % path)
#            print("Image Path: ", path)


            # Service DLL
            try:
                subkey = win32api.RegOpenKeyEx( hkey, "%s\Parameters" % name, 0, read_perm )
                service_dll = win32api.RegQueryValueEx( subkey, "ServiceDll" )
                path = win32api.ExpandEnvironmentStrings( service_dll[0] )
                path = path.lower()

            except pywintypes.error as e:
                path = ""

            fd.write("Service DLL: %s\n" % path)
#            print("Service DLL: ", path)

            fd.write("\n\n")
#            print("")
#            print("")


if __name__ == "__main__":
    main()