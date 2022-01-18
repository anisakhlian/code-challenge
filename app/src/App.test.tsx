import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

test('renders default editor hello world', () => {
  const { getByText } = render(<App />);
  const helloWorldText = getByText(/Hello world!/i);
  expect(helloWorldText).toBeInTheDocument();
});
