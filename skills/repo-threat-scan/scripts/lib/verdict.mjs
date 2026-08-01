const SEVERITIES = ['critical', 'high', 'medium', 'low', 'info'];

export function computeVerdict(findings = []) {
  const counts = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };
  for (const f of findings) {
    if (SEVERITIES.includes(f.severity)) counts[f.severity] += 1;
  }
  const weights = { critical: 100, high: 40, medium: 10, low: 2, info: 0 };
  const score = SEVERITIES.reduce((s, k) => s + counts[k] * weights[k], 0);

  let verdict;
  if (counts.critical >= 1 || counts.high >= 2) {
    verdict = 'NO-GO';
  } else if (counts.high === 1 || counts.medium >= 2) {
    verdict = 'CAUTION';
  } else {
    verdict = 'GO';
  }
  return { verdict, score, counts };
}
