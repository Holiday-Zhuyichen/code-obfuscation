# coding=utf-8
"""
The core of this code-obfuscation
Licensed under MIT license:
MIT License

Copyright (c) 2025 Holiday-Zhuyichen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Any, Optional
from inspect import getsource


def _warning_undeveloped() -> bool:
    """
    Warns the user the code is not production-ready
    """
    # noinspection PyBroadException
    try:
        from warnings import showwarning as _showwarning
        _showwarning("The code-obfuscation module is not fully developed, it is not production "
                     "ready!", Warning, "<code-obfuscation>", 0)
    except Exception:
        return True
    else:
        return False


def obfuscation_parse(original: str, config: Optional[dict[str, Any]] = None) -> str:
    """
    Parse your code
    """
    if config is None:
        config = {}
    try:
        # noinspection PyStatementEffect
        config["broke-on-re-obfuscation"]
        if not isinstance(config["broke-on-re-obfuscation"], str):
            raise TypeError("broke-on-re-obfuscation requires a str")
        if config["broke-on-re-obfuscation"] not in ("ignore", "error", "warning", "stop"):
            raise ValueError('broke-on-re-obfuscation must in ("ignore","error","warning","stop")')
    except KeyError:
        config["broke-on-re-obfuscation"] = "error"

    if config["broke-on-re-obfuscation"] != "ignore" and original.find("# Git Code Obfuscation") != -1:
        if config["broke-on-re-obfuscation"] == "error":
            raise RecursionError("call obfuscation_parse on already parsed file")
        elif config["broke-on-re-obfuscation"] == "warning":
            from warnings import showwarning
            showwarning("call obfuscation_parse on already parsed file", Warning,
                        "<obfuscation-parse>::<auto-broker>", 0)
        elif config["broke-on-re-obfuscation"] == "stop":
            return original

    pre_code = "# Begin of file\n\n\n"

    # noinspection PyProtectedMember
    from core import _TotalTransform
    # noinspection PyProtectedMember
    pre_code += "\n".join(i.removeprefix(" " * 4) for i in getsource(_TotalTransform._SmartString).split("\n"))
    pre_code += "\n\n# Seperator\n\n"
    # noinspection PyProtectedMember
    pre_code += "\n".join(i.removeprefix(" " * 4).replace("ConstTransform.", "") for i in
                          getsource(_TotalTransform._base_to_decimal).split("\n") if i != "@staticmethod")
    pre_code += "\n\n# Seperator\n\n"
    # noinspection PyProtectedMember
    pre_code += "\n".join(i.removeprefix(" " * 4).replace("ConstTransform.", "") for i in
                          getsource(_TotalTransform._smart_float_ratio).split("\n") if i != "@staticmethod")
    pre_code += "\n\n# Seperator\n\n"
    # noinspection PyProtectedMember
    pre_code += "\n".join(i.removeprefix(" " * 4).replace("ConstTransform.", "") for i in
                          getsource(_TotalTransform._smart_str_unparse).split("\n") if i != "@staticmethod")
    pre_code += "\n\n\n# End of File\n"

    from ast import parse, unparse, fix_missing_locations
    from base64 import b64encode
    tree = parse(original)
    _TotalTransform(config).visit(tree)
    fix_missing_locations(tree)
    pre_write: str = (
        f"# Git Code Obfuscation\nfrom base64 import b64decode as _b64decode\nexec(_b64decode({b64encode(pre_code.encode())!r}).decode())"
        "\n")
    retval = pre_write if original.find(pre_write) == -1 else "\n"
    retval += unparse(tree)
    return retval


if __name__ != "__main__":
    _warning_undeveloped()
else:
    with open("tmp.py", "w", encoding="gbk") as f:
        f.write("# encoding: gbk\n\n")
        tmp = """
# raise Exception(0.166666666666666666666666666666,0.1,0.2,0.3,0.1+0.2)
from time import time
begin=time()
def is_prime(num):
    if num<2: return False
    for i in range(2,num):
        if num%i==0: return False
    return True
from tqdm.rich import trange
for i in trange(0,1024,1):
    if is_prime(i): print(i)
print(1024,-2048)
end=time()
spent=int(round(end-begin))
really=end-begin
raise TimeoutError(f"Spent {spent//3600:02d}:{spent%3600//60:02d}:{really%3600%60:.2f}")
"""
        for _ in range(4):
            tmp = obfuscation_parse(tmp, {"broke-on-re-obfuscation": "warning"})
        f.write(tmp)

    from os import system
    from loguru import logger

    logger.info("End generation")
    assert system("py tmp.py") == 0, "Not py command"
    logger.info("Python Ran")
    # assert system("fc answer.tmp ANSWER > nul") == 0, "Result changed"
    # logger.info("Compare")
    assert system("type tmp.py") == 0, "tmp.py bad"
    logger.info("File content")
