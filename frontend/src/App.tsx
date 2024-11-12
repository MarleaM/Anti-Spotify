
import './App.css';
import Banner from './components/Banner';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';


const App = () => {

  return (
    <div className="App">
      <Navbar />
      <Banner />
      <Footer />
    </div>
  )
}

export default App
