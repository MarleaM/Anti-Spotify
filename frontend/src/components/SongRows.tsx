/* this is really scuffed */
import SongCard from "./SongCard";
import MainSongCard from "./MainSongCard";

const SongRows = ({ antiSongs }: { antiSongs: { song_name: string; artist: string; album_cover: string; }[] }) => {    
    return (
        <div className="title">
            <div className = "main-song-fade-in">
                <div className="main-song-div">
                        <MainSongCard song_name={antiSongs[0].song_name} artist={antiSongs[0].artist} album_cover={antiSongs[0].album_cover}/>
                </div>
            </div>

            <div className = "song-fade-in">
                <h1>Anti-Recommendations</h1>
                <div className="song-row">
                    <div className="song-card">
                        <SongCard song_name={antiSongs[0].song_name} artist={antiSongs[0].artist} album_cover={antiSongs[0].album_cover}/>
                    </div>
                    <div className="song-card">
                        <SongCard song_name={antiSongs[1].song_name} artist={antiSongs[1].artist} album_cover={antiSongs[1].album_cover}/>
                    </div>
                    <div className="song-card">
                        <SongCard song_name={antiSongs[2].song_name} artist={antiSongs[2].artist} album_cover={antiSongs[2].album_cover}/>
                    </div>
                    <div className="song-card">
                        <SongCard song_name={antiSongs[3].song_name} artist={antiSongs[3].artist} album_cover={antiSongs[3].album_cover}/>
                    </div>
                </div>
            </div>

            <h1>Recommendations</h1>
            <div className = "song-fade-in">
                <div className="song-row">
                    <div className="song-card">
                        <SongCard song_name={antiSongs[4].song_name} artist={antiSongs[4].artist} album_cover={antiSongs[4].album_cover}/>
                    </div>
                    <div className="song-card">
                        <SongCard song_name={antiSongs[5].song_name} artist={antiSongs[5].artist} album_cover={antiSongs[5].album_cover}/>
                    </div>
                    <div className="song-card">
                        <SongCard song_name={antiSongs[6].song_name} artist={antiSongs[6].artist} album_cover={antiSongs[6].album_cover}/>
                    </div>
                    <div className="song-card">
                        <SongCard song_name={antiSongs[7].song_name} artist={antiSongs[7].artist} album_cover={antiSongs[7].album_cover}/>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SongRows;
  