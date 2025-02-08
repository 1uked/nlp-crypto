import './App.css';
import Particle from "./components/Particle"
import PromptBar from "./components/PromptBar";
import Header from "./components/Header";

function App() {

    const handlePromptSubmit = (prompt) => {
        console.log('User prompt:', prompt);
    };

  return (
    <div className="App">
      <Particle></Particle>
        <Header></Header>
        <PromptBar onSubmitPrompt={handlePromptSubmit} />
    </div>
  );
}

export default App;
