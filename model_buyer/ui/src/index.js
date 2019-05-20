import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import theme from './utils/themes';
import CssBaseline from '@material-ui/core/CssBaseline';
import { MuiThemeProvider } from '@material-ui/core/styles';

ReactDOM.render(
    <MuiThemeProvider theme={theme}>
    {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
    <CssBaseline />
    <App />
  </MuiThemeProvider>,
  document.getElementById('root')
);
