import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import SimpleAppBar from '../bar/Bar'
import Chart from '../chart/Chart'
import RequirementsForm from '../requirements-form/RequirementsForm'

const styles = theme => ({
    root: {
        flexGrow: 1,
    },

    control: {
        padding: theme.spacing.unit * 2,
    },
});

class Home extends React.Component {
    state = {
        spacing: '16',
    };


    render() {
        const {classes} = this.props;

        return <div>
            <SimpleAppBar/>

            <Grid container className={classes.root} spacing={16}>
                <Grid item>
                    <Grid container className={classes.demo} spacing={16}>
                        <Grid item>
                            <RequirementsForm/>
                        </Grid>
                        <Grid item>
                            <Chart/>
                        </Grid>
                    </Grid>
                </Grid>

            </Grid>
        </div>;
    }
}

Home.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Home);
