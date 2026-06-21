from os import path
import yaml

class Status :
    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(Status, self).__new__(self)
        return self._instance

    def __init__(self) -> None :
        with open(path.expanduser("~/.config/qtile/saved_status.yml")) as f:
            data = yaml.safe_load(f)
        
        self.username = data["username"]
        self.vpn = data["vpn"]

    def save(self):
        with open(path.expanduser("~/.config/qtile/saved_status.yml"), "w") as f:
            yaml.dump({
                "username": self.username,
                "vpn": self.vpn
                }, f)
    
    def is_vpn_on(self):
        return self.vpn