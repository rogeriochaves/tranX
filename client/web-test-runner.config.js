const { importMapsPlugin } = require("@web/dev-server-import-maps");

process.env.NODE_ENV = "test";

module.exports = {
  plugins: [
    require("@snowpack/web-test-runner-plugin")(),
    importMapsPlugin({
      inject: {
        importMap: {
          imports: {
            "/_snowpack/pkg/axios.v0.21.1.js": "/src/mocks/axios.js",
          },
        },
      },
    }),
  ],
};
