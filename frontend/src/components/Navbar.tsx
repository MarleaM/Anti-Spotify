import { FaGithub } from "react-icons/fa";

/* current Navbar just shows clickable GitHub icon in top left */
const Navbar = () => {
    return ( 
        <div className="github-button" style = {{color: "white"}}>
            <a href ="https://github.com/MarleaM/Anti-Spotify" target ="_blank" className = "album-link">
                <FaGithub size = {65} color = "white"/>
            </a>
        </div>
    )
};
    
export default Navbar;