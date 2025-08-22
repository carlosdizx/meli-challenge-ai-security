from dataclasses import dataclass
from typing import Dict, Any, Iterable, List

# -----------------------------
# Alias de claves aceptadas
# -----------------------------
KEY_ALIASES: Dict[str, list[str]] = {
    "country": ["country", "Country"],
    "asn": ["asn", "ASN"],
    "user_agent_string": ["user_agent_string", "User Agent String"],
    "browser_name_and_version": ["browser_name_and_version", "Browser Name and Version"],
    "os_name_and_version": ["os_name_and_version", "OS Name and Version"],
    "device_type": ["device_type", "Device Type"],
    "login_successful": ["login_successful", "Login Successful"],
}


def _get_required(data: Dict[str, Any], canon_key: str):
    aliases = KEY_ALIASES.get(canon_key, [canon_key])
    for k in aliases:
        if k in data:
            return data[k]
    raise ValueError(f"Falta el campo requerido: '{canon_key}' (aceptados: {aliases})")


# --- helpers de validación estricta ---
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
    country: str
    asn: int
    user_agent_string: str
    browser_name_and_version: str
    os_name_and_version: str
    device_type: str
    login_successful: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEntry":
        country = _parse_str(_get_required(data, "country"), "country")
        asn = _parse_int(_get_required(data, "asn"), "asn")
        ua = _parse_str(_get_required(data, "user_agent_string"), "user_agent_string")
        br = _parse_str(_get_required(data, "browser_name_and_version"), "browser_name_and_version")
        os_ = _parse_str(_get_required(data, "os_name_and_version"), "os_name_and_version")
        device = _parse_str(_get_required(data, "device_type"), "device_type")
        login_ok = _parse_bool_strict(_get_required(data, "login_successful"), "login_successful")

        return cls(
            country=country,
            asn=asn,
            user_agent_string=ua,
            browser_name_and_version=br,
            os_name_and_version=os_,
            device_type=device,
            login_successful=login_ok,
        )

    @classmethod
    def from_external(cls, data: Dict[str, Any]) -> "LogEntry":
        return cls.from_dict(data)

    @classmethod
    def ensure(cls, obj: Any) -> "LogEntry":
        if isinstance(obj, LogEntry):
            return obj
        if isinstance(obj, dict):
            return cls.from_external(obj)
        raise TypeError(f"No se puede convertir a LogEntry: tipo {type(obj)}")

    @classmethod
    def parse_list(cls, payload: Iterable[Any]) -> List["LogEntry"]:
        if not isinstance(payload, Iterable):
            raise TypeError("parse_list requiere un iterable (lista) de items")
        result: List[LogEntry] = []
        for i, item in enumerate(payload):
            try:
                result.append(cls.ensure(item))
            except Exception as e:
                raise ValueError(f"Registro {i}: {e}") from e
        return result

    def to_dict(self) -> Dict[str, Any]:
        # Exporta en snake_case, con enteros/códigos para booleans (1/0)
        return {
            "country": self.country,
            "asn": self.asn,
            "user_agent_string": self.user_agent_string,
            "browser_name_and_version": self.browser_name_and_version,
            "os_name_and_version": self.os_name_and_version,
            "device_type": self.device_type,
            "login_successful": 1 if self.login_successful else 0,
        }
