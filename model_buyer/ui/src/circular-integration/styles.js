import green from '@material-ui/core/colors/green';

const styles = theme => ({
    root: {
      display: 'flex',
      alignItems: 'center',
      margin: theme.spacing.unit,
    },
    wrapper: {
      margin: theme.spacing.unit,
      position: 'relative',
    },
    buttonSuccess: {
      backgroundColor: green[500],
      '&:hover': {
        backgroundColor: green[700],
      },
    },
    fabProgress: {
      color: green[500],
      position: 'absolute',
      top: -6,
      left: -6,
      zIndex: 1,
    },
    buttonProgress: {
      color: green[500],
      position: 'absolute',
      top: '50%',
      left: '50%',
      marginTop: -12,
      marginLeft: -12,
    },
    input: {
      display: 'none',
    },
  });

  export default styles;