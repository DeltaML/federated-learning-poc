import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Client from '../utils/ClientApi'
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis,} from 'recharts';
import styles from './styles'
import model from './model'

class RequirementsForm extends React.Component {
    state = {
        weight_id: 0,
        model_type: 'LINEAR_REGRESSION',
        model_id: '',
        weights: [],
        active_update: false,
        data_chart: [],
        model: model
    };

    handleSubmit = (e) => {
        e.preventDefault();
        // get our form data out of state
        this.setState(state => {
            const model = this.buildModel(state);
            return {
                model
            };
        });
        const data = JSON.stringify(this.state.model)
        Client.sendOrderModel(data)
            .then(resp => {
                const model_id = resp.model.id
                this.setState({model_id: model_id, active_update: true})
            })

    }


    handleChange = event => {
        this.setState({model_type: event.target.value})
    };

    buildModel(state) {

        state.model.model_type = state.model_type
        return state.model
    }

    updateWeights(update) {
        this.setState(state => {
            const value = {error: update.MSE, values: update.values, weight_id: state.weight_id}
            const weight_id = state.weight_id + 1;
            const weights = state.weights.concat(value);
            const data_chart = state.data_chart.concat({name: state.weight_id, MSE: update.MSE});
            return {
                weights: weights,
                data_chart: data_chart,
                weight_id
            }
        });
    }


    tick() {
        if (this.state.active_update) {
            var prediction = {
                model_id: this.state.model_id
            }
            const data = JSON.stringify(prediction)
            Client.sendPing(data).then(resp => {
                this.updateWeights(resp)
            })
        }
    }


    componentDidMount() {
        this.interval = setInterval(() => this.tick(), 1000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    handleClick () {
        console.log(this.state.active_update)
         this.setState({active_update: false})
        console.log(this.state.active_update)
    }

    render() {
        const {classes} = this.props;

        return (
            <div className={classes.root}>
                <Grid container>
                    <Grid item xs={4}>
                        <form className={classes.container} noValidate autoComplete="off" onSubmit={this.handleSubmit}>
                            <div>
                                <TextField
                                    id="model-id"
                                    label="Model ID"
                                    defaultValue=""
                                    className={classes.textField}
                                    margin="normal"
                                    InputProps={{
                                        readOnly: true,
                                    }}
                                    value={this.state.model_id}
                                    variant="outlined"
                                />
                            </div>
                            <div>
                                <FormControl className={classes.formControl}>

                                    <InputLabel htmlFor="model-type">Model Type</InputLabel>
                                    <Select
                                        value={this.state.model_type}
                                        defaultValue="NONE"
                                        onChange={this.handleChange}

                                    >
                                        <MenuItem value="">
                                            <em>None</em>
                                        </MenuItem>
                                        <MenuItem value="LINEAR_REGRESSION">Linear Regression</MenuItem>
                                    </Select>
                                </FormControl>
                            </div>
                            <div>
                                <Button variant="contained"
                                        color="primary"
                                        className={classes.button}
                                        type="submit">

                                    Run
                                </Button>
                                <Button variant="contained"
                                        color="secondary"
                                        className={classes.button}
                                        onClick={(e) => this.handleClick(e)}>

                                    Stop
                                </Button>
                            </div>


                        </form>
                    </Grid>
                    <Grid item xs={4}>
                        <LineChart
                            width={500}
                            height={300}
                            data={this.state.data_chart}
                            margin={{
                                top: 5, right: 30, left: 20, bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="name"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <Line type="monotone" dataKey="MSE" stroke="#8884d8" activeDot={{r: 8}}/>
                        </LineChart>
                    </Grid>
                    <Grid item xs={4}>
                        <Paper className={classes.root}>
                            <Table className={classes.table}>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>#</TableCell>
                                        <TableCell align="right">Values</TableCell>
                                        <TableCell align="right">MSE</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {this.state.weights.map(row => (
                                        <TableRow key={row.weight_id}>
                                            <TableCell component="th" scope="row">
                                                {row.weight_id}
                                            </TableCell>
                                            <TableCell align="right">{row.values}</TableCell>
                                            <TableCell align="right">{row.error}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </Paper>
                    </Grid>
                </Grid>


            </div>

        );
    }
}

RequirementsForm.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(RequirementsForm);