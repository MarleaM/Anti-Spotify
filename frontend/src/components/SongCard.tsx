import { useRef, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faPause } from '@fortawesome/free-solid-svg-icons';

type SongCardProps = {
  song_name: string;
  artist: string;
  album_cover: string;
  preview_url: string;
  link_url: string;
};

const SongCard = ({ song_name, artist, album_cover, preview_url, link_url}: SongCardProps) => {
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
        <div className="tileRow">
            <div className="tile">
                <div className="album_cover">
                    <a href ={link_url} target ="_blank">
                        <img src={album_cover} alt={`${song_name} album cover`} />
                    </a>
                </div>
                <div className="song_info">
                    <p>
                        Name: {song_name}
                    </p>
                    <p>
                        Artist: {artist}
                    </p>
                </div>
            </div>
        {preview_url && (
        <div className="preview-btn-container">
            <button className="preview-btn" onClick={handlePlayPause}>
                <FontAwesomeIcon icon={isPlaying ? faPause : faPlay} />
            </button>
        <audio ref={audioRef} controls={false}>
           <source src={preview_url} type="audio/mpeg" />
        </audio>
        </div>
        )}
    </div>
    );
};

export default SongCard;
