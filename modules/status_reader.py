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
        self.last_incident_date = data.get("last_incident_date")
        self.last_boot_id = data.get("last_boot_id")


    def save(self):
        with open(path.expanduser("~/.config/qtile/saved_status.yml"), "w") as f:
            yaml.dump({
                "username": self.username,
                "vpn": self.vpn,
                "last_incident_date": self.last_incident_date,
                "last_boot_id": self.last_boot_id,
                }, f)
    
    def is_vpn_on(self):
        return self.vpn