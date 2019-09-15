module.exports = {
  env: {
    browser: true,
    es6: true
  },
  extends: ["airbnb", "plugin:react/recommended"],
  globals: {
    Atomics: "readonly",
    SharedArrayBuffer: "readonly"
  },
  parser: "babel-eslint",
  plugins: ["react"],
  rules: {
    "no-param-reassign": ["error", { "props": true, "ignorePropertyModificationsFor": ["action"] }]
  }
};
