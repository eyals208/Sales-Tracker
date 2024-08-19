from dataclasses import dataclass, field
from datetime import datetime, date


@dataclass
class Sale:
    _id : str
    product : str
    cost : float
    date : str
    upload_time : str
    customer : str = ""


@dataclass
class user_data:
    _id : str
    name : str
    password : str
    email : str
    sales : list[str] = field(default_factory=list)
