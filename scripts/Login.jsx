import React, { useState} from 'react'
import { Modal } from 'react-bootstrap';
import {GoogleButton} from './GoogleButton';


export function Login() {
  const [display, set_display] = useState(false);
  const close_handler = () => set_display(false);
  window.onload=function(){
    set_display(true);
    };
  
  return (
    <div>
      <Modal show={display} onHide={close_handler} animation={false} size={'xl'} backdrop="static" keyboard={false}>
        <Modal.Body><div onClick={close_handler}><GoogleButton /> </div></Modal.Body>
      </Modal>
    </div>
  );
}
