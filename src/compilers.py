import json

def buildC(code: str) -> str:
    data = {
            "code": code,
            "compiler": "gcc-head"
        }
    return json.dumps(data)


def buildBash(code: str) -> str:
    data = {
            "code": code,
            "compiler": "bash"
        }
    return json.dumps(data)


def buildCSharp(code: str) -> str:
    data = {
            "code": code,
            "compiler": "mono-head"
        }
    return json.dumps(data)


def buildGo(code: str) -> str:
    data = {
            "code": code,
            "compiler": "golang-head"
        }
    return json.dumps(data)


def buildHaskell(code: str) -> str:
    data = {
            "code": code,
            "compiler": "ghc-head"
        }
    return json.dumps(data)


def buildJulia(code: str) -> str:
    data = {
            "code": code,
            "compiler": "julia-head"
        }
    return json.dumps(data)


def buildLua(code: str) -> str:
    data = {
            "code": code,
            "compiler": "lua-head"
        }
    return json.dumps(data)


def buildPascal(code: str) -> str:
    data = {
            "code": code,
            "compiler": "fpc-head"
        }
    return json.dumps(data)


def buildPerl(code: str) -> str:
    data = {
            "code": code,
            "compiler": "perl-head"
        }
    return json.dumps(data)


def buildR(code: str) -> str:
    data = {
            "code": code,
            "compiler": "r-head"
        }
    return json.dumps(data)


def buildRuby(code: str) -> str:
    data = {
            "code": code,
            "compiler": "ruby-head"
        }
    return json.dumps(data)


def buildCPP(code: str) -> str:
    data = {
            "code": code,
            "options": "warning,gnu++1y",
            "compiler": "gcc-head"
        }
    return json.dumps(data)


def buildTS(code: str) -> str:
    data = {
            "code": code,
            "compiler": "typescript-3.9.5"
        }
    return json.dumps(data)


def buildRust(code: str) -> str:
    data = {
            "code": code,
            "compiler": "rust-head"
        }
    return json.dumps(data)


def buildPython(code: str) -> str:
    data = {
            "code": code,
            "compiler": "cpython-head"
        }
    return json.dumps(data)


def buildPHP(code: str) -> str:
    data = {
            "code": code,
            "compiler": "php-head"
        }
    return json.dumps(data)


def buildJS(code: str) -> str:
    data = {
            "code": code,
            "compiler": "nodejs-head"
        }
    return json.dumps(data)


def buildJava(code: str) -> str:
    data = {
            "code": code,
            "compiler": "openjdk-head"
        }
    return json.dumps(data)