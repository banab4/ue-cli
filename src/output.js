function print(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

export const output = {
  success(verb, request, response) {
    print({ ok: true, verb, request, response });
  },

  dryRun(verb, method, url, body) {
    print({ ok: true, dryRun: true, verb, method, url, body });
  },

  error(verb, message, code) {
    print({ ok: false, verb, error: message, code });
  },
};
