import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faPause } from '@fortawesome/free-solid-svg-icons';
import { useRef, useEffect } from 'react';

/* props for SongCard components (this is what each song card will store) */
type SongCardProps = {
    song_name: string; // name of song
    artist: string; // name of artist
    album_cover: string; // URL of album cover image
    preview_url: string; // URL of song preview audio
    link_url: string; // URL to Spotify's page for the song
    isPlaying: boolean; // keeps track of if a song's preview is currently playing
    onPlayPause: (previewUrl: string | null) => void; // callback to toggle play/pause
};

/* what defines a MainSongCard (same as song card but different styling, used for searched song) */
const MainSongCard = ( {song_name, artist, album_cover, preview_url, link_url, isPlaying, onPlayPause}: SongCardProps) => {    

    // ref for audio element
    const audioRef = useRef<HTMLAudioElement | null>(null);

    // handle play/pause as the isPlaying state changes
    useEffect(() => {
        if (audioRef.current) {
            if (isPlaying) {
                // play audio if song marked as playing
                audioRef.current.play().catch((error) =>
                    console.error("Audio playback error:", error)
                );
            } else {
                // pause audio and reset playback pos if not playing
                audioRef.current.pause();
                audioRef.current.currentTime = 0;
            }
        }
    }, [isPlaying]);

    return (
        <div className="main-song-card">
            {/* Display the album cover, song name, and artist */}
                <div className = "main-album-cover">
                    <a href ={link_url} target ="_blank">
                        <img src={album_cover} alt={`${song_name} album cover`} />
                    </a>
                </div>
            <div className="main-song-info">
                <h2>
                    {song_name}
                </h2>
                <h2>
                    By {artist}
                </h2>
                {/* Only render the preview button and audio element if a preview URL is available */}
                {preview_url && (
                    <div className="main-preview-btn-container">
                        <div>
                            <button
                                className="main-preview-btn"
                                onClick={() => onPlayPause(preview_url)}
                            >
                                <FontAwesomeIcon icon={isPlaying ? faPause : faPlay} />
                            </button>
                        </div>
                        <audio ref={audioRef} controls={false}>
                            <source src={preview_url} type="audio/mpeg" />
                        </audio>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MainSongCard;