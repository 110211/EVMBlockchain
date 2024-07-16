import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AdminPanel from './components/AdminPanel';
import Blocks from './components/Blocks';
import Transactions from './components/Transactions';
import { Navbar, NavbarBrand, Nav, NavItem, NavLink, Container } from 'reactstrap';

const App = () => {
  return (
    <Router>
      <div>
        <Navbar color="dark" dark expand="md">
          <Container>
            <NavbarBrand href="/">Admin Panel</NavbarBrand>
            <Nav className="ml-auto" navbar>
              <NavItem>
                <NavLink href="/">Home</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="/blocks">Blocks</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="/transactions">Transactions</NavLink>
              </NavItem>
            </Nav>
          </Container>
        </Navbar>
        <Routes>
          <Route path="/" element={<AdminPanel />} />
          <Route path="/blocks" element={<Blocks />} />
          <Route path="/transactions" element={<Transactions />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
