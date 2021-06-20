import proxy from "http2-proxy";

// Snowpack Configuration File
// See all supported options: https://www.snowpack.dev/reference/configuration

/** @type {import("snowpack").SnowpackUserConfig } */
export default {
  packageOptions: {
    polyfillNode: true,
  },
  plugins: ["@snowpack/plugin-typescript"],
  routes: [
    {
      src: "/run",
      dest: (req, res) => {
        return proxy.web(req, res, {
          hostname: "localhost",
          port: 8081,
        });
      },
    },
  ],
};
