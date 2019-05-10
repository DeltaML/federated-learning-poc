import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import SimpleAppBar from '../bar/Bar'

import RequirementsForm from '../requirements-form/RequirementsForm'

const styles = theme => ({
    root: {
        flexGrow: 3,
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

            <Grid container className={classes.root}>
                <Grid item>
                    <Grid container className={classes.demo}>
                        <RequirementsForm/>
                        {/*<Grid item xs={12}>
                            <RequirementsForm/>
                        </Grid>*/}
                        {/*<Grid item xs={12}>
                            {/*<Chart/>
                        </Grid>*/}
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
