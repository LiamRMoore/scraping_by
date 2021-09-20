import './App.css';
import SearchResults from './search-results';
import {perform_get} from './api.service'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <SearchResults></SearchResults>
      </header>
      <button onClick={perform_get}>Get Results</button>
    </div>
  );
}

export default App;
