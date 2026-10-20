# 미래엔 교사용 교과서(글자 벡터화)에서 적갈색(교사용) 채움·선 도형만 지운 뒤 렌더링
import pymupdf, re, sys
REDS = [(0.668, 0.203, 0.066), (0.746, 0.383, 0.23)]
def is_red(v): return len(v) == 3 and any(all(abs(a - b) < 0.012 for a, b in zip(v, R)) for R in REDS)
PAINT_FILL = {b"f", b"F", b"f*"}; PAINT_STROKE = {b"S", b"s"}; PAINT_BOTH = {b"B", b"B*", b"b", b"b*"}
def strip(stream):
    out = []; fill = stroke = (0, 0, 0); stack = []
    for line in stream.split(b"\n"):
        t = line.split()
        if not t or len(t) > 8: out.append(line); continue
        try: [float(x) for x in t[:-1]]
        except ValueError: out.append(line); continue
        op = t[-1]
        if op == b"q": stack.append((fill, stroke))
        elif op == b"Q" and stack: fill, stroke = stack.pop()
        elif op == b"rg" and len(t) == 4: fill = tuple(float(x) for x in t[:3])
        elif op == b"RG" and len(t) == 4: stroke = tuple(float(x) for x in t[:3])
        elif op == b"g" and len(t) == 2: fill = (float(t[0]),) * 3
        elif op == b"G" and len(t) == 2: stroke = (float(t[0]),) * 3
        if len(t) == 1 and op in PAINT_FILL and is_red(fill): line = b"n"
        elif len(t) == 1 and op in PAINT_STROKE and is_red(stroke): line = b"n"
        elif len(t) == 1 and op in PAINT_BOTH:
            rf, rs = is_red(fill), is_red(stroke)
            if rf and rs: line = b"n"
            elif rf: line = b"S" if op in (b"B", b"B*") else b"s"
            elif rs: line = b"f" if op in (b"B", b"b") else b"f*"
        out.append(line)
    return b"\n".join(out)
if __name__ == "__main__":
    src, pn, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    clip = [float(x) for x in sys.argv[4:8]] if len(sys.argv) >= 8 else None
    d = pymupdf.open(src); p = d[pn - 1]
    xs = p.get_contents(); s = b"\n".join(d.xref_stream(x) for x in xs)
    d.update_stream(xs[0], strip(s))
    for x in xs[1:]: d.update_stream(x, b"")
    pix = p.get_pixmap(dpi=200, clip=pymupdf.Rect(*clip) if clip else None)
    pix.save(out); print(out, pix.width, pix.height)
