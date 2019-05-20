import React, {PureComponent} from 'react';
import {CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis,} from 'recharts';
import Client from '../utils/ClientApi'

class Char extends PureComponent {


    constructor(props) {
        super(props);
        console.log(props.weights)
        this.state = {
            data: [
                {name: 0, MSE: 0}
            ],
            weights: [props.weights]
        };

    }

    tick() {
        console.log(this.state.weights)
        this.setState(state => {
            const data = this.buildData(state);
            //Client.sendPing(data)
            return {
                data
            };
        });

    }

    buildData(state) {
        const newLength = state.data.length + 1;
        var RandomNumber = Math.floor(Math.random() * 100) + 1
        const value = {name: newLength, MSE: RandomNumber};
        const oldData = state.data.slice();
        return oldData.concat(value);
    }

    componentDidMount() {
        this.interval = setInterval(() => this.tick(), 2000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }


    render() {
        return (
            <Paper className={classes.root}>
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
                    </Paper>
        );
    }
}

export default Char;
