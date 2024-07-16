import React, { useState, useEffect } from 'react';
import web3 from '../utils/web3';
import { Container, Row, Col } from 'reactstrap';

const Blocks = () => {
  const [blocks, setBlocks] = useState([]);

  useEffect(() => {
    const loadBlocks = async () => {
      try {
        const latestBlockNumber = await web3.eth.getBlockNumber();
        const blocksArray = [];
        for (let i = 0; i <= latestBlockNumber; i++) {
          const block = await web3.eth.getBlock(i);
          blocksArray.push(block);
        }
        setBlocks(blocksArray);
      } catch (error) {
        console.error('Error loading blocks:', error);
      }
    };

    loadBlocks();
  }, []);

  return (
    <Container className="mt-5">
      <Row className="mt-5 justify-content-center">
        <Col md={8}>
          <h3 className="mt-5">Block Information</h3>
          <div className="block-info">
            {blocks.map((block, index) => (
              <div key={index} className="block">
                <p><strong>Block Number:</strong> {block.number.toString()}</p>
                <p><strong>Timestamp:</strong> {new Date(Number(block.timestamp) * 1000).toLocaleString()}</p>
                <p><strong>Transactions:</strong> {Array.isArray(block.transactions) ? block.transactions.length : 0}</p>
                <hr />
              </div>
            ))}
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default Blocks;
