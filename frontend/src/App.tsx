
import './App.css';
import Banner from './components/Banner';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';


const App = () => {

  return (
    <div className="App">
      <div className = "navbar-fade-down">
        <Navbar />
        <Banner />
      </div>
      <div className = "footer-fade-up">
        <Footer />
      </div>
    </div>
  )
}

export default App
