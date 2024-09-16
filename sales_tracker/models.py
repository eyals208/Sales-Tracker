from dataclasses import dataclass, field
from datetime import datetime, date


@dataclass
class Sale:
    _id : str
    product : str
    price : float
    date : datetime
    upload_time : datetime
    customer : str = ""
    details :str = ""


@dataclass
class user_data:
    _id : str
    name : str
    password : str
    email : str
    sales : list[str] = field(default_factory=list)
