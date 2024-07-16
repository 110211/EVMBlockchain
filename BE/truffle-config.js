// truffle-config.js
module.exports = {
  networks: {
      development: {
          host: "127.0.0.1",     // Localhost (ganache)
          port: 7545,            // Ganache port
          network_id: "*"        // Any network (default: none)
      },
  },
  compilers: {
      solc: {
          version: "0.8.4",    // Fetch exact version from solc-bin (default: truffle's version)
      }
  } 
};
