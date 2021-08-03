import requests
import json
import os
import sys
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
        table.add_row("whatcms","CMS recognition","-")
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
            url = "http://" + self.options["url"]["value"]
            cms_tmp = os.popen('curl -s -G https://whatcms.org/API/CMS \
            --data-urlencode key="5926b162fde6d3da25520ef5dc0512f8556e637009b72aed3b7576c527766c487a3510" \
            --data-urlencode url="%s"'%(url)).read()
            cms = json.loads(cms_tmp)
            print("\033[32m[CMS]\033[0m",cms['result']['name'])
        else:
            url = self.options["url"]["value"]

