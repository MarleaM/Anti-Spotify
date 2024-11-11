import React from "react";
import {useState} from 'react';
import {Container, Row, Col} from "react-bootstrap";
import axios from 'axios';
import anti_song_column from "./AntiSongColumn.tsx";
import AntiSongColumn from "./AntiSongColumn.tsx";


const Banner = () => {
    const [antiSongs, setAntiSongs] = useState<string[]>([]);
    const [searchSong, setSearchSong] = useState('');


    const getAntiSongs = () => {
        axios.get('http://localhost:8080/api/users')
        .then(response => {
            console.log(response.data.users) /* now this is getting information from a python script in the backend */
            setAntiSongs(response.data.users)
        }).catch(err => {
            console.log(err)
        })
    }
    
    return (
        <section className="banner" id="home">
            <Container>
                <Row className = "align-items-center">
                    <Col>
                        <span 
                            className="tagline" 
                            style={{ 
                                pointerEvents: 'none',
                                userSelect: 'none'
                            }}
                        >
                            Anti-Spotify
                        </span>
                        <div className="input-container">
                            <input 
                                type="text" 
                                placeholder="Enter a song" 
                            />
                            <button onClick={getAntiSongs}
                                style={{
                                    userSelect: 'none'
                                }}
                            >
                                Search
                            </button>
                            {antiSongs.length > 0 && <AntiSongColumn antiSongs={antiSongs} />}
                        </div>
                    </Col>
                </Row>
            </Container>
        </section>
    );
};

export default Banner;