from dataclasses import dataclass


@dataclass
class LogEntry:
    index: int
    country: str
    region: str
    city: str
    device_type: str
    login_successful: bool
    is_attack_ip: bool
    is_account_takeover: bool

    @classmethod
    def from_dict(cls, data: dict) -> 'LogEntry':
        return cls(
            index=int(data.get('index', 0)),
            country=data.get('Country', ''),
            region=data.get('Region', ''),
            city=data.get('City', ''),
            device_type=data.get('Device Type', ''),
            login_successful=bool(data.get('Login Successful', False)),
            is_attack_ip=bool(data.get('Is Attack IP', False)),
            is_account_takeover=bool(data.get('Is Account Takeover', False))
        )

    def to_dict(self) -> dict:
        return {
            'index': self.index,
            'Country': self.country,
            'Region': self.region,
            'City': self.city,
            'Device Type': self.device_type,
            'Login Successful': self.login_successful,
            'Is Attack IP': self.is_attack_ip,
            'Is Account Takeover': self.is_account_takeover
        }
