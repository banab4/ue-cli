import { parseArgs } from 'node:util';
import { output } from '../output.js';

const DISCOVERY_URL = 'https://raw.githubusercontent.com/banab4/ue-cli/main/discovery/index.json';

async function fetchDiscovery() {
  try {
    const res = await fetch(DISCOVERY_URL);
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

function buildExample(objectPath, func) {
  const parts = ['ue-cli call', objectPath, func.name];
  if (func.params && Object.keys(func.params).length > 0) {
    const example = {};
    for (const [key, schema] of Object.entries(func.params)) {
      if (schema.required) example[key] = `<${schema.type}>`;
    }
    if (Object.keys(example).length > 0) {
      parts.push(`--params '${JSON.stringify(example)}'`);
    }
  }
  if (func.safety === 'WRITE') parts.push('--force');
  return parts.join(' ');
}

export const discoverCommand = {
  help() {
    console.log(`ue-cli discover — Browse available UE objects and functions

Usage: ue-cli discover [options]
       ue-cli discover --detail <objectPath>

Options:
  --object <keyword>    Filter by class name (substring match)
  --category <cat>      Filter by category (subsystem, library)
  --detail <objectPath> Show full function signatures for an object
  --help                Show this help`);
  },

  async execute(positionals, argv, options) {
    const { values } = parseArgs({
      args: argv,
      options: {
        object: { type: 'string' },
        category: { type: 'string' },
        detail: { type: 'string' },
        help: { type: 'boolean', short: 'h' },
      },
      allowPositionals: true,
      strict: false,
    });

    const discovery = await fetchDiscovery();
    if (!discovery) {
      output.error('discover', 'Failed to fetch discovery.json from GitHub', 'FETCH_ERROR');
      process.exit(1);
    }

    // Detail mode: show full signatures for one object
    if (values.detail) {
      const obj = discovery.objects.find(o => o.objectPath === values.detail);
      if (!obj) {
        output.error('discover', `Object not found: ${values.detail}`, 'NOT_FOUND');
        process.exit(1);
      }

      const functions = obj.functions.map(f => ({
        ...f,
        example: buildExample(obj.objectPath, f),
      }));

      output.success('discover', { detail: values.detail }, {
        objectPath: obj.objectPath,
        class: obj.class,
        category: obj.category,
        description: obj.description,
        deprecated: obj.deprecated || false,
        ...(obj.deprecatedBy ? { deprecatedBy: obj.deprecatedBy } : {}),
        functions,
        properties: obj.properties || [],
      });
      return;
    }

    // List mode: show all objects with summaries
    let objects = discovery.objects;

    if (values.object) {
      const keyword = values.object.toLowerCase();
      objects = objects.filter(o => o.class.toLowerCase().includes(keyword));
    }

    if (values.category) {
      objects = objects.filter(o => o.category === values.category);
    }

    const summary = objects.map(o => ({
      objectPath: o.objectPath,
      class: o.class,
      category: o.category,
      description: o.description,
      deprecated: o.deprecated || false,
      functions: o.functions.map(f => f.name),
      properties: (o.properties || []).map(p => p.name),
    }));

    output.success('discover', { filters: { object: values.object || null, category: values.category || null } }, {
      version: discovery.version,
      count: summary.length,
      objects: summary,
    });
  },
};
