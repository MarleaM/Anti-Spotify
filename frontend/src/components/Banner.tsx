import React from "react";
import {useState} from 'react';
import {Container, Row, Col} from "react-bootstrap";
import axios from 'axios';


const Banner = () => {
    const [quote, setQuote] = useState('');
    const [searchSong, setSearchSong] = useState('');
    /*
    const handleInput = (event) => {
        setSearchSong(event.target.value);
    };
    */
    const getQuote = () => {
        axios.get('http://api.quotable.io/random')
        .then(response => {
            console.log(response.data.content) /** get just the quote */
            setQuote(response.data.content)
        }).catch(err => {
            console.log(err)
        })
    }
    return (
        <section className="banner" id="home">
            <Container>
                <Row className = "align-items-center">
                    <Col>
                        <span className="tagline"> Anti-Spotify </span>
                        <div className="input-container">
                            <input 
                                type="text" 
                                placeholder="Enter a song" 
                                value={searchSong}
                                //onChange={handleInput} this will be for when we do our api call
                            />
                            <button onClick={getQuote}>
                                Search
                            </button>
                            { quote ? <h1>{quote}</h1> : null }
                        </div>
                    </Col>
                </Row>
            </Container>
        </section>
    );
};

export default Banner;