import { FaGithub } from "react-icons/fa";


const Navbar = () => {
    return (
        <a href ="https://github.com/MarleaM/OSS_Project" target ="_blank" >
            <div className="github-button" style = {{color: "white"}}>
                <FaGithub size = {65}/>
            </div>
        </a>
    )
};
    
export default Navbar;