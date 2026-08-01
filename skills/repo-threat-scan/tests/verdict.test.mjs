import { test } from 'node:test';
import assert from 'node:assert/strict';
import { computeVerdict } from '../scripts/lib/verdict.mjs';

const f = (severity, confidence = 0.9) => ({
  id: 'x', vector: 'secrets', severity, confidence,
  title: 't', evidence: 'e', tool: 'gitleaks', location: 'a:1',
});

test('any critical => NO-GO', () => {
  const r = computeVerdict([f('critical'), f('low')]);
  assert.equal(r.verdict, 'NO-GO');
});

test('two highs => NO-GO', () => {
  const r = computeVerdict([f('high'), f('high')]);
  assert.equal(r.verdict, 'NO-GO');
});

test('one high => CAUTION', () => {
  const r = computeVerdict([f('high'), f('low')]);
  assert.equal(r.verdict, 'CAUTION');
});

test('several mediums => CAUTION', () => {
  const r = computeVerdict([f('medium'), f('medium'), f('medium')]);
  assert.equal(r.verdict, 'CAUTION');
});

test('only low/info => GO', () => {
  const r = computeVerdict([f('low'), f('info')]);
  assert.equal(r.verdict, 'GO');
});

test('empty => GO', () => {
  const r = computeVerdict([]);
  assert.equal(r.verdict, 'GO');
  assert.equal(r.counts.critical, 0);
});
