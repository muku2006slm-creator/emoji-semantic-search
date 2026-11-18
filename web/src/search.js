import { pipeline, env } from '@huggingface/transformers';

env.allowLocalModels = false;

const MODEL = 'Xenova/all-MiniLM-L6-v2';

// Module-level promises: created once per page load, no matter how many
// times React calls the effect. This is what fixes the StrictMode double-run.
let dataPromise = null;
let modelPromise = null;

export function loadData() {
  if (!dataPromise) {
    dataPromise = (async () => {
      const [meta, items, buf] = await Promise.all([
        fetch('/data/meta.json').then((r) => r.json()),
        fetch('/data/emoji.json').then((r) => r.json()),
        fetch('/data/vectors_int8.bin').then((r) => r.arrayBuffer()),
      ]);
      const Q = new Int8Array(buf);
      if (Q.length !== meta.count * meta.dims) {
        throw new Error('vector file does not match meta.json');
      }
      return { meta, items, Q };
    })();
  }
  return dataPromise;
}

export function loadModel(onProgress) {
  if (!modelPromise) {
    modelPromise = pipeline('feature-extraction', MODEL, {
      dtype: 'q8',
      progress_callback: onProgress,
    });
  }
  return modelPromise;
}

// Scores are dot products against int8 rows, so they are the true cosine
// multiplied by (127 / scale). That constant is the same for every row, so
// it cannot change the ranking — we only divide it out for display.
export function rank({ Q, meta }, qv, k = 24) {
  const { count: n, dims: d, scale } = meta;
  const scores = new Float32Array(n);

  for (let i = 0; i < n; i++) {
    let s = 0;
    const off = i * d;
    for (let j = 0; j < d; j++) s += Q[off + j] * qv[j];
    scores[i] = s;
  }

  const order = Array.from(scores.keys()).sort((a, b) => scores[b] - scores[a]);
  const k2 = scale / 127;
  return order.slice(0, k).map((i) => ({ i, score: scores[i] * k2 }));
}