import sys, importlib, pathlib
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).parent / "해설"))
from mock_render import render
for r in sys.argv[1:]:
    m = importlib.import_module(f"mock{r}")
    try:
        ex = importlib.import_module(f"expl_{r}").EXPL
    except ModuleNotFoundError:
        ex = {}
    for it in m.ITEMS:
        it["expl"] = ex.get((it["part"], it["no"]), [])
    print(render(m.ITEMS, r, f"화학교육론_실전모의고사_{r}회"))
