const Footer = () => {
    return (
        <div className="footer-container">
            <div className="footer-box">
                <span className="contribute">
                    Thanks for visiting! If you would like to contribute to our project,
                    please visit our GitHub repository. We welcome developers of all levels!
                </span>
                <span className="love">
                    This project was made with love by Emily, Lisa, Tony, and Marlea ♥
                </span>
                <span className="get-involved">
                    Get Involved
                </span>
                <div className="links-container">
                    <a className="links-content" href="https://github.com/MarleaM/OSS_Project" target="_blank">
                        <span> Documentation </span>
                    </a>
                    <a className="links-content" href="https://github.com/MarleaM/OSS_Project" target="_blank">
                        <span> Code of Conduct </span>
                    </a>
                    <a className="links-content" href="https://github.com/MarleaM/OSS_Project" target="_blank">
                        <span> Contributing Guidelines </span>
                    </a>
                </div>
            </div>
        </div>
    );
};

export default Footer;
