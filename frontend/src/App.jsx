import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import StoryLoader from "./components/StoryLoader";

function App() {
  return (
    <Router>
      <header>
        <h1>Interactive Story Generator</h1>
      </header>
      <main>
        <Routes>
          <Route path={"/story/:id"} element={<StoryLoader />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
