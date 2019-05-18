import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';

import SimpleAppBar from '../bar/Bar'

import RequirementsForm from '../requirements-form/RequirementsForm'

const styles = theme => ({
    root: {
        flexGrow: 1,
    }
});

class Home extends React.Component {
    state = {
        spacing: '16',
    };


    render() {
        const {classes} = this.props;

        return <div className={classes.root}>
            <SimpleAppBar/>
            <RequirementsForm/>
        </div>;
    }
}

Home.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Home);
