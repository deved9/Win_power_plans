import os, subprocess

#get names and GUIDs and parse them
class Plan:
    def __init__(self, guid, name):
        self.name = name
        self.guid = guid

plans_raw = subprocess.check_output(["powercfg.exe","-list"],shell=True,text=True)

plans = []
for plan in "".join(plans_raw.replace(")","").replace("(","").replace("\xa0","a").replace("RyzenT", "Ryzen").replace(" *","").split("\n")[3:]).split("Power Scheme GUID: ")[1:]:
    guid, name = plan.split("  ")
    print(name)
    print(guid)
    name = name[:-2] if ') *' in name else name
    plans.append(Plan(guid, name))


#create bat files to set power plans
for plan in plans:
    with open(f"{plan.name}.bat","w") as out:
        out.write(f"echo off\nC:\Windows\System32\powercfg.exe /setactive {plan.guid}")

#create folde to put the shortcuts to
def rm_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path,item)):
                rm_dir(os.path.join(path,item))
            else:
                os.remove(os.path.join(path,item))
        rm_dir(path)

if os.path.isdir(os.path.join(os.getcwd(),"Power Plans")):
    rm_dir(os.path.join(os.getcwd(),"Power Plans"))

os.mkdir(os.path.join(os.getcwd(),"Power Plans"))

#create shortcuts
def mkShortcut(pathToShortcut,targetPath):
    os.system(f'powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut(\'{pathToShortcut}.lnk\');$s.TargetPath=\'{targetPath}.bat\';$s.Save()"')

for plan in plans:
    mkShortcut(os.path.join(os.path.join(os.getcwd(),"Power Plans"),plan.name),os.path.join(os.getcwd(),plan.name))