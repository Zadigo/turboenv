from typing import TYPE_CHECKING, Any, Type
    
if TYPE_CHECKING:
    from turboenv.main import TurboEnv

type TypeAny = str | bool | float | list[str] | dict[str, Any] | None

type TypeCast[T = str | int | float] = Type[T]

type TypeTurboEnv  = 'TurboEnv'
