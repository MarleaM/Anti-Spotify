
type SongCardProps = {
    song_name: string;
    artist: string;
    album_cover: string;
}

const MainSongCard = ( {song_name, artist, album_cover}: SongCardProps) => {    
    return (
        <div className="main-song-card">
                <div className = "main-album-cover">
                    <a href ="https://github.com/MarleaM/OSS_Project" target ="_blank">
                        <img src={album_cover}/>
                    </a>
                </div>
            <div className="main-song-info">
                <h2>
                    {song_name}
                </h2>
                <h2>
                    By {artist}
                </h2>
            </div>
        </div>
    );
};

export default MainSongCard;