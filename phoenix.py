#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
import importlib
import importlib.util
import pathlib
import readline
import sys
import time
import os
import re
import cowsay
import colorama
from colorama import Fore, Style
from loguru import logger
from rich.console import Console
from rich.table import Table


#cowsay
version_path = pathlib.Path.cwd() / "VERSION"
with open(version_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    version = lines[0]
cowsay.cow('Phoenix Framework Version:%s' %(version))
#exploit
dir = pathlib.Path.cwd() / "modules" / "exploit"
count = 0
for root,dirs,files in os.walk(dir):
    for each in files:
        count += 1

print("\033[34mNumber of exploits:\033[0m",count)
#scanner
dir_scanners = pathlib.Path.cwd() / "modules" / "scanner"
s_count = 0
for root,dirs,files in os.walk(dir_scanners):
    for each in files:
        s_count += 1

print("\033[34mNumber of scanners:\033[0m",s_count)

#tools
dir_tools = pathlib.Path.cwd() / "modules" / "tools"
s_count = 0
for root,dirs,files in os.walk(dir_tools):
    for each in files:
        s_count += 1

print("\033[34mNumber of tools:\033[0m",s_count)
class PhoenixShell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.module = None
        self.prompt = "{}phoenix2{} > ".format(Fore.YELLOW, Style.RESET_ALL)

    def do_use(self, arg):
        "use exploit/solr/cve-2019-0193"
        args = arg.split()
        try:
            module_path = pathlib.Path.cwd() / "modules" / (args[0] + ".py")
        except:
            logger.error("No module specified")
            return
        relative_path = module_path.relative_to(pathlib.Path.cwd() / "modules")

        if not module_path.is_file():
            logger.error("the specified module does not exist")
            return
        spec = importlib.util.spec_from_file_location("module.name", str(module_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.module = module.Module(logger)
        logger.success("Successfully loaded {}".format(relative_path))
        self.prompt = "{}phoenix2{} ({}{}{}) > ".format(
            Fore.YELLOW, Style.RESET_ALL, Fore.RED, relative_path, Style.RESET_ALL
        )

    def do_show(self, arg):
        if self.module is None:
            logger.warning("Please select a module first")
            return
        table = Table()
        table.add_column("Key")
        table.add_column("Value")
        table.add_column("Required")

        for key in self.module.options:
            table.add_row(
                key,
                str(self.module.options[key]["value"]),
                str(self.module.options[key]["required"]),
            )
        Console().print(table)

    def do_set(self, arg):
        "set an option for the selected module"
        if self.module is None:
            logger.warning("Please select a module first")
            return
        key = arg.split()[0]
        value = arg.split()[1]
        if key not in self.module.options:
            logger.error("Option does not exist")
            return
        self.module.options[key]["value"] = value


    def do_run(self,arg):
        self.module.run()

    def do_exploit(self,arg):
        self.module.run()

    def do_info(self, arg):
        if self.module is None:
            logger.warning("Please select a module first")
            return
        self.module.info()

    def do_clear(self, arg):
        try:
            os.system("clear")
        except:
            os.system("cls")

    def do_version(self,arg):
        "version info"
        version_path = pathlib.Path.cwd() / "VERSION"
        with open(version_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            version = lines[0]
            print(version)

    def do_exit(self, arg):
        "exit the Phoenix shell"
        sys.exit(1)
    def do_quit(self, arg):
        "exit the Phoenix shell"
        sys.exit(1)
    def do_EOF(self, arg):
        sys.exit(1)

    def do_search(self,arg):
        search_path = pathlib.Path.cwd() / "modules"
        for root,dirs,files in os.walk(search_path):
            for name in files:
                name_list = []
                name_list.append(root)
                name_list.append(name)
                str ='/'
                string_list = str.join(name_list)
                #print(string_list)
                
                if arg in string_list:
                    print("\033[32m[STATUS] Already Found\033[0m")
                    pass

                    
                    

        
def main():
    colorama.init()
    logger.remove(0)
    logger.add(sys.stderr, colorize=True, format="<level>{level}: {message}</level>")
    while True:
        try:
            PhoenixShell().cmdloop()
        except KeyboardInterrupt:
            print()
            logger.warning("Please use EOF or the exit/quit commands to exit")
        except Exception:
            raise
if __name__ == "__main__":
    main()
