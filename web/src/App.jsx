import { useEffect, useState } from 'react';
import { pipeline, env } from '@huggingface/transformers';

env.allowLocalModels = false;

export default function App() {
  const [log, setLog] = useState([]);
  const [results, setResults] = useState([]);

  const say = (m) => setLog((l) => [...l, m]);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      // ---- stage 1: data ----
      say('fetching data...');
      const meta = await (await fetch('/data/meta.json')).json();
      const items = await (await fetch('/data/emoji.json')).json();
      const buf = await (await fetch('/data/vectors_int8.bin')).arrayBuffer();
      const Q = new Int8Array(buf);
      say(`data ok — ${items.length} emoji, ${meta.dims}d, ${Q.length} int8 values`);

      if (Q.length !== meta.count * meta.dims) {
        say('MISMATCH: vector buffer size does not match meta');
        return;
      }

      // ---- stage 2: model ----
      say('loading model (first time downloads ~25MB)...');
      const t0 = performance.now();
      const extractor = await pipeline(
        'feature-extraction',
        'Xenova/all-MiniLM-L6-v2',
        {
          dtype: 'q8',
          progress_callback: (p) => {
            if (p.status === 'progress' && p.file?.endsWith('.onnx')) {
              const pct = Math.round(p.progress ?? 0);
              if (pct % 20 === 0) say(`  ${p.file} ${pct}%`);
            }
          },
        }
      );
      if (cancelled) return;
      say(`model ready in ${((performance.now() - t0) / 1000).toFixed(1)}s`);

      // ---- stage 3: one search ----
      const query = 'feeling overwhelmed at work';
      const t1 = performance.now();
      const out = await extractor(query, { pooling: 'mean', normalize: true });
      const qv = out.data;
      say(`query embedded: ${qv.length} dims in ${(performance.now() - t1).toFixed(1)}ms`);

      const t2 = performance.now();
      const n = meta.count, d = meta.dims;
      const scores = new Float32Array(n);
      for (let i = 0; i < n; i++) {
        let s = 0;
        const off = i * d;
        for (let j = 0; j < d; j++) s += Q[off + j] * qv[j];
        scores[i] = s;
      }
      const top = Array.from(scores.keys())
        .sort((a, b) => scores[b] - scores[a])
        .slice(0, 12);
      say(`searched ${n} vectors in ${(performance.now() - t2).toFixed(2)}ms`);

      const k = meta.scale / 127;   // recover true cosine for display
      setResults(top.map((i) => ({ ...items[i], score: scores[i] * k })));
    })().catch((e) => say('ERROR: ' + e.message));

    return () => { cancelled = true; };
  }, []);

  return (
    <div style={{ fontFamily: 'ui-monospace, monospace', padding: 24, maxWidth: 720 }}>
      <h2>pipeline test</h2>
      <pre style={{ background: '#f4f4f4', padding: 12, whiteSpace: 'pre-wrap' }}>
        {log.join('\n')}
      </pre>
      <h3>query: "feeling overwhelmed at work"</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12 }}>
        {results.map((r, i) => (
          <div key={i} style={{ textAlign: 'center', width: 90 }}>
            <div style={{ fontSize: 40 }}>{r.e}</div>
            <div style={{ fontSize: 11, color: '#666' }}>{r.score.toFixed(3)}</div>
            <div style={{ fontSize: 10, color: '#999' }}>{r.n}</div>
          </div>
        ))}
      </div>
    </div>
  );
}