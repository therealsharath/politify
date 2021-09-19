import * as React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Slide from '@material-ui/core/Slide';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export default function DisabledDialog() {
  const [open, setOpen] = React.useState(true);

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Dialog
        open={open}
        TransitionComponent={Transition}
        keepMounted
        onClose={handleClose}
        aria-describedby="alert-dialog-slide-description"
      >
        <DialogTitle>{"Oops! We're broke 🥺"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-slide-description">
            This project is currently unusable because we have no way to keep our servers running.
            We are extremely sorry about this; but it isn't all bad! Take a look at our UI and also
            checkout the project in action by clicking the button below.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button href="https://devpost.com/software/politify-3xhpml" onClick={handleClose}>Check out project</Button>
          <Button onClick={handleClose}>Continue to site</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}