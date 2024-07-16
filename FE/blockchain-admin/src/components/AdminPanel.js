import React, { useState, useEffect } from 'react';
import web3 from '../utils/web3';
import SimpleStorageABI from '../build/contracts/SimpleStorage.json';
import { Toast, ToastBody, ToastHeader, Spinner } from 'reactstrap';
import {  Container, Row, Col, Label, Input, Button } from 'reactstrap';

const contractAddress = '0x4db09e17d6da3e8c20daa3e12d99cdee3cd0b121';
const contract = new web3.eth.Contract(SimpleStorageABI.abi, contractAddress);

const AdminPanel = () => {
  const [account, setAccount] = useState('');
  const [storedValue, setStoredValue] = useState('');
  const [newValue, setNewValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [toastMessage, setToastMessage] = useState('');

  useEffect(() => {
    const loadAccount = async () => {
      const accounts = await web3.eth.getAccounts();
      setAccount(accounts[0]);
    };
    loadAccount();
  }, []);




  const getValue = async () => {
    try {
      setLoading(true);
      const value = await contract.methods.get().call();
      setStoredValue(value.toString());
      setLoading(false);
    } catch (error) {
      console.error('Error getting value:', error);
      setLoading(false);
      setToastMessage('Error getting stored value');
    }
  };

  const setValue = async () => {
    if (newValue === '' || isNaN(newValue) || Number(newValue) < 0) {
      setToastMessage('Please enter a valid positive number');
      return;
    }
    try {
      setLoading(true);
      await contract.methods.set(newValue).send({ from: account });
      setNewValue('');
      getValue();
      setToastMessage('Value set successfully');
    } catch (error) {
      console.error('Error setting value:', error);
      setLoading(false);
      setToastMessage('Error setting new value');
    }
  };

  return (
    <div>

      <Container className="mt-5">
  
        <Row className="mt-5 justify-content-center">
          <Col md={8}>
            <h2 className="mb-4">Admin Functions</h2>
            <p>Connected account: <strong>{account}</strong></p>
            <div className="mb-4">
              <h3>Stored Value: <strong>{storedValue}</strong></h3>
              <button className="btn btn-primary" onClick={getValue} disabled={loading}>
                {loading ? <Spinner size="sm" /> : 'Get Stored Value'}
              </button>
            </div>
            <div className="mb-4">
              <Label for="newValue" className="form-label">New Value:</Label>
              <Input
                type="number"
                className="form-control"
                id="newValue"
                value={newValue}
                onChange={(e) => setNewValue(e.target.value)}
                disabled={loading}
              />
              <Button color="success" className="mt-2" onClick={setValue} disabled={loading} block>
                {loading ? <Spinner size="sm" /> : 'Set New Value'}
              </Button>
            </div>
            {toastMessage && (
              <div className="toast show position-fixed bottom-0 end-0 p-3" style={{ zIndex: 1 }}>
                <Toast>
                  <ToastHeader toggle={() => setToastMessage('')}>Notification</ToastHeader>
                  <ToastBody>{toastMessage}</ToastBody>
                </Toast>
              </div>
            )}

          
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default AdminPanel;
