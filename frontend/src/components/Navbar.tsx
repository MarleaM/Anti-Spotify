import React from "react";
import {useState} from 'react';
import {Container, Row, Col} from "react-bootstrap";
import axios from 'axios';
import { FaGithub } from "react-icons/fa";


const Navbar = () => {
    return (
        <div className="github-button" style = {{color: "white"}}>
            <FaGithub size = {100}/>
        </div>
    )
};
    
export default Navbar;