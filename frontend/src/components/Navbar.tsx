import { FaGithub } from "react-icons/fa";


const Navbar = () => {
    return ( 
        <div className="github-button" style = {{color: "white"}}>
            <a href ="https://github.com/MarleaM/OSS_Project" target ="_blank" className = "album-link">
                <FaGithub size = {65} color = "white"/>
            </a>
        </div>
    )
};
    
export default Navbar;