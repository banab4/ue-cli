import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';

const DEFAULT_REGISTRY = 'https://raw.githubusercontent.com/banab4/ue-cli/main/discovery';
const CONFIG_PATH = join(homedir(), '.ue-cli.json');

function loadConfig() {
  try {
    return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
  } catch {
    return {};
  }
}

export function getRegistries() {
  const config = loadConfig();
  const additional = Array.isArray(config.registries) ? config.registries : [];
  const cleaned = additional
    .filter(r => typeof r === 'string' && r.length > 0)
    .map(r => r.replace(/\/+$/, ''));
  return [...cleaned, DEFAULT_REGISTRY];
}

export async function fetchMergedIndex() {
  const registries = getRegistries();
  const results = await Promise.all(
    registries.map(async (url) => {
      try {
        const res = await fetch(`${url}/index.json`);
        if (!res.ok) return null;
        return await res.json();
      } catch {
        return null;
      }
    })
  );

  const seenObjects = new Set();
  const mergedObjects = [];
  const seenScripts = new Set();
  const mergedScripts = [];
  let version = null;

  for (const index of results) {
    if (!index) continue;
    if (!version) version = index.version;

    for (const obj of (index.objects || [])) {
      if (!seenObjects.has(obj.objectPath)) {
        seenObjects.add(obj.objectPath);
        mergedObjects.push(obj);
      }
    }

    for (const script of (index.scripts || [])) {
      if (!seenScripts.has(script.name)) {
        seenScripts.add(script.name);
        mergedScripts.push(script);
      }
    }
  }

  if (mergedObjects.length === 0 && mergedScripts.length === 0) return null;

  return { version: version || '0.0.0', objects: mergedObjects, scripts: mergedScripts };
}

export async function fetchFromRegistries(subPath) {
  const registries = getRegistries();
  for (const url of registries) {
    try {
      const res = await fetch(`${url}/${subPath}`);
      if (res.ok) return await res.text();
    } catch {
      continue;
    }
  }
  return null;
}
