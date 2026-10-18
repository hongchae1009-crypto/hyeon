import sys, importlib, pathlib
sys.dont_write_bytecode = True
from mock_render import render
for r in sys.argv[1:]:
    m = importlib.import_module(f"mock{r}")
    print(render(m.ITEMS, r, f"화학교육론_실전모의고사_{r}회"))
