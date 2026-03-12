import { parseArgs } from 'node:util';
import { output } from '../output.js';
import { fetchMergedIndex } from '../config.js';

async function fetchDiscovery() {
  return await fetchMergedIndex();
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
       ue-cli discover <keyword>
       ue-cli discover --detail <objectPath>

Options:
  --object <keyword>    Filter by class name (substring match)
  --category <cat>      Filter by category (subsystem, library)
  --detail <objectPath> Show full function signatures for an object
  --help                Show this help

Search:
  ue-cli discover <keyword>  Search objects and scripts by keyword`);
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
      output.error('discover', 'Failed to fetch discovery index from any registry', 'FETCH_ERROR');
      process.exit(1);
    }

    // Search mode: unified search across objects and scripts
    if (positionals[0] && !values.detail && !values.object && !values.category) {
      const query = positionals[0].toLowerCase();

      const matchedObjects = [];
      for (const obj of discovery.objects) {
        const matchedFns = obj.functions.filter(f =>
          f.name.toLowerCase().includes(query) ||
          f.description.toLowerCase().includes(query)
        );
        if (
          obj.class.toLowerCase().includes(query) ||
          obj.description.toLowerCase().includes(query) ||
          matchedFns.length > 0
        ) {
          matchedObjects.push({
            objectPath: obj.objectPath,
            class: obj.class,
            description: obj.description,
            matchedFunctions: matchedFns.map(f => f.name),
          });
        }
      }

      const matchedScripts = (discovery.scripts || []).filter(s =>
        s.name.toLowerCase().includes(query) ||
        s.description.toLowerCase().includes(query)
      );

      output.success('discover', { search: positionals[0] }, {
        query: positionals[0],
        objects: matchedObjects,
        scripts: matchedScripts,
      });
      return;
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
