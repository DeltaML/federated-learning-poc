import styles from "../requirements-form/styles";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {withStyles} from "@material-ui/core/styles/index";

class Partials extends React.Component {

    render() {
        return (


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
        );
    }
}


export default withStyles(styles)(Partials);


