// migrations/2_deploy_contracts.js

const fs = require('fs');
const path = require('path');
const SimpleStorage = artifacts.require("SimpleStorage");

module.exports = async function(deployer) {
  await deployer.deploy(SimpleStorage);
  const contractAddress = SimpleStorage.address;
  const envPath = path.join(__dirname, '..', '.env');
  
  // Ghi địa chỉ hợp đồng vào tệp .env
  fs.appendFileSync(envPath, `CONTRACT_ADDRESS=${contractAddress}\n`, (err) => {
    if (err) throw err;
    console.log(`Contract address ${contractAddress} saved to .env`);
  });
};
