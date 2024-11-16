
type SongCardProps = {
    song_name: string;
    artist: string;
    album_cover: string;
}

const SongCard = ( {song_name, artist, album_cover}: SongCardProps) => {    
    return (
        <div className="tileRow"> 
            <div className="tile">
                <div className = "album_cover">
                    <img src={album_cover}/>
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
        </div>
    );
};

export default SongCard;