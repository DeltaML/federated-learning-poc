import React from 'react';

import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Client from '../utils/ClientApi'
const styles = theme => ({
    container: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
        width: 200,
    },
    dense: {
        marginTop: 19,
    },
    menu: {
        width: 200,
    },
    button: {
        margin: theme.spacing.unit,
    },
    input: {
        display: 'none',
    },
    root: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    formControl: {
        margin: theme.spacing.unit,
        minWidth: 120,
    },
});


class RequirementsForm extends React.Component {
    state = {
        model_type: '',
        name: 'hai',
        labelWidth: 0,
    };


      handleButtonClick = (event) => {

          Client.sendOrderModel({ body: {}}, res => {
          if (res.statusCode !== 200) {
              console.log("ERROR")
          } else {
              console.log("OK")
          }
      })
  };


    handleChange = event => {
        this.setState({[event.target.name]: event.target.value});
    };


    render() {
        const {classes} = this.props;

        return (
            <form className={classes.container} noValidate autoComplete="off">
                <FormControl className={classes.formControl}>
                    <InputLabel htmlFor="model_type">Model Type</InputLabel>
                    <Select
                        value={this.state.model_type}
                        onChange={this.handleChange}
                        inputProps={{
                            name: 'model_type',
                            id: 'model_type',
                        }}
                    >
                        <MenuItem value="">
                            <em>None</em>
                        </MenuItem>
                        <MenuItem value={"LINEAR_REGRESSION"}>Linear Regression</MenuItem>
                    </Select>
                </FormControl>

                <TextField
                    id="standard-uncontrolled"
                    label="Uncontrolled"
                    defaultValue="foo"
                    className={classes.textField}
                    margin="normal"
                />

                <TextField
                    required
                    id="standard-required"
                    label="Required"
                    defaultValue="Hello World"
                    className={classes.textField}
                    margin="normal"
                />

                <Button variant="contained"
                        color="primary"
                        className={classes.button}
                        onClick={this.handleButtonClick}>

                    Run
                </Button>


            </form>
        );
    }
}

RequirementsForm.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(RequirementsForm);