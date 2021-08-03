import sys
import os
from rich.console import Console
from rich.table import Table

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.options = {
            "url": {"value": None, "required": True},
        }
    
    def info(self):
        console = Console()
        table = Table()
        table.add_column("Author")
        table.add_column("Scanner description")
        table.add_column("Other")
        table.add_row("BaCde","RapidDNS","-")
        console.print(table)       

    def run(self):
        for key in self.options:
            if (
                self.options[key]["value"] is None
                and self.options[key]["required"] is True
            ):
                self.logger.error("Required key {} is not set".format(key))
                return

        if not self.options["url"]["value"].startswith("http"):
            url =  self.options["url"]["value"]
            print("\033[32m[Domain]\033[0m",url)
            #url = sys.argv[1]
            subdomain = os.popen('''
            curl -s "https://rapiddns.io/subdomain/%s?full=1" | grep -oP '_blank">\K[^<]*' | grep -v http | sort -u
            ''' %(url)).read()
            print(subdomain)