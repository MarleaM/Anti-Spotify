const Footer = () => {
    return (
        <div className="footer-container">
            <div className="footer-box">
                <div className="top">
                    <span className="visit-contribute-repository">
                        Thanks for visiting! If you would like to contribute to our project,
                        please visit our GitHub repository. We welcome developers of all levels!
                    </span>
                    <span className="made-with-love">
                        This project was made with love by Emily, Lisa, Tony, and Marlea ♡
                    </span>
                </div>
                <div className="bottom">
                    <span className="get-involved">Get Involved</span>
                    <div className="links-container">
                        <a className="documentation" href="https://github.com/MarleaM/OSS_Project" target="_blank">
                            <span className="documentation-text">Documentation</span>
                        </a>
                        <a className="code-of-conduct" href="https://github.com/MarleaM/OSS_Project" target="_blank">
                            <span className="code-of-conduct-text">Code of Conduct</span>
                        </a>
                        <a className="contributing-guidelines" href="https://github.com/MarleaM/OSS_Project" target="_blank">
                            <span className="contributing-guidelines-text">Contributing Guidelines</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Footer;
