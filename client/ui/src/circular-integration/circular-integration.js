import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import Button from '@material-ui/core/Button';
import Fab from '@material-ui/core/Fab';
import CheckIcon from '@material-ui/icons/Check';
import SaveIcon from '@material-ui/icons/Save';
import styles from './styles'
import Client from '../ClientApi';
const fs = require('fs');


class CircularIntegration extends React.Component {
  state = {
    loading: false,
    success: false,
    uploadedFile: null
  };

  componentWillUnmount() {
    clearTimeout(this.timer);
  }

  handleButtonClick = (event) => {
    if (!this.state.loading) {
      this.setState(
        {
          success: false,
          loading: true,
        },
        () => {
          this.timer = setTimeout(() => {
            this.setState({
              loading: false,
              success: true,
            });
          }, 2000);
        },
      );
    }
  };

  loadFile = (event) => {
      let file = event.target.files[0];
      if (file) {
          let data = new FormData();
          data.append('file', file);
          this.setState({
              uploadedFile: file
          });
          console.log(data.get('file').size);
          Client.sendFile({ body: data}, res => {
              if (res.statusCode !== 200) {
                  console.log("ERROR")
              }
          })
      }
  };

  render() {
    const { loading, success } = this.state;
    const { classes } = this.props;
    const buttonClassname = classNames({
      [classes.buttonSuccess]: success,
    });

    return (
      <div className={classes.root}>
        <input accept="*/*" className={classes.input} id="contained-button-file" type="file" onChange={this.loadFile} />
        <div className={classes.wrapper}>
          <label htmlFor="contained-button-file">
            <Fab color="primary" component="span" className={buttonClassname} onClick={this.handleButtonClick}>
                {success ? <CheckIcon /> : <SaveIcon />}
            </Fab>
          </label>
          {loading && <CircularProgress size={68} className={classes.fabProgress} />}
        </div>
        <div className={classes.wrapper}>
          <label htmlFor="contained-button-file">
            <Button
                variant="contained"
                color="primary"
                className={buttonClassname}
                disabled={loading}
                onClick={this.handleButtonClick}
                component="span"
            >
                Load Dataset
            </Button>
          </label>
          {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
        </div>
      </div>
    );
  }
}

CircularIntegration.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CircularIntegration);