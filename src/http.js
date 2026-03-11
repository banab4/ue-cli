export async function request(method, path, body, options = {}) {
  const url = `${options.host}${path}`;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), options.timeout || 5000);

  try {
    if (options.verbose) {
      console.error(`> ${method} ${url}`);
      if (body) console.error(`> ${JSON.stringify(body)}`);
    }

    const fetchOptions = {
      method,
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json' },
    };

    if (body !== undefined && body !== null) {
      fetchOptions.body = JSON.stringify(body);
    }

    const res = await fetch(url, fetchOptions);

    if (options.verbose) {
      console.error(`< ${res.status} ${res.statusText}`);
    }

    const text = await res.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }

    if (!res.ok) {
      return {
        ok: false,
        status: res.status,
        error: typeof data === 'string' ? data : JSON.stringify(data),
        code: 'HTTP_ERROR',
      };
    }

    return { ok: true, data };
  } catch (err) {
    if (err.name === 'AbortError') {
      return { ok: false, error: `Request timed out after ${options.timeout}ms`, code: 'TIMEOUT_ERROR' };
    }
    return { ok: false, error: err.message, code: 'CONNECTION_ERROR' };
  } finally {
    clearTimeout(timeoutId);
  }
}
