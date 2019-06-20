import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Client from '../utils/ClientApi'
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
//TAble
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
// FIle upload imports
import classNames from 'classnames';
import CircularProgress from '@material-ui/core/CircularProgress';
import Fab from '@material-ui/core/Fab';
import CheckIcon from '@material-ui/icons/Check';
import SaveIcon from '@material-ui/icons/Save';
// Chars
import {CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis,} from 'recharts';
import model from './model'
import styles from "./styles";
import {withStyles} from "@material-ui/core/styles/index";

class RequirementsForm extends React.Component {
    state = {
        weight_id: 0,
        model_type: 'LINEAR_REGRESSION',
        model_id: '',
        weights: [],
        active_update: false,
        data_chart: [],
        model: model,
        loadStatus: {
            loading: false,
            success: false,
        },
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
            data.append('filename', file.name)
            this.setState({
                uploadedFile: file,
                uploadedFileName: file.name
            });
            console.log(data.get('file').size);
            //console.log(Client.getClientId())
            Client.sendFile({body: data}, res => {
                if (res.status !== 200) {
                    console.log("ERROR")
                }
            })
        }
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
        state.model.file_name = state.uploadedFileName
        state.model.model_type = state.model_type
        return state.model
    }

    updateWeights(data) {
        this.setState(state => {
            const value = {error: data.mse, values: data.values, weight_id: state.weight_id}
            const weight_id = state.weight_id + 1;
            const weights = state.weights.slice().concat(value);
            const data_chart = state.data_chart.slice().concat({name: state.weight_id, MSE: data.mse});
            const modelIsFinished = data.model.model.status === "FINISHED";
            return {
                weights: weights,
                data_chart: data_chart,
                weight_id: weight_id
            }
        });
    }


    tick() {
        if (this.state.active_update) {
            var prediction = {
                model_id: this.state.model_id
            }
            const data = JSON.stringify(prediction)
            Client.sendPrediction(data).then(resp => {
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

    handleClick() {
        console.log(this.state.active_update)
        this.setState({active_update: false})
        console.log(this.state.active_update)
    }

    render() {
        const {classes} = this.props;
        const {loading, success} = this.state.loadStatus;
        const buttonClassname = classNames({
            [classes.buttonSuccess]: success,
        });
        return (
            <Grid container>
                <Grid item container direction="column" xs={12} sm={6} lg={4} xl={3} className={classes.container}>
                    <Paper style={{padding: 24}}>
                        <form noValidate autoComplete="off" onSubmit={this.handleSubmit}>
                            <Grid item xs>
                                <TextField
                                    id="model-id"
                                    label="Model ID"
                                    defaultValue=""
                                    margin="normal"
                                    InputProps={{
                                        readOnly: true,
                                    }}
                                    value={this.state.model_id}
                                    className={classes.textField}
                                />
                            </Grid>
                            <Grid item xs>
                                <FormControl className={classes.formControl}>

                                    <InputLabel shrink htmlFor="model-type">Model Type</InputLabel>
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
                            </Grid>
                            <Grid item xs>
                                <TextField
                                    id="outlined-name"
                                    label="Name"
                                    value={"asd"}
                                    margin="normal"
                                />
                            </Grid>
                            <Grid item xs style={{padding: 24}}>
                                <div className={classes.root}>
                                    <input accept="*/*" className={classes.input} id="contained-button-file" type="file"
                                           onChange={this.loadFile}/>
                                    <div className={classes.wrapper}>
                                        <label htmlFor="contained-button-file">
                                            <Fab color="primary" component="span" className={buttonClassname}
                                                 onClick={this.handleButtonClick}>
                                                {success ? <CheckIcon/> : <SaveIcon/>}
                                            </Fab>
                                        </label>
                                        {loading && <CircularProgress size={68} className={classes.fabProgress}/>}
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
                                        {loading && <CircularProgress size={24} className={classes.buttonProgress}/>}
                                    </div>
                                </div>
                                <Button variant="contained"
                                        color="primary"
                                        type="submit">

                                    Run
                                </Button>
                                <Button variant="contained"
                                        color="secondary"
                                        onClick={(e) => this.handleClick(e)}>
                                    Stop
                                </Button>
                            </Grid>
                        </form>
                    </Paper>

                </Grid>
                <Grid item xs={12} sm={6} lg={4} xl={3} style={{padding: 24}}>
                    <Paper style={{padding: 24}}>
                        <LineChart
                            width={500}
                            height={300}
                            data={this.state.data_chart}

                        >
                            <CartesianGrid strokeDasharray="3 3"/>
                            <XAxis dataKey="name"/>
                            <YAxis/>
                            <Tooltip/>
                            <Legend/>
                            <Line type="monotone" dataKey="MSE" stroke="#8884d8" activeDot={{r: 8}}/>
                        </LineChart>
                    </Paper>

                </Grid>
                <Grid item xs={12} sm={6} lg={4} xl={3} style={{padding: 24}}>
                    <Paper style={{padding: 24}}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>#</TableCell>
                                    {/*<TableCell align="right">Values</TableCell>*/}
                                    <TableCell align="right">MSE</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {this.state.weights.map(row => (
                                    <TableRow key={row.weight_id}>
                                        <TableCell component="th" scope="row">
                                            {row.weight_id}
                                        </TableCell>
                                        {/*<TableCell align="right">{row.values}</TableCell>*/}
                                        <TableCell align="right">{row.error}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Paper>
                </Grid>
            </Grid>
        );
    }
}


RequirementsForm.propTypes = {
    classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(RequirementsForm);