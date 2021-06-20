import proxy from "http2-proxy";
import finalhandler from "finalhandler";

const defaultWebHandler = (err, req, res) => {
  if (err) {
    console.error("proxy error", err);
    finalhandler(req, res)(err);
  }
};

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
      src: "/api/.*",
      dest: (req, res) =>
        proxy.web(
          req,
          res,
          {
            hostname: "localhost",
            port: 8081,
          },
          defaultWebHandler
        ),
    },
  ],
};
