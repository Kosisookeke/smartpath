import { render, screen } from '@testing-library/react';
import App from './App';

test('renders SmartPath application', () => {
  render(<App />);
  // Check if the app renders without crashing
  const appElement = screen.getByText(/SmartPath|Learning|Login|Sign/i);
  expect(appElement).toBeInTheDocument();
});

test('App component is defined', () => {
  expect(App).toBeDefined();
});
