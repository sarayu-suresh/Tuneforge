import './App.css';
import UploadForm from './components/UploadForm';
import TrainPanel from './components/TrainPanel';
import ChatBox from './components/ChatBox';

function App() {
  return (
    <div className="container">
      <h1>🧠 LLM Fine-Tuning Playground</h1>
      <UploadForm />
      <TrainPanel />
      <ChatBox />
    </div>
  );
}

export default App;