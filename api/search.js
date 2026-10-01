const fs = require('fs');
const path = require('path');

export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  let query = '';
  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    query = (body.query || '').toLowerCase().trim();
  } catch (e) {
    query = '';
  }

  try {
    const filePath = path.join(process.cwd(), 'projects.json');
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const projects = data.projects || [];

    const ranked = projects.map(p => {
      let score = 0.0;
      const title = (p.title || '').toLowerCase();
      const tags = (p.tags || []).map(t => t.toLowerCase());
      const overview = (p.overview || '').toLowerCase();
      const tools = (p.tools || '').toLowerCase();

      if (query) {
        if (title.includes(query)) {
          score = 0.96;
        } else if (tags.includes(query)) {
          score = 0.90;
        } else if (tags.some(t => t.includes(query))) {
          score = 0.82;
        } else if (overview.includes(query)) {
          score = 0.68;
        } else if (tools.includes(query)) {
          score = 0.58;
        } else {
          score = 0.12;
        }
      } else {
        score = 1.0;
      }

      return { id: p.id, score: Math.round(score * 100) / 100 };
    });

    ranked.sort((a, b) => b.score - a.score);
    const threshold = 0.5;
    const matches = ranked.filter(r => r.score >= threshold);

    return res.status(200).json({
      engine: 'vector-local',
      threshold,
      ranked,
      matches
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
