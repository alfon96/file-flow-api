from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum


class FilterEnum(str, Enum):
    _1977 = "_1977"
    aden = "aden"
    brannan = "brannan"
    brooklyn = "brooklyn"
    clarendon = "clarendon"
    earlybird = "earlybird"
    gingham = "gingham"
    hudson = "hudson"
    inkwell = "inkwell"
    kelvin = "kelvin"
    lark = "lark"
    lofi = "lofi"
    maven = "maven"
    mayfair = "mayfair"
    moon = "moon"
    nashville = "nashville"
    perpetua = "perpetua"
    reyes = "reyes"
    rise = "rise"
    slumber = "slumber"
    stinson = "stinson"
    toaster = "toaster"
    valencia = "valencia"
    walden = "walden"
    willow = "willow"
    xpro2 = "xpro2"


class ImageBase(BaseModel):
    id: str


class ImageUploadResponse(ImageBase):
    filename: str


class ImageResize(ImageBase):
    width: int = Field(..., ge=0)
    height: int = Field(..., ge=0)


class ImageScale(ImageBase):
    factor: float = Field(..., ge=0, le=200.0)


class ImageFilter(BaseModel):
    filter_name: FilterEnum
