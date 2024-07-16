const Web3 = require('web3');
const fs = require('fs');
const path = require('path');
require('dotenv').config(); // Đọc tệp .env

// URL mạng Ethereum của Ganache
const ganacheUrl = process.env.GANACHE_URL || 'http://127.0.0.1:7545';
const web3 = new Web3(new Web3.providers.HttpProvider(ganacheUrl));

// Địa chỉ của smart contract đã triển khai (lấy từ biến môi trường)
const contractAddress = process.env.CONTRACT_ADDRESS;

// ABI của smart contract
const contractAbi = JSON.parse(fs.readFileSync(path.resolve(__dirname, './build/contracts/SimpleStorage.json'), 'utf-8')).abi;

const contract = new web3.eth.Contract(contractAbi, contractAddress);

// Địa chỉ tài khoản cố định từ biến môi trường
const account = process.env.ACCOUNT_ADDRESS;

// Tương tác với smart contract
async function interactWithContract() {
    try {
        // Gọi hàm set() của smart contract
        const setValue = await contract.methods.set(42).send({ from: account });
        console.log('Set value transaction:', setValue);

        // Gọi hàm get() của smart contract
        const getValue = await contract.methods.get().call();
        console.log('Stored value:', getValue);
    } catch (error) {
        console.error('Error interacting with contract:', error);
    }
}

interactWithContract();
