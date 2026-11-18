import { useEffect, useRef, useState } from 'react';
import { loadData, loadModel, rank } from './search';

const EXAMPLES = [
  'feeling overwhelmed at work',
  'quiet happiness',
  'someone betrayed me',
  'celebrating with friends',
  'that looks delicious',
  'abandoned and forgotten',
];

const RESULTS = 12;

export default function App() {
  const [phase, setPhase] = useState('loading');   // loading | ready | error
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [took, setTook] = useState(null);
  const [copied, setCopied] = useState(-1);

  const store = useRef(null);
  const extractor = useRef(null);
  const runId = useRef(0);
  const inputEl = useRef(null);

  useEffect(() => {
    let dead = false;
    (async () => {
      try {
        store.current = await loadData();
        extractor.current = await loadModel((p) => {
          if (p.status === 'progress' && p.file?.endsWith('.onnx')) {
            setProgress((cur) => Math.max(cur, p.progress ?? 0));
          }
        });
        if (dead) return;
        setProgress(100);
        setPhase('ready');
        inputEl.current?.focus();
      } catch (e) {
        if (!dead) { setError(e.message); setPhase('error'); }
      }
    })();
    return () => { dead = true; };
  }, []);

  useEffect(() => {
    if (phase !== 'ready') return;
    const q = query.trim();
    if (!q) { setResults([]); setTook(null); return; }

    const id = ++runId.current;
    const timer = setTimeout(async () => {
      const t0 = performance.now();
      const out = await extractor.current(q, { pooling: 'mean', normalize: true });
      if (id !== runId.current) return;          // a newer keystroke won
      const hits = rank(store.current, out.data, RESULTS);
      setResults(hits.map((h) => ({ ...store.current.items[h.i], score: h.score })));
      setTook(performance.now() - t0);
    }, 180);

    return () => clearTimeout(timer);
  }, [query, phase]);

  async function copy(emoji, idx) {
    try {
      await navigator.clipboard.writeText(emoji);
      setCopied(idx);
      setTimeout(() => setCopied((c) => (c === idx ? -1 : c)), 1200);
    } catch { /* clipboard blocked; silently ignore */ }
  }

  return (
    <main className="wrap">
      <header className="top">
        <h1>Emoji by meaning</h1>
        <p className="sub">
          Describe a feeling or a situation. Nothing you type leaves your device.
        </p>
      </header>

      <div className="field">
        <input
          ref={inputEl}
          className="q"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={phase === 'ready' ? 'how are you feeling?' : 'loading the model…'}
          disabled={phase !== 'ready'}
          autoComplete="off"
          spellCheck="false"
          aria-label="Search emoji by meaning"
        />
        <div className="rule">
          <div
            className={'fill' + (phase === 'ready' ? ' done' : '')}
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {phase === 'loading' && (
        <p className="note">
          Downloading the language model, about 25 MB. It is cached after the
          first visit.
        </p>
      )}

      {phase === 'error' && <p className="note err">Could not start: {error}</p>}

      {phase === 'ready' && !query.trim() && (
        <div className="chips">
          {EXAMPLES.map((ex) => (
            <button key={ex} className="chip" onClick={() => setQuery(ex)}>
              {ex}
            </button>
          ))}
        </div>
      )}

      {results.length > 0 && (
        <>
          <ul className="grid">
            {results.map((r, i) => (
              <li key={r.e + i}>
                <button
                  className="cell"
                  onClick={() => copy(r.e, i)}
                  title={`${r.n} — click to copy`}
                >
                  <span className="glyph">{r.e}</span>
                  <span className="score">
                    {copied === i ? 'copied' : r.score.toFixed(2)}
                  </span>
                </button>
              </li>
            ))}
          </ul>
          <p className="stats">
            {store.current?.meta.count.toLocaleString()} emoji searched in{' '}
            {took?.toFixed(0)} ms. Click any emoji to copy it.
          </p>
        </>
      )}
    </main>
  );
}