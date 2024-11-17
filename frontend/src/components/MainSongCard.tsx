
type SongCardProps = {
    song_name: string;
    artist: string;
    album_cover: string;
    link_url: string;
}

const MainSongCard = ( {song_name, artist, album_cover, link_url}: SongCardProps) => {    

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
            </div>
        </div>
    );
};

export default MainSongCard;