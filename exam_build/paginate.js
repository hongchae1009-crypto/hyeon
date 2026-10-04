// 브라우저에서 실행: #pool 안의 .q 블록을 2단 A4 페이지에 순서대로 배치한다.
(function () {
  const pool = document.getElementById('pool');
  if (!pool) return;
  const sets = JSON.parse(pool.dataset.sets);           // [{id,title,subtitle,count,points,time}]
  const out = document.getElementById('book');
  const mm = v => v * 96 / 25.4;
  sets.forEach(set => {
    const qs = Array.from(pool.querySelectorAll(`.q[data-set="${set.id}"]`));
    let pages = [], page, cols, ci;
    const newPage = first => {
      page = document.createElement('div'); page.className = 'page';
      if (first) page.innerHTML = document.getElementById('cover-' + set.id).innerHTML;
      const c = document.createElement('div'); c.className = 'cols ' + (first ? 'first' : 'rest');
      c.innerHTML = '<div class="col"></div><div class="col"></div>';
      page.appendChild(c);
      const f = document.createElement('div'); f.className = 'foot'; page.appendChild(f);
      out.appendChild(page); pages.push(page);
      cols = c.querySelectorAll('.col'); ci = 0;
    };
    newPage(true);
    qs.forEach(q => {
      for (;;) {
        const col = cols[ci];
        col.appendChild(q);
        if (col.scrollHeight <= col.clientHeight + 1 || col.children.length === 1) {
          if (col.scrollHeight > col.clientHeight + 1) q.classList.add('overflow');
          break;
        }
        col.removeChild(q);
        if (ci === 0) ci = 1; else newPage(false);
      }
    });
    const last = cols[ci];
    const end = document.createElement('div'); end.className = 'end'; end.textContent = '<수고하셨습니다.>';
    last.appendChild(end);
    if (last.scrollHeight > last.clientHeight + 1) { last.removeChild(end); }
    pages.forEach((p, i) => {
      p.querySelector('.foot').innerHTML =
        `<span class="tag">${set.tag}</span>화 학 [${set.label}] (${pages.length}면 중 <b>${i + 1}</b> 면)`;
    });
  });
  pool.remove();
  document.body.dataset.ready = '1';
})();
