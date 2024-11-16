import {useState} from 'react';
import {Container, Row, Col} from "react-bootstrap";
import axios from 'axios';
import AntiSongColumn from "./SongRows.tsx";

type Song = {
    song_name: string;
    artist: string;
    album_cover: string;
}

const Banner = () => {
    const [antiSongs, setAntiSongs] = useState<Song[]>([]);
    const [searchSong, setSearchSong] = useState('');
    const [searchedSong, setSearchedSong] = useState('');

    const getAntiSongs = (songName: string) => {
        if (!songName) return;
        axios.get(`http://localhost:8080/api/users?song_name=${songName}`)
        .then(response => {
            setAntiSongs(response.data.songs)
            setSearchedSong(songName); // Update the searched song name
        })
        .catch(err => {
            console.log(err)
        });
    };
    
    return (
        <section className="banner" id="home">
            <Container>
                <Row className = "align-items-center">
                    <Col>
                        <span className="tagline">
                            Anti-Spotify
                        </span>
                        <div className="input-container">
                            <input 
                                type="text" 
                                placeholder="Enter a song" 
                                value={searchSong}
                                onChange={(e) => setSearchSong(e.target.value)}
                            />
                            <button onClick={() => getAntiSongs(searchSong)}>
                                Search
                            </button>
                        </div>
                        {searchedSong && (
                            <h3 className="searched-song">Results for: {searchedSong}</h3>
                        )}
                        {antiSongs.length > 0 && <AntiSongColumn antiSongs={antiSongs} />}
                    </Col>
                </Row>
            </Container>
        </section>
    );
};

export default Banner;