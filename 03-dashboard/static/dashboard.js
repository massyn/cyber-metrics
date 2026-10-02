// Scorecard rows open the metric's detail page; filter drop-downs apply as soon as they change.
document.querySelectorAll('.clickable-row').forEach((row) => {
  row.addEventListener('click', (event) => {
    if (!event.target.closest('a')) {
      window.location = row.dataset.href;
    }
  });
});

document.querySelectorAll('select[data-autosubmit]').forEach((select) => {
  select.addEventListener('change', () => select.form.submit());
});

const scorecard = document.getElementById('scorecard-table');
if (scorecard) {
  const statusClasses = JSON.parse(scorecard.dataset.statusClasses);
  const statusLabels = JSON.parse(scorecard.dataset.statusLabels);
  const rows = [...scorecard.querySelectorAll('tbody tr[data-score-url]')];
  const progress = document.getElementById('score-progress');
  const summary = document.getElementById('summary');
  const percent = (value) => (value === null ? '—' : `${(value * 100).toFixed(1)}%`);
  let loaded = 0;

  // Fill in one row from its score endpoint.
  const loadScore = async (row) => {
    const scoreCell = row.querySelector('[data-cell="score"]');
    try {
      const response = await fetch(row.dataset.scoreUrl);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const result = await response.json();
      scoreCell.innerHTML = '';
      const badge = document.createElement('span');
      badge.className = `badge text-bg-${statusClasses[result.status]} score-badge`;
      badge.title = statusLabels[result.status];
      badge.textContent = percent(result.value);
      scoreCell.appendChild(badge);
      row.querySelector('[data-cell="total"]').textContent = result.total.toLocaleString();
      const note = row.querySelector('[data-cell="note"]');
      note.textContent = result.note;
      note.classList.toggle('text-danger', result.has_errors);
      row.dataset.sortTotal = result.total;
      row.dataset.sortScore = result.value === null ? '' : result.value;
      row.classList.toggle('d-none', !result.visible);
    } catch (error) {
      scoreCell.innerHTML = '<span class="badge text-bg-danger score-badge">Error</span>';
      console.error(`Could not load ${row.dataset.scoreUrl}`, error);
    }
    loaded += 1;
    if (progress) {
      progress.textContent = `${loaded} of ${rows.length}`;
    }
  };

  // A few at a time, so the server isn't asked to run every metric at once.
  const loadAll = async (concurrency) => {
    const queue = [...rows];
    const worker = async () => {
      while (queue.length) {
        await loadScore(queue.shift());
      }
    };
    await Promise.all(Array.from({ length: concurrency }, worker));
  };

  loadAll(4).then(async () => {
    const empty = document.getElementById('no-metrics');
    empty.classList.toggle('d-none', rows.some((row) => !row.classList.contains('d-none')));
    const response = await fetch(summary.dataset.summaryUrl);
    summary.innerHTML = response.ok
      ? await response.text()
      : '<div class="alert alert-danger">Could not load the summary.</div>';
  });

  // Sortable columns: click a header to sort, click again to reverse.
  const tbody = scorecard.querySelector('tbody');
  scorecard.querySelectorAll('th.sortable').forEach((header) => {
    header.addEventListener('click', () => {
      const key = `sort${header.dataset.sortKey[0].toUpperCase()}${header.dataset.sortKey.slice(1)}`;
      const numeric = header.dataset.sortType === 'number';
      const descending = header.dataset.order === 'asc';
      scorecard.querySelectorAll('th.sortable').forEach((th) => delete th.dataset.order);
      header.dataset.order = descending ? 'desc' : 'asc';

      const value = (row) => row.dataset[key] ?? '';
      rows.sort((a, b) => {
        const [x, y] = [value(a), value(b)];
        // rows without a value (e.g. no data) always sort last
        if (x === '' || y === '') {
          return (x === '') - (y === '');
        }
        const order = numeric ? Number(x) - Number(y) : x.localeCompare(y);
        return descending ? -order : order;
      });
      rows.forEach((row) => tbody.insertBefore(row, document.getElementById('no-metrics')));
    });
  });
}
