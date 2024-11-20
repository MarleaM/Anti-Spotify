import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faPause } from '@fortawesome/free-solid-svg-icons';
import { useRef, useState } from 'react';

type SongCardProps = {
    song_name: string;
    artist: string;
    album_cover: string;
    preview_url: string;
    link_url: string;
}

const MainSongCard = ( {song_name, artist, album_cover, preview_url, link_url}: SongCardProps) => {    
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);

    const handlePlayPause = () => {
    if (audioRef.current) {
        if (isPlaying) {
        audioRef.current.pause();
        } 
        else {
        audioRef.current.play().catch((error) => {
            console.error('Audio playback error:', error);
        });
        }
        setIsPlaying(!isPlaying);
    }
    };

    return (
        <div className="main-song-card">
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
                {preview_url && (
                <div className = "main-preview-btn-container">
                    <div>
                        <button className="main-preview-btn" onClick={handlePlayPause}>
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