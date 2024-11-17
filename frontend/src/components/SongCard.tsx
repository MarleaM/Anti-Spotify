import { useRef, useState } from 'react';

type SongCardProps = {
  song_name: string;
  artist: string;
  album_cover: string;
  preview_url: string;
};

const SongCard = ({ song_name, artist, album_cover, preview_url }: SongCardProps) => {
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
                    <img src={album_cover} alt={`${song_name} album cover`} />
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
        <div className="preview-btn-container">
            <button className="preview-btn" onClick={handlePlayPause}>
                {isPlaying ? 'Pause' : 'Preview'}
            </button>
        </div>
        <audio ref={audioRef} controls={false}>
           <source src={preview_url} type="audio/mpeg" />
        </audio>
    </div>
    );
};

export default SongCard;
