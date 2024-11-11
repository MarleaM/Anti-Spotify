
const AntiSongColumn = ({ antiSongs }: { antiSongs: string[] }) => {
    return (
    <div className = "title">
        <h1>Anti-Recommendations</h1>
        <div className="tileRow">
            {antiSongs.map((user) => (
            <div className="tile" key={user}>
                {user}
            </div>
            ))}
        </div>
    </div>
    );
  };
  
export default AntiSongColumn;
  