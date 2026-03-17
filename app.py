<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BI Data Generator PRO — Dados Reais para Business Intelligence</title>
<meta name="description" content="Gere bases de dados profissionais no modelo estrela em segundos. 10 setores, modelo star schema, dCalendario automático. Ideal para projetos de Power BI, Tableau e Data Analytics.">
<meta name="keywords" content="BI data generator, Power BI dados, star schema, modelo estrela, dCalendario, dados fictícios, business intelligence">
<meta property="og:title" content="BI Data Generator PRO — Star Schema em Segundos">
<meta property="og:description" content="Gere bases de dados profissionais no modelo estrela para Power BI, Tableau e qualquer projeto de BI.">
<meta property="og:type" content="website">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
/* ══════════════════════════════════════
   TOKENS
══════════════════════════════════════ */
:root {
  --bg:        #060912;
  --bg2:       #090d1a;
  --surface:   #0d1120;
  --surface2:  #111828;
  --border:    rgba(0,180,216,.12);
  --border2:   rgba(0,180,216,.22);
  --border3:   rgba(0,180,216,.4);
  --cyan:      #00b4d8;
  --cyan2:     #0096c7;
  --cyan-dim:  rgba(0,180,216,.08);
  --cyan-glow: rgba(0,180,216,.25);
  --text:      #e8edf8;
  --text2:     #8fa0bb;
  --text3:     #4a5878;
  --mono:      'JetBrains Mono', monospace;
  --display:   'Syne', sans-serif;
  --body:      'DM Sans', sans-serif;
  --r:         14px;
  --ease:      cubic-bezier(.22,1,.36,1);
}

*,*::before,*::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--body);
  font-size: 15px;
  line-height: 1.65;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
}

/* dot grid */
body::before {
  content: '';
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image: radial-gradient(rgba(0,180,216,.12) 1px, transparent 1px);
  background-size: 32px 32px;
  mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 20%, transparent 100%);
}

/* grain */
body::after {
  content: '';
  position: fixed; inset: 0; z-index: 0; pointer-events: none; opacity: .35;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
}

/* ══════════════════════════════════════
   NAV
══════════════════════════════════════ */
nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 48px;
  background: rgba(6,9,18,.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--display); font-weight: 800; font-size: 1rem;
  letter-spacing: -.02em; color: var(--text);
}
.nav-logo-icon {
  width: 32px; height: 32px; border-radius: 8px;
  background: linear-gradient(135deg, #00b4d8, #0077b6);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
}
.nav-chip {
  font-family: var(--mono); font-size: .65rem; letter-spacing: .1em;
  color: var(--cyan); border: 1px solid var(--border2);
  background: var(--cyan-dim); border-radius: 100px; padding: 3px 10px;
}
.nav-links { display: flex; align-items: center; gap: 32px; }
.nav-link {
  font-size: .82rem; color: var(--text2); text-decoration: none;
  letter-spacing: .01em; transition: color .2s;
}
.nav-link:hover { color: var(--cyan); }
.nav-cta {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, var(--cyan), var(--cyan2));
  color: #001a24; font-family: var(--display); font-weight: 700;
  font-size: .82rem; padding: 9px 22px; border-radius: 100px;
  text-decoration: none; transition: transform .2s, box-shadow .2s;
  box-shadow: 0 0 24px var(--cyan-glow);
}
.nav-cta:hover { transform: translateY(-2px); box-shadow: 0 6px 32px rgba(0,180,216,.45); }

/* ══════════════════════════════════════
   HERO
══════════════════════════════════════ */
.hero {
  position: relative; z-index: 1;
  padding: 160px 48px 120px;
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 80px; align-items: center;
  max-width: 1300px; margin: 0 auto;
}

/* scan line animation */
.hero::after {
  content: '';
  position: absolute; left: 0; right: 0;
  height: 1px; background: linear-gradient(90deg, transparent, var(--cyan), transparent);
  animation: scanLine 6s ease-in-out infinite;
  opacity: .35; pointer-events: none;
}
@keyframes scanLine {
  0%   { top: 10%; opacity: 0; }
  10%  { opacity: .35; }
  90%  { opacity: .35; }
  100% { top: 90%; opacity: 0; }
}

.hero-left { position: relative; }

.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--mono); font-size: .7rem; letter-spacing: .12em;
  text-transform: uppercase; color: var(--cyan);
  border: 1px solid var(--border2); background: var(--cyan-dim);
  border-radius: 100px; padding: 6px 14px; margin-bottom: 28px;
  animation: fadeUp .6s .1s both;
}
.eyebrow-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--cyan); animation: breathe 2s infinite; }
@keyframes breathe { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.3;transform:scale(.6)} }

.hero h1 {
  font-family: var(--display); font-size: clamp(2.6rem, 5vw, 4.2rem);
  font-weight: 800; line-height: 1.02; letter-spacing: -.04em;
  margin-bottom: 24px;
  animation: fadeUp .65s .18s both;
}
.hero h1 .hl {
  background: linear-gradient(120deg, var(--cyan) 0%, #48cae4 60%, #90e0ef 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.hero-sub {
  font-size: 1rem; color: var(--text2); max-width: 460px;
  line-height: 1.75; font-weight: 300; margin-bottom: 40px;
  animation: fadeUp .65s .26s both;
}

.hero-cta-row {
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
  animation: fadeUp .65s .34s both;
}
.btn-primary {
  display: inline-flex; align-items: center; gap: 9px;
  background: linear-gradient(135deg, var(--cyan), var(--cyan2));
  color: #001a24; font-family: var(--display); font-weight: 700; font-size: .9rem;
  padding: 13px 28px; border-radius: 100px; text-decoration: none;
  transition: transform .25s, box-shadow .25s;
  box-shadow: 0 0 28px var(--cyan-glow);
}
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 8px 40px rgba(0,180,216,.5); }
.btn-primary svg { width: 15px; height: 15px; transition: transform .2s; }
.btn-primary:hover svg { transform: translateX(3px); }
.btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  color: var(--text2); font-size: .86rem;
  border: 1px solid var(--border2); border-radius: 100px;
  padding: 13px 22px; text-decoration: none; transition: color .2s, border-color .2s;
}
.btn-ghost:hover { color: var(--cyan); border-color: var(--border3); }

/* stat pills */
.hero-stats {
  display: flex; gap: 12px; margin-top: 48px; flex-wrap: wrap;
  animation: fadeUp .65s .42s both;
}
.stat-pill {
  display: flex; align-items: center; gap: 10px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 12px 18px;
}
.stat-val { font-family: var(--display); font-weight: 800; font-size: 1.2rem; color: var(--cyan); }
.stat-lbl { font-size: .72rem; color: var(--text2); line-height: 1.3; }

/* ── HERO RIGHT — terminal mockup ── */
.hero-right {
  position: relative;
  animation: fadeUp .65s .22s both;
}
.terminal {
  background: var(--surface);
  border: 1px solid var(--border2);
  border-radius: 16px; overflow: hidden;
  box-shadow: 0 24px 80px rgba(0,0,0,.5), 0 0 0 1px rgba(0,180,216,.06);
  position: relative;
}
.terminal::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
}
.terminal-bar {
  display: flex; align-items: center; gap: 8px;
  padding: 14px 18px; background: rgba(0,0,0,.3);
  border-bottom: 1px solid var(--border);
}
.t-dot { width: 10px; height: 10px; border-radius: 50%; }
.t-title {
  font-family: var(--mono); font-size: .72rem; color: var(--text2);
  margin-left: 8px; flex: 1;
}
.t-status {
  font-family: var(--mono); font-size: .65rem; color: var(--cyan);
  background: var(--cyan-dim); border: 1px solid var(--border2);
  border-radius: 100px; padding: 2px 10px;
}
.terminal-body { padding: 20px 22px; }
.t-line {
  font-family: var(--mono); font-size: .76rem; line-height: 1.9;
  display: flex; align-items: baseline; gap: 10px;
}
.t-prompt { color: var(--cyan); user-select: none; }
.t-cmd    { color: #e8edf8; }
.t-out    { color: var(--text2); padding-left: 20px; }
.t-key    { color: #7dd3fc; }
.t-val    { color: #86efac; }
.t-sep    { color: var(--text3); }
.t-table  { color: #fbbf24; }
.t-num    { color: var(--cyan); }
.cursor {
  display: inline-block; width: 8px; height: 14px;
  background: var(--cyan); vertical-align: middle;
  animation: blink 1.2s step-end infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* progress bar inside terminal */
.t-progress-row { margin: 6px 0 4px 20px; }
.t-progress-track {
  height: 3px; background: rgba(0,180,216,.12); border-radius: 3px; overflow: hidden;
}
.t-progress-fill {
  height: 100%; border-radius: 3px;
  background: linear-gradient(90deg, var(--cyan2), var(--cyan));
  animation: loadBar 2.4s 1s both ease-out;
}
@keyframes loadBar { from{width:0} to{width:100%} }

/* ══════════════════════════════════════
   LOGOS STRIP
══════════════════════════════════════ */
.strip {
  position: relative; z-index: 1;
  border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
  padding: 28px 48px; text-align: center;
  background: linear-gradient(to bottom, var(--bg2), var(--bg));
}
.strip-label {
  font-family: var(--mono); font-size: .65rem; letter-spacing: .14em;
  text-transform: uppercase; color: var(--text3); margin-bottom: 18px;
}
.strip-row {
  display: flex; align-items: center; justify-content: center;
  gap: 10px; flex-wrap: wrap;
}
.sector-tag {
  font-family: var(--mono); font-size: .7rem; color: var(--text2);
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 6px 14px;
  transition: color .2s, border-color .2s, background .2s;
  cursor: default;
}
.sector-tag:hover { color: var(--cyan); border-color: var(--border2); background: var(--cyan-dim); }

/* ══════════════════════════════════════
   STAR SCHEMA DIAGRAM
══════════════════════════════════════ */
.schema-section {
  position: relative; z-index: 1;
  padding: 100px 48px; max-width: 1300px; margin: 0 auto;
}
.section-header { text-align: center; margin-bottom: 72px; }
.section-eyebrow {
  font-family: var(--mono); font-size: .68rem; letter-spacing: .16em;
  text-transform: uppercase; color: var(--cyan); margin-bottom: 14px;
  display: flex; align-items: center; justify-content: center; gap: 10px;
}
.section-eyebrow::before, .section-eyebrow::after {
  content: ''; flex: 1; max-width: 48px; height: 1px; background: rgba(0,180,216,.3);
}
.section-header h2 {
  font-family: var(--display); font-size: clamp(1.8rem, 3.5vw, 2.8rem);
  font-weight: 800; letter-spacing: -.03em; line-height: 1.1; margin-bottom: 14px;
}
.section-header p { color: var(--text2); font-size: .95rem; max-width: 480px; margin: 0 auto; font-weight: 300; }

/* schema diagram */
.schema-diagram {
  position: relative; max-width: 760px; margin: 0 auto;
  height: 420px;
}

/* fact table — center */
.schema-fact {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  background: linear-gradient(135deg, rgba(0,180,216,.18), rgba(0,119,182,.1));
  border: 1.5px solid var(--cyan); border-radius: 14px;
  padding: 20px 28px; text-align: center; z-index: 2;
  box-shadow: 0 0 40px rgba(0,180,216,.2);
  min-width: 160px;
}
.schema-fact-label {
  font-family: var(--mono); font-size: .65rem; color: var(--cyan);
  letter-spacing: .1em; text-transform: uppercase; margin-bottom: 6px;
}
.schema-fact-name {
  font-family: var(--display); font-weight: 800; font-size: 1rem; color: #fff;
}
.schema-fact-cols {
  margin-top: 10px; display: flex; flex-direction: column; gap: 3px;
}
.schema-fact-col {
  font-family: var(--mono); font-size: .62rem; color: var(--text2);
  background: rgba(0,180,216,.06); border-radius: 4px; padding: 2px 8px;
  text-align: left;
}
.schema-fact-col.fk { color: var(--cyan); }

/* dim tables */
.schema-dim {
  position: absolute; z-index: 2;
  background: var(--surface2); border: 1px solid var(--border2);
  border-radius: 12px; padding: 14px 18px; min-width: 130px;
  transition: border-color .3s, box-shadow .3s;
}
.schema-dim:hover { border-color: var(--border3); box-shadow: 0 0 24px var(--cyan-glow); }
.schema-dim-label {
  font-family: var(--mono); font-size: .58rem; color: var(--text3);
  letter-spacing: .1em; text-transform: uppercase; margin-bottom: 5px;
}
.schema-dim-name {
  font-family: var(--display); font-weight: 700; font-size: .82rem; color: var(--text);
  margin-bottom: 8px;
}
.schema-dim-cols { display: flex; flex-direction: column; gap: 2px; }
.schema-dim-col {
  font-family: var(--mono); font-size: .58rem; color: var(--text2);
  background: var(--surface); border-radius: 3px; padding: 2px 7px;
}
.schema-dim-col.pk { color: #fbbf24; }

/* connector lines via SVG */
.schema-svg {
  position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;
}
.conn-line {
  stroke: var(--cyan); stroke-width: 1; fill: none; stroke-dasharray: 4 4;
  animation: dashFlow 3s linear infinite;
}
@keyframes dashFlow { to { stroke-dashoffset: -24; } }

/* dim positions */
.dim-top    { top: 10px;  left: 50%; transform: translateX(-50%); }
.dim-right  { top: 50%;  right: 10px; transform: translateY(-50%); }
.dim-bottom { bottom: 10px; left: 50%; transform: translateX(-50%); }
.dim-left   { top: 50%;  left: 10px; transform: translateY(-50%); }
.dim-tr     { top: 30px;  right: 60px; }
.dim-tl     { top: 30px;  left: 60px; }

/* ══════════════════════════════════════
   FEATURES GRID
══════════════════════════════════════ */
.features-section {
  position: relative; z-index: 1;
  padding: 100px 48px; max-width: 1300px; margin: 0 auto;
}
.features-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 20px; margin-top: 64px;
}
.feature-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r); padding: 32px;
  position: relative; overflow: hidden;
  transition: border-color .3s, transform .3s var(--ease), box-shadow .3s;
}
.feature-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
  transform: scaleX(0); transform-origin: left;
  transition: transform .4s var(--ease);
}
.feature-card:hover { transform: translateY(-5px); border-color: var(--border2); box-shadow: 0 16px 48px rgba(0,0,0,.35); }
.feature-card:hover::before { transform: scaleX(1); }

.feature-icon {
  width: 46px; height: 46px; border-radius: 12px;
  background: var(--cyan-dim); border: 1px solid var(--border2);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; margin-bottom: 20px;
  transition: box-shadow .3s;
}
.feature-card:hover .feature-icon { box-shadow: 0 0 20px var(--cyan-glow); }
.feature-title {
  font-family: var(--display); font-weight: 700; font-size: 1rem;
  letter-spacing: -.015em; margin-bottom: 10px;
}
.feature-text { font-size: .84rem; color: var(--text2); line-height: 1.75; font-weight: 300; }
.feature-mono {
  margin-top: 14px; font-family: var(--mono); font-size: .68rem;
  color: var(--cyan); background: var(--cyan-dim); border: 1px solid var(--border);
  border-radius: 6px; padding: 6px 10px; display: inline-block;
}

/* ══════════════════════════════════════
   CALENDAR SECTION
══════════════════════════════════════ */
.calendar-section {
  position: relative; z-index: 1;
  padding: 100px 48px;
  background: linear-gradient(to bottom, var(--bg), var(--bg2) 40%, var(--bg2) 60%, var(--bg));
}
.calendar-inner { max-width: 1100px; margin: 0 auto; }

.cal-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 64px; align-items: center; margin-top: 64px;
}
.cal-text h3 {
  font-family: var(--display); font-weight: 800;
  font-size: clamp(1.5rem, 3vw, 2.2rem); letter-spacing: -.03em; line-height: 1.15;
  margin-bottom: 16px;
}
.cal-text p { color: var(--text2); font-size: .9rem; line-height: 1.8; font-weight: 300; margin-bottom: 24px; }

.col-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 32px; }
.col-item {
  display: flex; align-items: center; gap: 14px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 10px; padding: 12px 16px;
  transition: border-color .25s, background .25s;
}
.col-item:hover { border-color: var(--border2); background: var(--surface2); }
.col-name { font-family: var(--mono); font-size: .78rem; color: var(--cyan); min-width: 90px; }
.col-type {
  font-family: var(--mono); font-size: .65rem; color: var(--text3);
  background: rgba(0,180,216,.06); border-radius: 4px; padding: 2px 8px;
}
.col-desc { font-size: .78rem; color: var(--text2); font-weight: 300; }

/* calendar table preview */
.cal-table-wrap {
  background: var(--surface); border: 1px solid var(--border2);
  border-radius: var(--r); overflow: hidden;
  box-shadow: 0 16px 48px rgba(0,0,0,.4);
  position: relative;
}
.cal-table-wrap::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
}
.cal-table-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px; border-bottom: 1px solid var(--border);
  background: rgba(0,0,0,.2);
}
.cal-table-title {
  font-family: var(--mono); font-size: .72rem; color: var(--cyan);
  display: flex; align-items: center; gap: 8px;
}
.cal-table-badge {
  font-family: var(--mono); font-size: .6rem; color: var(--text2);
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 100px; padding: 2px 10px;
}
table { width: 100%; border-collapse: collapse; }
th {
  font-family: var(--mono); font-size: .62rem; color: var(--text3);
  text-transform: uppercase; letter-spacing: .08em;
  padding: 10px 14px; border-bottom: 1px solid var(--border);
  text-align: left; background: rgba(0,0,0,.15);
}
td {
  font-family: var(--mono); font-size: .72rem; padding: 9px 14px;
  border-bottom: 1px solid rgba(0,180,216,.05); color: var(--text2);
}
td.td-date { color: var(--text); }
td.td-num  { color: var(--cyan); }
td.td-mes  { color: #86efac; }
td.td-id   { color: #fbbf24; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(0,180,216,.03); }

/* ══════════════════════════════════════
   SECTORS CAROUSEL — HORIZONTAL SCROLL
══════════════════════════════════════ */
.sectors-section {
  position: relative; z-index: 1; padding: 100px 0;
  overflow: hidden;
}
.sectors-header { padding: 0 48px; margin-bottom: 56px; }
.sectors-track-wrap { position: relative; }
.sectors-track-wrap::before,
.sectors-track-wrap::after {
  content: ''; position: absolute; top: 0; bottom: 0; width: 120px; z-index: 2; pointer-events: none;
}
.sectors-track-wrap::before { left: 0; background: linear-gradient(to right, var(--bg), transparent); }
.sectors-track-wrap::after  { right: 0; background: linear-gradient(to left, var(--bg), transparent); }

.sectors-track {
  display: flex; gap: 16px; padding: 8px 48px;
  overflow-x: auto; scroll-snap-type: x mandatory;
  scrollbar-width: none;
}
.sectors-track::-webkit-scrollbar { display: none; }

.sector-card {
  flex-shrink: 0; scroll-snap-align: start;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r); padding: 24px 28px; min-width: 220px;
  transition: border-color .3s, transform .3s var(--ease), box-shadow .3s;
  cursor: default;
}
.sector-card:hover {
  border-color: var(--border2); transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0,0,0,.3);
}
.sector-card-icon { font-size: 28px; margin-bottom: 14px; display: block; }
.sector-card-name {
  font-family: var(--display); font-weight: 700; font-size: .95rem;
  margin-bottom: 6px; letter-spacing: -.01em;
}
.sector-card-hint { font-size: .76rem; color: var(--text2); font-weight: 300; }
.sector-card-tables {
  margin-top: 14px; display: flex; flex-direction: column; gap: 4px;
}
.sector-table-tag {
  font-family: var(--mono); font-size: .62rem; color: var(--text3);
  background: var(--surface2); border-radius: 4px; padding: 3px 8px;
}

/* ══════════════════════════════════════
   HOW IT WORKS
══════════════════════════════════════ */
.how-section {
  position: relative; z-index: 1;
  padding: 100px 48px; max-width: 1100px; margin: 0 auto;
}
.steps-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 0; margin-top: 64px; position: relative;
}
.steps-grid::before {
  content: '';
  position: absolute; top: 28px; left: 10%; right: 10%; height: 1px;
  background: linear-gradient(90deg, transparent, var(--border2), var(--border2), transparent);
}
.step {
  text-align: center; padding: 0 16px; position: relative;
}
.step-num {
  width: 56px; height: 56px; border-radius: 50%;
  background: var(--surface2); border: 1px solid var(--border2);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--display); font-weight: 800; font-size: .9rem;
  color: var(--cyan); margin: 0 auto 20px;
  position: relative; z-index: 1;
  transition: background .3s, box-shadow .3s;
}
.step:hover .step-num { background: var(--cyan-dim); box-shadow: 0 0 24px var(--cyan-glow); }
.step-icon { font-size: 22px; display: block; margin-bottom: 12px; }
.step-title {
  font-family: var(--display); font-weight: 700; font-size: .9rem;
  margin-bottom: 8px; letter-spacing: -.01em;
}
.step-text { font-size: .78rem; color: var(--text2); line-height: 1.65; font-weight: 300; }

/* ══════════════════════════════════════
   CTA SECTION
══════════════════════════════════════ */
.cta-section {
  position: relative; z-index: 1;
  padding: 100px 48px 120px; text-align: center;
}
.cta-glow {
  position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(0,180,216,.07) 0%, transparent 65%);
}
.cta-box {
  max-width: 620px; margin: 0 auto;
  background: var(--surface); border: 1px solid var(--border2);
  border-radius: 24px; padding: 64px 56px; position: relative; overflow: hidden;
}
.cta-box::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
}
.cta-tag {
  font-family: var(--mono); font-size: .68rem; letter-spacing: .14em;
  text-transform: uppercase; color: var(--cyan); margin-bottom: 20px;
  display: flex; align-items: center; justify-content: center; gap: 10px;
}
.cta-tag::before,.cta-tag::after { content:''; flex:1; max-width:40px; height:1px; background:rgba(0,180,216,.3); }
.cta-box h2 {
  font-family: var(--display); font-size: clamp(1.6rem,4vw,2.4rem);
  font-weight: 800; letter-spacing: -.03em; line-height: 1.08; margin-bottom: 16px;
}
.cta-box > p { color: var(--text2); font-size: .9rem; line-height: 1.75; max-width: 400px; margin: 0 auto 36px; font-weight: 300; }
.cta-form { display: flex; gap: 10px; max-width: 400px; margin: 0 auto; }
.cta-input {
  flex: 1; background: var(--bg2); border: 1px solid var(--border2);
  color: var(--text); font-family: var(--body); font-size: .88rem;
  padding: 12px 18px; border-radius: 100px; outline: none;
  transition: border-color .2s, box-shadow .2s;
}
.cta-input::placeholder { color: var(--text3); }
.cta-input:focus { border-color: var(--border3); box-shadow: 0 0 0 3px rgba(0,180,216,.09); }
.cta-btn {
  background: linear-gradient(135deg, var(--cyan), var(--cyan2));
  color: #001a24; font-family: var(--display); font-weight: 700; font-size: .85rem;
  padding: 12px 24px; border-radius: 100px; border: none; cursor: pointer;
  white-space: nowrap; transition: transform .2s, box-shadow .2s;
  box-shadow: 0 0 20px rgba(0,180,216,.3);
}
.cta-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 32px rgba(0,180,216,.5); }
.cta-fine { margin-top: 14px; font-size: .7rem; color: var(--text3); font-family: var(--mono); }

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
footer {
  position: relative; z-index: 1;
  border-top: 1px solid var(--border);
  padding: 32px 48px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: .78rem; color: var(--text2);
  background: var(--bg2);
}
.footer-logo { font-family: var(--display); font-weight: 800; font-size: .9rem; color: var(--cyan); }
.footer-links { display: flex; gap: 28px; }
.footer-link { color: var(--text2); text-decoration: none; transition: color .2s; }
.footer-link:hover { color: var(--cyan); }
.footer-mono { font-family: var(--mono); font-size: .68rem; color: var(--text3); }

/* ══════════════════════════════════════
   ANIMATIONS
══════════════════════════════════════ */
@keyframes fadeUp { to { opacity: 1; transform: none; } }
.reveal { opacity: 0; transform: translateY(20px); transition: opacity .6s var(--ease), transform .6s var(--ease); }
.reveal.visible { opacity: 1; transform: none; }

/* ══════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════ */
@media (max-width: 960px) {
  nav { padding: 14px 24px; }
  .nav-links { display: none; }
  .hero { grid-template-columns: 1fr; gap: 48px; padding: 120px 24px 80px; }
  .hero-right { display: none; }
  .strip { padding: 24px; }
  .schema-section, .features-section, .how-section { padding: 64px 24px; }
  .features-grid { grid-template-columns: 1fr; }
  .steps-grid { grid-template-columns: 1fr 1fr; gap: 32px; }
  .steps-grid::before { display: none; }
  .cal-grid { grid-template-columns: 1fr; gap: 40px; }
  .calendar-section { padding: 64px 24px; }
  .sectors-header { padding: 0 24px; }
  .cta-section { padding: 64px 24px 80px; }
  .cta-box { padding: 44px 28px; }
  .cta-form { flex-direction: column; }
  footer { flex-direction: column; gap: 16px; text-align: center; padding: 28px 24px; }
}
</style>
</head>
<body>

<!-- ══ NAV ══ -->
<nav>
  <div class="nav-logo">
    <div class="nav-logo-icon">📊</div>
    BI Data Generator
    <span class="nav-chip">PRO</span>
  </div>
  <div class="nav-links">
    <a href="#schema" class="nav-link">Star Schema</a>
    <a href="#calendario" class="nav-link">dCalendario</a>
    <a href="#setores" class="nav-link">Setores</a>
    <a href="#como" class="nav-link">Como usar</a>
  </div>
  <a href="https://bi-data-generator.streamlit.app" class="nav-cta" target="_blank">
    Abrir app
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
  </a>
</nav>

<!-- ══ HERO ══ -->
<section class="hero">
  <div class="hero-left">
    <div class="hero-eyebrow"><span class="eyebrow-dot"></span> Star Schema · 10 Setores · dCalendario</div>
    <h1>Dados reais para<br>seu projeto de <span class="hl">Business<br>Intelligence</span></h1>
    <p class="hero-sub">
      Gere bases profissionais no modelo estrela em segundos. Tabelas fato, dimensões e dCalendario prontos para Power BI, Tableau e qualquer ferramenta de BI.
    </p>
    <div class="hero-cta-row">
      <a href="https://bi-data-generator.streamlit.app" class="btn-primary" target="_blank">
        Gerar minha base agora
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
      </a>
      <a href="#schema" class="btn-ghost">Ver estrutura</a>
    </div>
    <div class="hero-stats">
      <div class="stat-pill">
        <span class="stat-val">10</span>
        <span class="stat-lbl">setores<br>disponíveis</span>
      </div>
      <div class="stat-pill">
        <span class="stat-val">10k</span>
        <span class="stat-lbl">linhas<br>máximo</span>
      </div>
      <div class="stat-pill">
        <span class="stat-val">.zip</span>
        <span class="stat-lbl">download<br>completo</span>
      </div>
      <div class="stat-pill">
        <span class="stat-val">free</span>
        <span class="stat-lbl">sem<br>cadastro</span>
      </div>
    </div>
  </div>

  <!-- terminal mockup -->
  <div class="hero-right">
    <div class="terminal">
      <div class="terminal-bar">
        <div class="t-dot" style="background:#ff5f57"></div>
        <div class="t-dot" style="background:#febc2e"></div>
        <div class="t-dot" style="background:#28c840"></div>
        <span class="t-title">bi_generator — python app.py</span>
        <span class="t-status">● running</span>
      </div>
      <div class="terminal-body">
        <div class="t-line"><span class="t-prompt">$</span><span class="t-cmd">gerar_base_completa(<span class="t-key">setor</span>=<span class="t-val">"Varejo"</span>, <span class="t-key">linhas</span>=<span class="t-num">5000</span>)</span></div>
        <div class="t-line"><span class="t-out">→ Inicializando gerador...</span></div>
        <div class="t-progress-row"><div class="t-progress-track"><div class="t-progress-fill" style="width:100%"></div></div></div>
        <div class="t-line" style="margin-top:8px"><span class="t-out">✓ <span class="t-table">DimCliente</span> &nbsp;&nbsp;&nbsp; <span class="t-num">5.000</span> linhas</span></div>
        <div class="t-line"><span class="t-out">✓ <span class="t-table">DimProduto</span> &nbsp;&nbsp; <span class="t-num">500</span> &nbsp; linhas</span></div>
        <div class="t-line"><span class="t-out">✓ <span class="t-table">DimVendedor</span> &nbsp; <span class="t-num">50</span> &nbsp;&nbsp; linhas</span></div>
        <div class="t-line"><span class="t-out">✓ <span class="t-table">DimFilial</span> &nbsp;&nbsp;&nbsp; <span class="t-num">10</span> &nbsp;&nbsp; linhas</span></div>
        <div class="t-line"><span class="t-out">✓ <span class="t-table">DimGeografia</span> &nbsp;<span class="t-num">17</span> &nbsp;&nbsp; linhas</span></div>
        <div class="t-line"><span class="t-out">✓ <span class="t-table">FatoVendas</span> &nbsp;&nbsp; <span class="t-num">5.000</span> linhas</span></div>
        <div class="t-line"><span class="t-out">✓ <span class="t-table">dCalendario</span> &nbsp;&nbsp; <span class="t-num">365</span> &nbsp;&nbsp; dias</span></div>
        <div class="t-line" style="margin-top:10px"><span class="t-out" style="color:#86efac">✓ Base gerada — zipando arquivos...</span></div>
        <div class="t-line"><span class="t-out" style="color:#86efac">✓ Base_BI_Varejo.zip pronto (2.1 MB)</span></div>
        <div class="t-line" style="margin-top:8px"><span class="t-prompt">$</span><span class="cursor"></span></div>
      </div>
    </div>
  </div>
</section>

<!-- ══ SECTORS STRIP ══ -->
<div class="strip reveal">
  <div class="strip-label">setores disponíveis na versão atual</div>
  <div class="strip-row">
    <span class="sector-tag">🛒 Varejo</span>
    <span class="sector-tag">💰 Financeiro</span>
    <span class="sector-tag">🏥 Saúde</span>
    <span class="sector-tag">💻 Tecnologia</span>
    <span class="sector-tag">📚 Educação</span>
    <span class="sector-tag">🚚 Logística</span>
    <span class="sector-tag">⚡ Energia</span>
    <span class="sector-tag">📡 Telecom</span>
    <span class="sector-tag">🏭 Indústria</span>
    <span class="sector-tag">🌾 Agronegócio</span>
  </div>
</div>

<!-- ══ STAR SCHEMA ══ -->
<section class="schema-section" id="schema">
  <div class="section-header reveal">
    <div class="section-eyebrow">Modelo de dados</div>
    <h2>Star Schema pronto para produção</h2>
    <p>Cada setor gera tabelas fato e dimensões relacionadas, prontas para serem carregadas diretamente no Power BI ou Tableau</p>
  </div>

  <div class="schema-diagram reveal">
    <!-- SVG connector lines -->
    <svg class="schema-svg" viewBox="0 0 760 420" xmlns="http://www.w3.org/2000/svg">
      <!-- top: DimCliente → Fato (center ~380,210) -->
      <line class="conn-line" x1="380" y1="90"  x2="380" y2="178"/>
      <!-- right: DimProduto -->
      <line class="conn-line" x1="600" y1="210" x2="492" y2="210"/>
      <!-- bottom: DimVendedor -->
      <line class="conn-line" x1="380" y1="330" x2="380" y2="242"/>
      <!-- left: DimFilial -->
      <line class="conn-line" x1="160" y1="210" x2="268" y2="210"/>
      <!-- tr: DimGeografia -->
      <line class="conn-line" x1="580" y1="80"  x2="460" y2="185"/>
      <!-- tl: dCalendario -->
      <line class="conn-line" x1="180" y1="80"  x2="300" y2="185"/>
    </svg>

    <!-- Fact center -->
    <div class="schema-fact">
      <div class="schema-fact-label">● Fato</div>
      <div class="schema-fact-name">FatoVendas</div>
      <div class="schema-fact-cols">
        <div class="schema-fact-col fk">id_cliente →</div>
        <div class="schema-fact-col fk">id_produto →</div>
        <div class="schema-fact-col fk">id_vendedor →</div>
        <div class="schema-fact-col fk">id_filial →</div>
        <div class="schema-fact-col fk">id_data →</div>
        <div class="schema-fact-col">valor_total</div>
        <div class="schema-fact-col">quantidade</div>
      </div>
    </div>

    <!-- Dims -->
    <div class="schema-dim dim-top">
      <div class="schema-dim-label">● Dim</div>
      <div class="schema-dim-name">DimCliente</div>
      <div class="schema-dim-cols">
        <div class="schema-dim-col pk">id_cliente PK</div>
        <div class="schema-dim-col">nome</div>
        <div class="schema-dim-col">segmento</div>
        <div class="schema-dim-col">cidade</div>
      </div>
    </div>
    <div class="schema-dim dim-right">
      <div class="schema-dim-label">● Dim</div>
      <div class="schema-dim-name">DimProduto</div>
      <div class="schema-dim-cols">
        <div class="schema-dim-col pk">id_produto PK</div>
        <div class="schema-dim-col">nome</div>
        <div class="schema-dim-col">categoria</div>
        <div class="schema-dim-col">preco</div>
      </div>
    </div>
    <div class="schema-dim dim-bottom">
      <div class="schema-dim-label">● Dim</div>
      <div class="schema-dim-name">DimVendedor</div>
      <div class="schema-dim-cols">
        <div class="schema-dim-col pk">id_vendedor PK</div>
        <div class="schema-dim-col">nome</div>
        <div class="schema-dim-col">regiao</div>
      </div>
    </div>
    <div class="schema-dim dim-left">
      <div class="schema-dim-label">● Dim</div>
      <div class="schema-dim-name">DimFilial</div>
      <div class="schema-dim-cols">
        <div class="schema-dim-col pk">id_filial PK</div>
        <div class="schema-dim-col">nome</div>
        <div class="schema-dim-col">uf</div>
      </div>
    </div>
    <div class="schema-dim dim-tr">
      <div class="schema-dim-label">● Dim</div>
      <div class="schema-dim-name">DimGeografia</div>
      <div class="schema-dim-cols">
        <div class="schema-dim-col pk">id_geo PK</div>
        <div class="schema-dim-col">estado</div>
        <div class="schema-dim-col">regiao</div>
      </div>
    </div>
    <div class="schema-dim dim-tl">
      <div class="schema-dim-label">● Dim</div>
      <div class="schema-dim-name">dCalendario</div>
      <div class="schema-dim-cols">
        <div class="schema-dim-col pk">Data PK</div>
        <div class="schema-dim-col">Ano · Mês</div>
        <div class="schema-dim-col">MesAno · IdMesAno</div>
      </div>
    </div>
  </div>
</section>

<!-- ══ FEATURES ══ -->
<section class="features-section">
  <div class="section-header reveal">
    <div class="section-eyebrow">Funcionalidades</div>
    <h2>Tudo que seu projeto de BI precisa</h2>
    <p>Dados coerentes, relacionamentos válidos e estrutura pronta para análise</p>
  </div>
  <div class="features-grid reveal">
    <div class="feature-card">
      <div class="feature-icon">⭐</div>
      <div class="feature-title">Modelo Estrela nativo</div>
      <div class="feature-text">Tabelas fato e dimensões com chaves primárias e estrangeiras consistentes. Relações íntegras, prontas para modelagem no Power BI.</div>
      <span class="feature-mono">FatoVendas → Dims</span>
    </div>
    <div class="feature-card">
      <div class="feature-icon">📅</div>
      <div class="feature-title">dCalendario automático</div>
      <div class="feature-text">Tabela de calendário gerada via Python com Data, Ano, Mês, MesAno e IdMesAno — equivalente exato ao script Power Query.</div>
      <span class="feature-mono">IdMesAno = Ano×100+Mês</span>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🏭</div>
      <div class="feature-title">10 setores especializados</div>
      <div class="feature-text">Cada setor gera colunas e valores contextualmente corretos. Varejo tem SKU e categoria; Saúde tem CID e procedimentos.</div>
      <span class="feature-mono">setor="Financeiro"</span>
    </div>
    <div class="feature-card">
      <div class="feature-icon">📦</div>
      <div class="feature-title">Download em .zip</div>
      <div class="feature-text">Todas as tabelas exportadas em CSV separados, compactadas em um único arquivo pronto para importar no Power BI ou Python.</div>
      <span class="feature-mono">Base_BI_{setor}.zip</span>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🎛️</div>
      <div class="feature-title">Controle total do volume</div>
      <div class="feature-text">Defina o período temporal e a quantidade de linhas da tabela fato — de 1.000 a 10.000 registros com distribuição realista.</div>
      <span class="feature-mono">linhas=5000</span>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🆓</div>
      <div class="feature-title">100% gratuito e open</div>
      <div class="feature-text">Sem cadastro, sem limite de uso, sem mensalidade. Roda no Streamlit Cloud — basta acessar e gerar quantas bases precisar.</div>
      <span class="feature-mono">streamlit.app</span>
    </div>
  </div>
</section>

<!-- ══ DCALENDARIO ══ -->
<section class="calendar-section" id="calendario">
  <div class="calendar-inner">
    <div class="section-header reveal">
      <div class="section-eyebrow">dCalendario</div>
      <h2>Tabela de calendário Power Query–compatível</h2>
      <p>Gerada em Python e 100% compatível com o padrão Power Query — mesmos tipos, mesma lógica, mesmo resultado</p>
    </div>
    <div class="cal-grid reveal">
      <div class="cal-text">
        <h3>Estrutura idêntica ao<br>script Power Query</h3>
        <p>A tabela dCalendario é construída seguindo exatamente a mesma sequência de transformações do Power Query — ColunaData, ColunaAno, ColunaMes, ColunaMesAno e ColunaIdMesAno — garantindo compatibilidade total com modelos existentes.</p>
        <div class="col-list">
          <div class="col-item">
            <span class="col-name">Data</span>
            <span class="col-type">date</span>
            <span class="col-desc">Dia a dia do período selecionado</span>
          </div>
          <div class="col-item">
            <span class="col-name">Ano</span>
            <span class="col-type">int64</span>
            <span class="col-desc">Date.Year([Data])</span>
          </div>
          <div class="col-item">
            <span class="col-name">Mês</span>
            <span class="col-type">int64</span>
            <span class="col-desc">Date.Month([Data])</span>
          </div>
          <div class="col-item">
            <span class="col-name">MesAno</span>
            <span class="col-type">text</span>
            <span class="col-desc">Text.Proper(MMM/yy) → Jan/23</span>
          </div>
          <div class="col-item">
            <span class="col-name">IdMesAno</span>
            <span class="col-type">int64</span>
            <span class="col-desc">Ano × 100 + Mês → 202301</span>
          </div>
        </div>
      </div>

      <!-- table preview -->
      <div class="cal-table-wrap">
        <div class="cal-table-header">
          <span class="cal-table-title">📅 dCalendario</span>
          <span class="cal-table-badge">365 linhas · 5 colunas</span>
        </div>
        <table>
          <thead>
            <tr><th>Data</th><th>Ano</th><th>Mês</th><th>MesAno</th><th>IdMesAno</th></tr>
          </thead>
          <tbody>
            <tr><td class="td-date">2023-01-01</td><td class="td-num">2023</td><td class="td-num">1</td><td class="td-mes">Jan/23</td><td class="td-id">202301</td></tr>
            <tr><td class="td-date">2023-01-02</td><td class="td-num">2023</td><td class="td-num">1</td><td class="td-mes">Jan/23</td><td class="td-id">202301</td></tr>
            <tr><td class="td-date">2023-01-31</td><td class="td-num">2023</td><td class="td-num">1</td><td class="td-mes">Jan/23</td><td class="td-id">202301</td></tr>
            <tr><td class="td-date">2023-02-01</td><td class="td-num">2023</td><td class="td-num">2</td><td class="td-mes">Fev/23</td><td class="td-id">202302</td></tr>
            <tr><td class="td-date">2023-06-15</td><td class="td-num">2023</td><td class="td-num">6</td><td class="td-mes">Jun/23</td><td class="td-id">202306</td></tr>
            <tr><td class="td-date">2023-12-31</td><td class="td-num">2023</td><td class="td-num">12</td><td class="td-mes">Dez/23</td><td class="td-id">202312</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<!-- ══ SECTORS ══ -->
<section class="sectors-section" id="setores">
  <div class="sectors-header reveal">
    <div class="section-eyebrow" style="justify-content:flex-start">Setores</div>
    <h2 style="font-family:var(--display);font-size:clamp(1.8rem,3.5vw,2.8rem);font-weight:800;letter-spacing:-.03em;margin-bottom:10px">Dados contextuais por setor</h2>
    <p style="color:var(--text2);font-size:.9rem;max-width:520px;font-weight:300">Cada setor gera colunas, categorias e valores estatisticamente coerentes com o mercado real</p>
  </div>
  <div class="sectors-track-wrap">
    <div class="sectors-track" id="sectorsTrack">
      <div class="sector-card">
        <span class="sector-card-icon">🛒</span>
        <div class="sector-card-name">Varejo</div>
        <div class="sector-card-hint">Vendas B2C, produtos e lojas físicas</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimProduto</span>
          <span class="sector-table-tag">DimCliente</span>
          <span class="sector-table-tag">DimFilial</span>
          <span class="sector-table-tag">FatoVendas</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">💰</span>
        <div class="sector-card-name">Financeiro</div>
        <div class="sector-card-hint">Transações, contas e carteiras</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimConta</span>
          <span class="sector-table-tag">DimAgencia</span>
          <span class="sector-table-tag">FatoTransacao</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">🏥</span>
        <div class="sector-card-name">Saúde</div>
        <div class="sector-card-hint">Pacientes, procedimentos e atendimentos</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimPaciente</span>
          <span class="sector-table-tag">DimMedico</span>
          <span class="sector-table-tag">FatoAtendimento</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">💻</span>
        <div class="sector-card-name">Tecnologia</div>
        <div class="sector-card-hint">SaaS, licenças e suporte técnico</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimCliente</span>
          <span class="sector-table-tag">DimProduto</span>
          <span class="sector-table-tag">FatoContrato</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">📚</span>
        <div class="sector-card-name">Educação</div>
        <div class="sector-card-hint">Alunos, cursos e matrículas</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimAluno</span>
          <span class="sector-table-tag">DimCurso</span>
          <span class="sector-table-tag">FatoMatricula</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">🚚</span>
        <div class="sector-card-name">Logística</div>
        <div class="sector-card-hint">Entregas, rotas e transportadoras</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimTransportadora</span>
          <span class="sector-table-tag">DimRota</span>
          <span class="sector-table-tag">FatoEntrega</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">⚡</span>
        <div class="sector-card-name">Energia</div>
        <div class="sector-card-hint">Consumo, medidores e contratos</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimConsumidor</span>
          <span class="sector-table-tag">DimMedidor</span>
          <span class="sector-table-tag">FatoConsumo</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">📡</span>
        <div class="sector-card-name">Telecom</div>
        <div class="sector-card-hint">Planos, chamadas e assinantes</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimAssinante</span>
          <span class="sector-table-tag">DimPlano</span>
          <span class="sector-table-tag">FatoChamada</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">🏭</span>
        <div class="sector-card-name">Indústria</div>
        <div class="sector-card-hint">Produção, insumos e ordens de fabricação</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimMaquina</span>
          <span class="sector-table-tag">DimInsumo</span>
          <span class="sector-table-tag">FatoProducao</span>
        </div>
      </div>
      <div class="sector-card">
        <span class="sector-card-icon">🌾</span>
        <div class="sector-card-name">Agronegócio</div>
        <div class="sector-card-hint">Safras, culturas e propriedades rurais</div>
        <div class="sector-card-tables">
          <span class="sector-table-tag">DimPropriedade</span>
          <span class="sector-table-tag">DimCultura</span>
          <span class="sector-table-tag">FatoSafra</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ══ HOW IT WORKS ══ -->
<section class="how-section" id="como">
  <div class="section-header reveal">
    <div class="section-eyebrow">Como usar</div>
    <h2>Do zero à base pronta em 4 passos</h2>
    <p>Sem configuração, sem código, sem espera</p>
  </div>
  <div class="steps-grid reveal">
    <div class="step">
      <div class="step-num">01</div>
      <span class="step-icon">🏭</span>
      <div class="step-title">Escolha o setor</div>
      <div class="step-text">Selecione entre 10 setores pré-configurados com dados contextualmente corretos</div>
    </div>
    <div class="step">
      <div class="step-num">02</div>
      <span class="step-icon">📅</span>
      <div class="step-title">Defina o período</div>
      <div class="step-text">Configure data início e fim — a dCalendario é gerada automaticamente para o intervalo</div>
    </div>
    <div class="step">
      <div class="step-num">03</div>
      <span class="step-icon">🚀</span>
      <div class="step-title">Clique em Gerar</div>
      <div class="step-text">A base completa é gerada em segundos com relações íntegras entre todas as tabelas</div>
    </div>
    <div class="step">
      <div class="step-num">04</div>
      <span class="step-icon">📦</span>
      <div class="step-title">Baixe o .zip</div>
      <div class="step-text">CSVs prontos para importar direto no Power BI, Tableau, Python ou qualquer ferramenta</div>
    </div>
  </div>
</section>

<!-- ══ CTA ══ -->
<section class="cta-section">
  <div class="cta-glow"></div>
  <div class="cta-box reveal">
    <div class="cta-tag">Acesso gratuito</div>
    <h2>Comece a gerar<br>sua base agora</h2>
    <p>Sem cadastro. Sem limite. Só acessar e gerar quantas bases precisar.</p>
    <div style="margin-bottom:8px">
      <a href="https://bi-data-generator.streamlit.app" class="btn-primary" target="_blank" style="display:inline-flex;font-size:.9rem;padding:14px 32px">
        Abrir o BI Data Generator
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
      </a>
    </div>
    <p class="cta-fine">// gratuito · sem cadastro · open source</p>
  </div>
</section>

<!-- ══ FOOTER ══ -->
<footer>
  <span class="footer-logo">📊 BI Data Generator PRO</span>
  <div class="footer-links">
    <a href="#schema" class="footer-link">Star Schema</a>
    <a href="#calendario" class="footer-link">dCalendario</a>
    <a href="#setores" class="footer-link">Setores</a>
    <a href="#como" class="footer-link">Como usar</a>
  </div>
  <span class="footer-mono">// built with Streamlit + Python</span>
</footer>

<!-- ══ SCHEMA.ORG SEO ══ -->
<script>
const schema = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "BI Data Generator PRO",
  "description": "Gerador de bases de dados profissionais no modelo estrela para projetos de Business Intelligence",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Web",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "BRL" },
  "featureList": [
    "Modelo Star Schema",
    "10 setores de negócio",
    "dCalendario automático",
    "Exportação em CSV/ZIP",
    "Compatível com Power BI e Tableau"
  ]
};
const s = document.createElement('script');
s.type = 'application/ld+json';
s.textContent = JSON.stringify(schema);
document.head.appendChild(s);

// Reveal on scroll
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
}, { threshold: .1 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Sectors auto-scroll
const track = document.getElementById('sectorsTrack');
let isPaused = false;
track.addEventListener('mouseenter', () => isPaused = true);
track.addEventListener('mouseleave', () => isPaused = false);
let pos = 0;
setInterval(() => {
  if (!isPaused) {
    pos += .6;
    if (pos >= track.scrollWidth - track.clientWidth) pos = 0;
    track.scrollLeft = pos;
  }
}, 16);
</script>
</body>
</html>
