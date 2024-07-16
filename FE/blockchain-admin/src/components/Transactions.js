import React, { useState, useEffect } from 'react';
import web3 from '../utils/web3';
import { Container, Row, Col } from 'reactstrap';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTransactions = async () => {
      try {
        const latestBlockNumber = await web3.eth.getBlockNumber();
        const transactionsArray = [];
        for (let i = 0; i <= latestBlockNumber; i++) {
          const block = await web3.eth.getBlock(i, true); // include full transaction objects
          console.log(`Block ${i}:`, block); // Ghi log block để kiểm tra
          if (block && block.transactions && Array.isArray(block.transactions)) {
            block.transactions.forEach(tx => transactionsArray.push(tx));
          }
        }
        console.log('Transactions:', transactionsArray); // Ghi log transactions để kiểm tra
        setTransactions(transactionsArray);
        setLoading(false);
      } catch (error) {
        console.error('Error loading transactions:', error);
        setLoading(false);
      }
    };

    loadTransactions();
  }, []);

  return (
    <Container className="mt-5">
      <Row className="mt-5 justify-content-center">
        <Col md={8}>
          <h3 className="mt-5">Transaction Information</h3>
          {loading ? (
            <p>Loading transactions...</p>
          ) : transactions.length === 0 ? (
            <p>No transactions found.</p>
          ) : (
            <div className="transaction-info">
              {transactions.map((tx, index) => (
                <div key={index} className="transaction">
                  <p><strong>TX Hash:</strong> {tx.hash}</p>
                  <p><strong>From:</strong> {tx.from}</p>
                  <p><strong>To:</strong> {tx.to}</p>
                  <p><strong>Value:</strong> {tx.value}</p>
                  <p><strong>Gas Used:</strong> {tx.gas}</p>
                  <hr />
                </div>
              ))}
            </div>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default Transactions;
