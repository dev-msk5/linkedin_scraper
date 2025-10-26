document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('jobTitle');
  const btn = document.getElementById('searchBtn');
  const list = document.getElementById('list');
  const chart = document.getElementById('chart');
  const meta = document.getElementById('meta');

  // Helper to set a lightweight loading state
  function setLoading(loading) {
    btn.disabled = loading;
    btn.textContent = loading ? 'Searching…' : 'Search';
  }

  async function doSearch() {
    const role = input.value.trim();
    if (!role) {
      // show a subtle inline message instead of alert
      list.innerHTML = '<div class="no-results">Please enter a job title to search.</div>';
      chart.innerHTML = '';
      meta.textContent = '';
      return;
    }

    const url = `/api/skills?role=${encodeURIComponent(role)}`;
    setLoading(true);
    list.innerHTML = '';
    chart.innerHTML = '';
    meta.textContent = 'Searching...';

    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();
      renderResults(data);
    } catch (err) {
      console.error(err);
      list.innerHTML = '';
      chart.innerHTML = `<div class="no-results">Error fetching results: ${err.message}</div>`;
      meta.textContent = '';
    } finally {
      setLoading(false);
    }
  }

  btn.addEventListener('click', doSearch);
  // allow Enter key to trigger search
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') doSearch();
  });

  function renderResults(data) {
    list.innerHTML = '';
    chart.innerHTML = '';
    meta.textContent = `Jobs matched: ${data.job_count}`;

    const skills = data.skills || {};
    const entries = Object.entries(skills).sort((a, b) => b[1] - a[1]);
    if (entries.length === 0) {
      list.innerHTML = '<div class="no-results">No skills found for this role.</div>';
      return;
    }

    // Render list (skill name + count)
    for (const [skill, count] of entries) {
      const li = document.createElement('li');
      const name = document.createElement('span');
      name.textContent = skill;
      const badge = document.createElement('span');
      badge.textContent = String(count);
      badge.style.opacity = '0.9';
      li.appendChild(name);
      li.appendChild(badge);
      list.appendChild(li);
    }

    // Render simple bars (visualization)
    const max = Math.max(...entries.map((e) => e[1]));
    for (const [skill, count] of entries) {
      const row = document.createElement('div');
      row.className = 'bar-row';
      const label = document.createElement('div');
      label.className = 'bar-label';
      label.textContent = skill;
      const bar = document.createElement('div');
      bar.className = 'bar';
      const fill = document.createElement('div');
      fill.className = 'fill';
      const pct = max ? Math.round((count / max) * 100) : 0;
      fill.style.width = pct + '%';
      bar.appendChild(fill);
      const countBadge = document.createElement('div');
      countBadge.style.width = '40px';
      countBadge.style.textAlign = 'right';
      countBadge.textContent = count;
      row.appendChild(label);
      row.appendChild(bar);
      row.appendChild(countBadge);
      chart.appendChild(row);
    }
  }
});
