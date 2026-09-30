// Dark mode toggle (initial theme is already set pre-paint by the inline <head> script)
const themeToggle = document.querySelector('.theme-toggle');
const themeColorMeta = document.querySelector('meta[name="theme-color"]');

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  if (themeColorMeta) {
    themeColorMeta.setAttribute('content', theme === 'dark' ? '#161616' : '#1e3a8a');
  }
  if (themeToggle) {
    themeToggle.setAttribute('aria-pressed', String(theme === 'dark'));
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  }
}

// Sync button state with whatever the head script decided
applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
}

// Follow OS changes only while the user hasn't made an explicit choice
const darkMq = window.matchMedia('(prefers-color-scheme: dark)');
darkMq.addEventListener('change', (e) => {
  let stored = null;
  try { stored = localStorage.getItem('theme'); } catch (err) {}
  if (stored !== 'light' && stored !== 'dark') {
    applyTheme(e.matches ? 'dark' : 'light');
  }
});

// Mobile navigation toggle
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');
if (toggle) {
  const setExpanded = (isExpanded) => {
    toggle.setAttribute('aria-expanded', String(isExpanded));
  };

  const handleResize = () => {
    const isDesktop = window.matchMedia('(min-width: 900px)').matches;
    if (isDesktop) {
      links?.classList.remove('open');
      setExpanded(false);
      return;
    }
    setExpanded(links?.classList.contains('open'));
  };

  toggle.addEventListener('click', () => {
    links?.classList.toggle('open');
    setExpanded(links?.classList.contains('open'));
  });

  window.addEventListener('resize', handleResize);
  window.addEventListener('load', handleResize);
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) {
      e.preventDefault();
      const header = document.querySelector('.site-header');
      const headerOffset = header ? header.offsetHeight : 0;
      const elementPosition = el.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
      
      links?.classList.remove('open');
      toggle?.setAttribute('aria-expanded', 'false');
    }
  });
});

// Active section highlighting in navigation
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

function updateActiveNav() {
  const scrollPos = window.scrollY + 100; // Offset for better UX
  
  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.offsetHeight;
    const sectionId = section.getAttribute('id');
    
    if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${sectionId}`) {
          link.classList.add('active');
        }
      });
    }
  });
}

// Update on scroll
window.addEventListener('scroll', updateActiveNav);
// Update on load
window.addEventListener('load', updateActiveNav);

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
  if (links && links.classList.contains('open')) {
    if (!e.target.closest('.nav-links') && !e.target.closest('.nav-toggle')) {
      links.classList.remove('open');
      toggle?.setAttribute('aria-expanded', 'false');
    }
  }
});

// Footer year
document.getElementById('year').textContent = new Date().getFullYear();


document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('[data-scroll]');

  cards.forEach(card => {
    const scroller = card.querySelector('.scroll-body');
    if (!scroller) return;

    const update = () => {
      const { scrollTop, scrollHeight, clientHeight } = scroller;
      const atTop = scrollTop <= 0;
      const atBottom = Math.ceil(scrollTop + clientHeight) >= scrollHeight;

      // mark whether it actually overflows
      const isScrollable = scrollHeight > clientHeight + 1;
      card.classList.toggle('is-scrollable', isScrollable);

      card.classList.toggle('at-top', atTop);
      card.classList.toggle('at-bottom', atBottom);
      if (scrollTop > 2) card.classList.add('scrolled');
    };

    scroller.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update(); // initial
  });

  // Fade in lazy-loaded images when they finish loading
  document.querySelectorAll('img.lazy-img').forEach(img => {
    if (img.complete) {
      img.classList.add('is-loaded');
      return;
    }
    img.addEventListener('load', () => img.classList.add('is-loaded'), { once: true });
  });
});

/* ---------------------------------------------------------------- search */
(function () {
  var input = document.getElementById('site-search');
  var panel = document.getElementById('search-results');
  if (!input || !panel) return;
  var base = input.getAttribute('data-base') || '';
  var data = null, loading = false, sel = -1, rows = [];

  function load() {
    if (data || loading) return Promise.resolve(data);
    loading = true;
    return fetch(base + 'search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (j) { data = j; loading = false; return j; })
      .catch(function () { loading = false; data = []; return data; });
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function mark(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) {
      if (t.length < 2) return;
      out = out.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>');
    });
    return out;
  }
  function score(it, terms) {
    var t = it.t.toLowerCase(), d = (it.d || '').toLowerCase(), s = (it.s || '').toLowerCase(), tot = 0;
    for (var i = 0; i < terms.length; i++) {
      var q = terms[i], hit = 0;
      if (t.indexOf(q) === 0) hit += 60; else if (t.indexOf(q) > -1) hit += 40;
      if (d.indexOf(q) > -1) hit += 12;
      if (s.indexOf(q) > -1) hit += 6;
      if (!hit) return 0;
      tot += hit;
    }
    return tot;
  }
  function render(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { panel.hidden = true; rows = []; return; }
    rows = (data || []).map(function (it) { return { it: it, sc: score(it, terms) }; })
      .filter(function (r) { return r.sc > 0; })
      .sort(function (a, b) { return b.sc - a.sc; }).slice(0, 8);
    panel.innerHTML = rows.length
      ? rows.map(function (r, i) {
          return '<a href="' + base + r.it.u + '" data-i="' + i + '">' +
                 '<span class="sr-title">' + mark(r.it.t, terms) + '</span>' +
                 '<span class="sr-kind">' + esc(r.it.k) + '</span>' +
                 '<span class="sr-desc">' + mark(r.it.d || '', terms) + '</span></a>';
        }).join('')
      : '<div class="sr-empty">No matches for &ldquo;' + esc(q) + '&rdquo;</div>';
    sel = -1; panel.hidden = false;
  }
  function highlight() {
    var links = panel.querySelectorAll('a');
    for (var i = 0; i < links.length; i++) links[i].classList.toggle('sel', i === sel);
    if (sel >= 0 && links[sel]) links[sel].scrollIntoView({ block: 'nearest' });
  }
  input.addEventListener('focus', load);
  input.addEventListener('input', function () {
    var q = input.value.trim();
    if (!q) { panel.hidden = true; return; }
    load().then(function () { render(q); });
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { panel.hidden = true; input.blur(); return; }
    if (panel.hidden || !rows.length) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); sel = (sel + 1) % rows.length; highlight(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); sel = (sel - 1 + rows.length) % rows.length; highlight(); }
    else if (e.key === 'Enter' && sel >= 0) { e.preventDefault(); window.location.href = base + rows[sel].it.u; }
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.search-wrap')) panel.hidden = true;
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      e.preventDefault(); input.focus();
    }
  });
})();
