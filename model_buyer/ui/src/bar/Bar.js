
import React, { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';


class SimpleAppBar extends Component {
  render() {
      return (
    <div className="SimpleAppBar">
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" color="inherit">
            Model Buyer
          </Typography>
        </Toolbar>
      </AppBar>
    </div>
  );
  }
}

export default SimpleAppBar;
