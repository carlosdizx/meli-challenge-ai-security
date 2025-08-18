from dataclasses import dataclass


@dataclass
class LogEntry:
    ip_address: int
    country: str
    asn: int
    user_agent_string: str
    browser_name_and_version: str
    os_name_and_version: str
    device_type: str
    login_successful: bool
    is_attack_ip: bool

    # is_account_takeover: bool

    @classmethod
    def from_dict(cls, data: dict) -> 'LogEntry':
        return cls(
            ip_address=int(data.get('IP Address', 0)),
            country=data.get('Country', ''),
            asn=int(data.get('ASN', 0)),
            user_agent_string=data.get('User Agent String', ''),
            browser_name_and_version=data.get('Browser Name and Version', ''),
            os_name_and_version=data.get('OS Name and Version', ''),
            device_type=data.get('Device Type', ''),
            login_successful=bool(data.get('Login Successful', False)),
            is_attack_ip=bool(data.get('Is Attack IP', False)),
            # is_account_takeover=bool(data.get('Is Account Takeover', False))
        )

    def to_dict(self) -> dict:
        return {
            'ip_address': self.ip_address,
            'country': self.country,
            'asn': self.asn,
            'user_agent_string': self.user_agent_string,
            'browser_name_and_version': self.browser_name_and_version,
            'os_name_and_version': self.os_name_and_version,
            'device_type': self.device_type,
            'login_successful': self.login_successful,
            'is_attack_ip': self.is_attack_ip,
            # 'is_account_takeover': self.is_account_takeover
        }
