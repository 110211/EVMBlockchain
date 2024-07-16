# Dự Án Blockchain với Ganache và Web3.js

## Giới thiệu
Dự án này nhằm mục đích triển khai và tương tác với một smart contract đơn giản trên mạng Ethereum cục bộ sử dụng Ganache và Web3.js. Chúng tôi đã sử dụng Truffle để quản lý quá trình triển khai hợp đồng thông minh.

## Yêu cầu
- Node.js và npm
- Ganache
- Truffle
- Web3.js

## Cài đặt và Cấu hình

### 1. Cài đặt và Khởi động Ganache
1. Tải và cài đặt Ganache từ [trang web chính thức](https://www.trufflesuite.com/ganache).
2. Khởi động Ganache và chọn "Quickstart Ethereum" để tạo một mạng Ethereum cục bộ.
3. Lấy URL mạng (thường là `http://127.0.0.1:7545`) và danh sách các tài khoản với địa chỉ và số dư tương ứng.

### 2. Cài đặt Web3.js
```sh
npm install web3
