import { useState, useRef, useEffect, useCallback } from 'react';
import { Container, Row, Col } from "react-bootstrap";
import axios from 'axios';
import AntiSongColumn from "./SongRows.tsx";
import debounce from 'lodash.debounce';

type Song = {
    song_name: string;
    artist: string;
    album_cover: string;
    preview_url: string;
    link_url: string;
}

const Banner = () => {
    const [antiSongs, setAntiSongs] = useState<Song[]>([]);
    const [searchSong, setSearchSong] = useState('');
    const [searchedSong, setSearchedSong] = useState('');
    const [loading, setLoading] = useState(false);
    const [suggestions, setSuggestions] = useState<Song[]>([]);
    const searchBoxRef = useRef<HTMLDivElement | null>(null);

    const getAntiSongs = (songName: string) => {
        if (!songName) return;
        setLoading(true);
        axios.get(`http://localhost:8080/api/users?song_name=${songName}`)
            .then(response => {
                setAntiSongs(response.data.songs)
                setSearchedSong(songName); // Update the searched song name
                setSearchSong('');
            })
            .catch(err => {
                console.log(err)
            })
            .finally(() => {
                setLoading(false);
            });
    };

    const getSuggestions = (searchInput: string) => {
        if (!searchInput.trim()) {
            setSuggestions([]);
            return;
        }
        axios
            .get(`http://localhost:8080/api/suggestions?query=${searchInput}`)
            .then((response) => {
                setSuggestions(response.data.suggestions);
            })
            .catch((err) => {
                console.error("Error fetching suggestions:", err);
            });
    };


    const debouncedGetSuggestions = useCallback(
        debounce((value: string) => {
            getSuggestions(value);
        }, 300), // 300ms delay
        []
    );

    useEffect(() => {
        return () => {
            debouncedGetSuggestions.cancel();
        };
    }, [debouncedGetSuggestions]);

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        // Check if the blur event is happening due to a click inside the suggestions
        if (searchBoxRef.current && searchBoxRef.current.contains(e.relatedTarget)) {
            return;
        }
        setSuggestions([]); // Hide suggestions if clicked outside
    };

    return (
        <section className="banner" id="home">
            <Container>
                <Row className="align-items-center">
                    <Col>
                        <span className="tagline">
                            Anti-Spotify
                        </span>
                        <div className="input-container">
                            <input
                                type="text"
                                placeholder="Enter a song"
                                value={searchSong}
                                onChange={(e) => {
                                    const value = e.target.value;
                                    setSearchSong(value);
                                    debouncedGetSuggestions(value);
                                }}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter') {
                                        getAntiSongs(searchSong);
                                        setSuggestions([]);
                                    }
                                }}
                                onBlur={handleBlur}
                                onFocus={() => getSuggestions(searchSong)}
                            />
                            <button onClick={() => {
                                getAntiSongs(searchSong);
                                setSuggestions([]);
                            }}
                            >
                                {loading ? `Searching...` : `Search`}
                            </button>
                            {suggestions.length > 0 && (
                                <div
                                    className="search_suggestion"
                                    ref={searchBoxRef}
                                >
                                    {suggestions.map((data, index) => (
                                        <div
                                            key={index}
                                            className="suggestion-row"
                                            onMouseDown={(e) => {
                                                e.preventDefault();
                                            }}
                                            onClick={() => {
                                                setSearchSong(data.song_name);
                                                getAntiSongs(data.song_name);
                                                setSuggestions([]);
                                            }}
                                        >
                                            <span className="song-name">{data.song_name}</span>
                                            <span className="artist-name">{data.artist}</span>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                        <div className="song-card-container" >
                            {antiSongs.length > 0 && !loading && (
                                <AntiSongColumn antiSongs={antiSongs} />)
                            }
                        </div>
                    </Col>
                </Row>
            </Container>
        </section>
    );
};

export default Banner;