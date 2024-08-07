from dataclasses import dataclass, field
from datetime import datetime, date


@dataclass
class Sale:
    _id : str
    product : str
    cost : float
    customer : str = ""
    date : date
    upload_time : datetime


@dataclass
class user_data:
    name : str
    password : str
    email : str
    sales : list[Sale] = field(default_factory=list)
