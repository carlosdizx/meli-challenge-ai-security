from dataclasses import dataclass
from typing import Dict, Any
import ipaddress


# --- helpers de validación estricta ---
def _require(data: Dict[str, Any], key: str):
    if key not in data:
        raise ValueError(f"Falta el campo requerido: '{key}'")
    return data[key]


def _parse_ip(v) -> int:
    try:
        return int(ipaddress.ip_address(str(v)))
    except Exception as e:
        raise ValueError(f"IP inválida: {v}") from e


def _parse_str(v, key: str) -> str:
    if v is None:
        raise ValueError(f"'{key}' no puede ser None")
    s = str(v).strip()
    if s == "":
        raise ValueError(f"'{key}' no puede estar vacío")
    return s


def _parse_int(v, key: str) -> int:
    try:
        return int(v)
    except Exception as e:
        raise ValueError(f"'{key}' debe ser un entero. Valor: {v}") from e


def _parse_bool_strict(v, key: str) -> bool:
    # Acepta solo: True/False (bool) o 1/0 (int/str)
    if isinstance(v, bool):
        return v
    if isinstance(v, int):
        if v in (0, 1):
            return bool(v)
        raise ValueError(f"'{key}' debe ser 0/1 o booleano. Valor: {v}")
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ("0", "1"):
            return s == "1"
        if s in ("true", "false"):
            return s == "true"
    raise ValueError(f"'{key}' debe ser 0/1 o booleano. Valor: {v}")


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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEntry":
        # Campos requeridos (del dataset que estás usando)
        ip_addr = _parse_ip(_require(data, "IP Address"))
        country = _parse_str(_require(data, "Country"), "Country")
        asn = _parse_int(_require(data, "ASN"), "ASN")
        ua = _parse_str(_require(data, "User Agent String"), "User Agent String")
        br = _parse_str(_require(data, "Browser Name and Version"), "Browser Name and Version")
        os_ = _parse_str(_require(data, "OS Name and Version"), "OS Name and Version")
        device = _parse_str(_require(data, "Device Type"), "Device Type")
        login_ok = _parse_bool_strict(_require(data, "Login Successful"), "Login Successful")
        atk_ip = _parse_bool_strict(_require(data, "Is Attack IP"), "Is Attack IP")
        ato = _parse_bool_strict(_require(data, "Is Account Takeover"), "Is Account Takeover")

        return cls(
            ip_address=ip_addr,
            country=country,
            asn=asn,
            user_agent_string=ua,
            browser_name_and_version=br,
            os_name_and_version=os_,
            device_type=device,
            login_successful=login_ok,
            is_attack_ip=atk_ip,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ip_address": self.ip_address,
            "country": self.country,
            "asn": self.asn,
            "user_agent_string": self.user_agent_string,
            "browser_name_and_version": self.browser_name_and_version,
            "os_name_and_version": self.os_name_and_version,
            "device_type": self.device_type,
            # Exporta booleanos como 0/1 para ML downstream:
            "login_successful": 1 if self.login_successful else 0,
            "is_attack_ip": 1 if self.is_attack_ip else 0,
        }
