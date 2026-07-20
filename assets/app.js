/* Shared helpers for the study log site. */

const WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri"];

async function loadLog() {
  const res = await fetch("data/log.json", { cache: "no-store" });
  if (!res.ok) return [];
  const entries = await res.json();
  // Index by date for quick lookup.
  const byDate = {};
  for (const e of entries) byDate[e.date] = e;
  return { entries, byDate };
}

function parseISO(dateStr) {
  const [y, m, d] = dateStr.split("-").map(Number);
  return new Date(y, m - 1, d);
}

function toISO(date) {
  const p = (n) => String(n).padStart(2, "0");
  return `${date.getFullYear()}-${p(date.getMonth() + 1)}-${p(date.getDate())}`;
}

/* Level 0-4 from hours studied, mirroring GitHub's intensity scale. */
function intensityLevel(entry) {
  if (!entry) return 0;
  const h = entry.hours || 0;
  if (h >= 5) return 4;
  if (h >= 4) return 3;
  if (h >= 2) return 2;
  return 1;
}

/* Render the Mon-Fri streak grid into `container`.
   Columns are weeks (oldest → newest), rows are Mon..Fri. */
function renderTimeline(container, byDate, startDateStr) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Show from the first logged day, clamped to the trailing 52 weeks.
  const minStart = new Date(today.getTime() - 52 * 7 * 86400000);
  let start = startDateStr ? parseISO(startDateStr) : new Date(today.getTime() - 25 * 7 * 86400000);
  if (start < minStart) start = minStart;
  // Snap start back to its Monday.
  const startMonday = new Date(start);
  const dow = (startMonday.getDay() + 6) % 7; // Mon=0 .. Sun=6
  startMonday.setDate(startMonday.getDate() - dow);

  const weeks = [];
  let cursor = new Date(startMonday);
  while (cursor <= today) {
    const week = [];
    for (let i = 0; i < 5; i++) {
      week.push(new Date(cursor.getTime() + i * 86400000));
    }
    weeks.push(week);
    cursor = new Date(cursor.getTime() + 7 * 86400000);
  }

  const grid = document.createElement("div");
  grid.className = "timeline";
  grid.style.gridTemplateRows = `auto repeat(5, 15px)`;

  // Row labels column (spacer aligns with the month-label row).
  const spacer = document.createElement("div");
  spacer.className = "month-label";
  grid.appendChild(spacer);
  for (const label of WEEKDAY_LABELS) {
    const el = document.createElement("div");
    el.className = "day-label";
    el.textContent = label;
    grid.appendChild(el);
  }

  let lastMonth = -1;
  for (const week of weeks) {
    const monthEl = document.createElement("div");
    monthEl.className = "month-label";
    const m = week[0].getMonth();
    if (m !== lastMonth) {
      monthEl.textContent = week[0].toLocaleString("en", { month: "short" });
      lastMonth = m;
    }
    grid.appendChild(monthEl);

    for (const day of week) {
      const iso = toISO(day);
      const entry = byDate[iso];
      const level = intensityLevel(entry);
      const dot = document.createElement("span");
      dot.className = "dot" + (level ? ` l${level}` : "") + (day > today ? " future" : "");
      dot.title = iso + (entry ? ` — ${entry.summary || "session logged"}` : "");

      if (entry) {
        const link = document.createElement("a");
        link.className = "dot-link";
        link.href = `day.html?date=${iso}`;
        link.appendChild(dot);
        grid.appendChild(link);
      } else {
        grid.appendChild(dot);
      }
    }
  }

  container.innerHTML = "";
  container.appendChild(grid);
}

/* Streak math over weekdays only: a streak continues as long as every
   weekday has an entry; weekends never break it. */
function computeStreaks(byDate) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  let current = 0;
  const cursor = new Date(today);
  // Today only counts if logged; start from today if logged, else yesterday.
  if (!byDate[toISO(cursor)]) cursor.setDate(cursor.getDate() - 1);
  while (true) {
    const dow = (cursor.getDay() + 6) % 7;
    if (dow >= 5) {
      cursor.setDate(cursor.getDate() - 1);
      continue;
    }
    if (byDate[toISO(cursor)]) {
      current++;
      cursor.setDate(cursor.getDate() - 1);
    } else break;
  }

  // Longest streak across all entries.
  const dates = Object.keys(byDate).sort();
  let longest = 0, run = 0, prev = null;
  for (const d of dates) {
    if (prev === null) run = 1;
    else {
      // Count weekdays between prev and d, exclusive.
      let gap = 0;
      const c = new Date(parseISO(prev).getTime() + 86400000);
      const end = parseISO(d);
      while (c < end) {
        const dow = (c.getDay() + 6) % 7;
        if (dow < 5) gap++;
        c.setDate(c.getDate() + 1);
      }
      run = gap === 0 ? run + 1 : 1;
    }
    longest = Math.max(longest, run);
    prev = d;
  }

  return { current, longest, total: dates.length };
}

async function renderNoteInto(el, notePath) {
  const res = await fetch(notePath, { cache: "no-store" });
  if (!res.ok) {
    el.innerHTML = '<p class="empty-state">No notes found for this day.</p>';
    return null;
  }
  let md = await res.text();
  // Strip YAML frontmatter if present.
  let frontmatter = {};
  const fm = md.match(/^---\n([\s\S]*?)\n---\n/);
  if (fm) {
    md = md.slice(fm[0].length);
    for (const line of fm[1].split("\n")) {
      const idx = line.indexOf(":");
      if (idx > 0) frontmatter[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
    }
  }
  el.innerHTML = marked.parse(md);
  return frontmatter;
}
